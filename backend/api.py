# -*- coding: utf-8 -*-
# api.py — REST API для клиентского UI
# Запуск:  uvicorn api:app --host 0.0.0.0 --port 8000 --reload
# Зависимости:
#   pip install fastapi uvicorn[standard] psycopg2-binary pandas numpy python-docx requests

import os
import io
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd
import psycopg2
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# ------- общий модуль логики (такой же, как в app.py) -------
from ttr_core.logic import (
    compute_recommendation,               # алгоритм мер (I/II)
    SYSTEM_PROMPT,                        # промт для чата (строгий стиль)
    sanitize_ai, clamp_measures_in_text,  # фильтры и защита от "лишнего"
    chat_completion, make_grounding_message,
    build_brief_docx,                     # DOCX «Справка по товару …»
    build_mosprom_docx                    # DOCX «Обращение в АНО “Моспром”»
)

# =============================
# Настройки БД (совпадают с app.py)
# =============================
DB_HOST = os.environ.get("PGHOST", "localhost")
DB_PORT = int(os.environ.get("PGPORT", "5433"))
DB_NAME = os.environ.get("PGDATABASE", "Hackaton")
DB_USER = os.environ.get("PGUSER", "postgres")
DB_PASS = os.environ.get("PGPASSWORD", "123")
DB_SCHEMA = "ttr"

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

# =============================
# FastAPI + CORS
# =============================
app = FastAPI(title="TTR API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # при необходимости сузьте до вашего фронта: ["http://<IP>:5173", ...]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Внутренние helper’ы работы с БД
# =============================
def fetch_good(good_id: int) -> Dict[str, Any]:
    with get_conn() as conn:
        df = pd.read_sql(f"SELECT id, hs_code, name FROM {DB_SCHEMA}.goods WHERE id=%s", conn, params=[good_id])
    if df.empty:
        raise HTTPException(404, "Товар не найден")
    return df.iloc[0].to_dict()

def fetch_tariffs(good_id: int) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql(
            f"SELECT applied_rate, wto_bound_rate FROM {DB_SCHEMA}.tariffs WHERE good_id=%s",
            conn, params=[good_id]
        )

def fetch_series(table: str, good_id: int) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql(
            f"SELECT year, value_usd_mln FROM {DB_SCHEMA}.{table} WHERE good_id=%s ORDER BY year",
            conn, params=[good_id]
        )

def fetch_imports(good_id: int) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql(
            f"""SELECT year, country,
                        COALESCE(value_usd_mln,0) AS value_usd_mln,
                        COALESCE(value_tons,0)    AS value_tons,
                        country_group
                 FROM {DB_SCHEMA}.import_values
                 WHERE good_id=%s""",
            conn, params=[good_id]
        )

def fetch_flags(good_id: int) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql(
            f"SELECT in_techreg, in_pp1875, in_order4114 FROM {DB_SCHEMA}.goods_flags WHERE good_id=%s",
            conn, params=[good_id]
        )

# =============================
# ENDPOINTS
# =============================

@app.get("/api/goods")
def api_goods():
    """Справочник товаров (id, hs_code, name)."""
    with get_conn() as conn:
        df = pd.read_sql(f"SELECT id, hs_code, name FROM {DB_SCHEMA}.goods ORDER BY name", conn)
    return df.to_dict(orient="records")


@app.get("/api/goods/{good_id}/dashboard")
def api_dashboard(good_id: int):
    """
    Полный набор данных для UI по конкретному товару:
      - good (id, hs_code, name)
      - tariffs (applied_rate, wto_bound_rate)
      - production/consumption time series
      - imports by country
      - flags (in_techreg, in_pp1875, in_order4114)
      - measures, summary (результат алгоритма)
    """
    good = fetch_good(good_id)
    tariffs = fetch_tariffs(good_id)
    prod = fetch_series("production", good_id)
    cons = fetch_series("consumption", good_id)
    imp = fetch_imports(good_id)
    flags = fetch_flags(good_id)

    measures, summary = compute_recommendation(tariffs, prod, cons, imp, flags)

    return {
        "good": good,
        "tariffs": tariffs.to_dict(orient="records"),
        "production": prod.to_dict(orient="records"),
        "consumption": cons.to_dict(orient="records"),
        "imports": imp.to_dict(orient="records"),
        "flags": flags.to_dict(orient="records"),
        "measures": measures,
        "summary": summary
    }


@app.get("/api/goods/{good_id}/report.docx")
def api_brief_docx(good_id: int):
    """
    DOCX «Справка по товару …» — тот самый связный текст с «Ключевыми ориентирами периода анализа».
    """
    good = fetch_good(good_id)
    tariffs = fetch_tariffs(good_id)
    prod = fetch_series("production", good_id)
    cons = fetch_series("consumption", good_id)
    imp = fetch_imports(good_id)
    flags = fetch_flags(good_id)

    measures, summary = compute_recommendation(tariffs, prod, cons, imp, flags)
    buf = build_brief_docx(good, measures, summary, tariffs, imp)

    filename = f"Spravka_{good['hs_code'].replace(' ','')}.docx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/api/goods/{good_id}/mosprom-letter.docx")
def api_mosprom_docx(good_id: int):
    """
    DOCX «Обращение в АНО “Моспром”».
    """
    good = fetch_good(good_id)
    tariffs = fetch_tariffs(good_id)
    prod = fetch_series("production", good_id)
    cons = fetch_series("consumption", good_id)
    imp = fetch_imports(good_id)
    flags = fetch_flags(good_id)

    measures, summary = compute_recommendation(tariffs, prod, cons, imp, flags)
    buf = build_mosprom_docx(good, measures, summary, tariffs, imp)

    filename = f"Mosprom_{good['hs_code'].replace(' ','')}.docx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/goods/{good_id}/chat")
def api_chat(good_id: int, body: Dict[str, Any]):
    """
    Чат по товару (тот же промт/логика, что в app.py).

    Request JSON:
      { "question": "строка вопроса" }

    Response JSON:
      { "answer": "текст ответа" }
    """
    question = (body or {}).get("question", "").strip()
    if not question:
        raise HTTPException(400, "question is required")

    # собираем «заземление» на основе расчёта мер (без внешних PDF/RAG)
    good = fetch_good(good_id)
    tariffs = fetch_tariffs(good_id)
    prod = fetch_series("production", good_id)
    cons = fetch_series("consumption", good_id)
    imp = fetch_imports(good_id)
    flags = fetch_flags(good_id)

    measures, summary = compute_recommendation(tariffs, prod, cons, imp, flags)
    grounding = make_grounding_message(good, measures, summary)

    # та же схема промта, что в app.py
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Основание для ответа (не показывай как источник):\n{grounding}"},
        {"role": "user",   "content": f"Вопрос: {question}"}
    ]

    try:
        raw = chat_completion(messages, temperature=0.15, max_tokens=900)
        ans = sanitize_ai(raw)
        ans = clamp_measures_in_text(ans, measures)
        return {"answer": ans}
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")
