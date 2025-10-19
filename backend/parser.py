# -*- coding: utf-8 -*-
"""
Загрузка данных ТТР в PostgreSQL:
- goods, tariffs, production, consumption
- import_values (поддержка листов с 'YYYY, млн $' и/или 'YYYY, тонны'; обход всех листов)
- goods_flags (техрег/ПП1875/приказ 4114)
- country_dict (Страна | Страна капс | Недружественная | Регион)

Зависимости:
  pip install pandas psycopg2-binary openpyxl
"""

import re
import pandas as pd
import psycopg2

# ---------- КОНФИГ БД ----------
DB = dict(host="localhost", port=5433, dbname="Hackaton", user="postgres", password="123")

# ---------- ПУТИ К ФАЙЛАМ ----------
MASTER_PATH = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\2. Данные для решения кейса (1).xlsx"
IMPORT_LIFTS_PATH = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\Лифты - объем импорта Россия (1).xlsx"
IMPORT_PERF_PATH  = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\Парфюмерия_объем_импорта_Россия (1).xlsx"
IMPORT_ATM_PATH   = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\Банкоматы - объем импорта Россия (1).xlsx"
DICT_STRANA_PATH  = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\dict_strana (1) (1).xlsx"  # Страна | Недружественная | Регион

# справочник стран (лист с колонками: Страна | Страна капс | Недружественная | Регион)
DICT_STRANA_PATH  = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\dict_strana (1) (1).xlsx"

# ---------- УТИЛИТЫ ----------
def norm_rate(x):
    if pd.isna(x): return None
    s = str(x).strip().replace(",", ".").replace("%", "")
    if not s: return None
    v = float(s)
    return v/100.0 if v > 1 else v

def parse_year_series_money(cell):
    """из мастер-файла: '2022 - 286 млн $' -> {2022: 286.0}"""
    out = {}
    if pd.isna(cell): return out
    for part in str(cell).splitlines():
        m = re.search(r'(\d{4}).*?([\d\s.,]+)\s*млн', part, flags=re.I)
        if m:
            year = int(m.group(1))
            val = float(m.group(2).replace(" ", "").replace(",", "."))
            out[year] = val
    return out

def detect_year_and_unit(colname: str):
    """
    '2022' -> (2022, None)
    '2022, млн $' -> (2022, 'млн $')
    '2022, тонны' -> (2022, 'тонны')
    """
    s = str(colname or "").strip()
    m = re.match(r'^(\d{4})(?:\s*[,;]\s*(.+))?$', s)
    if not m:
        return None, None
    year = int(m.group(1))
    unit = (m.group(2) or "").strip().lower()
    return year, (unit if unit else None)

def wide_import_to_long_one_sheet(df):
    """
    Для одного листа:
      колонка 'Список стран-продавцов в Россию'
      и годовые: 'YYYY', 'YYYY, млн $', 'YYYY, тонны'
    Возвращает список dict: {country, year, value_usd_mln?, value_tons?}
    """
    # нормализуем заголовок стран
    col_country = None
    for c in df.columns:
        if "Список стран" in str(c):
            col_country = c; break
    if not col_country:
        return []
    df = df.rename(columns={col_country: "country"})

    cols = []
    for c in df.columns:
        y, unit = detect_year_and_unit(c)
        if y: cols.append((c, y, unit))

    rows = []
    for _, r in df.iterrows():
        country = str(r.get("country", "")).strip()
        if not country:
            continue
        for c, year, unit in cols:
            raw = r.get(c)
            if pd.isna(raw): 
                continue
            val = float(str(raw).replace(" ", "").replace(",", "."))
            rec = {"country": country, "year": year, "value_usd_mln": None, "value_tons": None}
            if unit and "тонн" in unit:
                rec["value_tons"] = val
            else:
                rec["value_usd_mln"] = val
            rows.append(rec)
    return rows

def merge_import_rows(rows_list):
    """
    Склеивает записи из разных листов: (country, year) — одна строка, оба показателя (млн $, тонны) при наличии.
    """
    merged = {}
    for rec in rows_list:
        key = (rec["country"], rec["year"])
        if key not in merged:
            merged[key] = {"country": rec["country"], "year": rec["year"], "value_usd_mln": None, "value_tons": None}
        if rec.get("value_usd_mln") is not None:
            merged[key]["value_usd_mln"] = rec["value_usd_mln"]
        if rec.get("value_tons") is not None:
            merged[key]["value_tons"] = rec["value_tons"]
    return list(merged.values())

def read_import_workbook(path):
    """
    Читает все листы книги импорта и объединяет.
    """
    xls = pd.ExcelFile(path)
    all_rows = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        rows = wide_import_to_long_one_sheet(df)
        all_rows.extend(rows)
    return merge_import_rows(all_rows)

def parse_code_from_caps(caps: str):
    """
    'AB-АБХАЗИЯ' -> 'AB'
    если нет дефиса — вернёт None
    """
    s = (caps or "").strip()
    if "-" in s:
        return s.split("-", 1)[0].strip()
    return None

def name_ru_from_caps(caps: str):
    """
    'AB-АБХАЗИЯ' -> 'АБХАЗИЯ'
    """
    s = (caps or "").strip()
    if "-" in s:
        return s.split("-", 1)[1].strip()
    return s or None

def text_to_grouping(text: str):
    """'Недружественная страна' -> 'unfriendly'; иначе 'friendly'"""
    t = (text or "").strip().lower()
    return "unfriendly" if "недруж" in t else "friendly"

# ---------- UPSERT ----------
def upsert_goods(cur, name, hs):
    cur.execute("""
        INSERT INTO ttr.goods(name, hs_code)
        VALUES (%s, %s)
        ON CONFLICT (hs_code) DO NOTHING
        RETURNING id;
    """, (name, hs))
    row = cur.fetchone()
    if row: return row[0], True
    cur.execute("SELECT id FROM ttr.goods WHERE hs_code=%s", (hs,))
    return cur.fetchone()[0], False

def upsert_tariffs(cur, good_id, applied, wto):
    cur.execute("""
        INSERT INTO ttr.tariffs(good_id, applied_rate, wto_bound_rate)
        VALUES (%s, %s, %s)
        ON CONFLICT (good_id) DO NOTHING
        RETURNING 1;
    """, (good_id, applied, wto))
    if cur.fetchone(): return 1, 0
    cur.execute("""
        UPDATE ttr.tariffs
        SET applied_rate=%s, wto_bound_rate=%s, updated_at=now()
        WHERE good_id=%s
          AND (applied_rate IS DISTINCT FROM %s OR wto_bound_rate IS DISTINCT FROM %s)
        RETURNING 1;
    """, (applied, wto, good_id, applied, wto))
    return 0, (1 if cur.fetchone() else 0)

def upsert_series(cur, table, good_id, series_map):
    ins = upd = 0
    for year, val in series_map.items():
        cur.execute(f"""
            INSERT INTO ttr.{table}(good_id, year, value_usd_mln)
            VALUES (%s, %s, %s)
            ON CONFLICT (good_id, year) DO NOTHING
            RETURNING 1;
        """, (good_id, year, val))
        if cur.fetchone(): ins += 1; continue
        cur.execute(f"""
            UPDATE ttr.{table}
            SET value_usd_mln=%s
            WHERE good_id=%s AND year=%s
              AND value_usd_mln IS DISTINCT FROM %s
            RETURNING 1;
        """, (val, good_id, year, val))
        if cur.fetchone(): upd += 1
    return ins, upd

def upsert_import_values(cur, good_id, items):
    ins = upd = 0
    for it in items:
        ctry, year = it["country"], it["year"]
        v_usd = it.get("value_usd_mln")
        v_ton = it.get("value_tons")

        cur.execute("""
            INSERT INTO ttr.import_values(good_id, year, country, value_usd_mln, value_tons)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (good_id, year, country) DO NOTHING
            RETURNING 1;
        """, (good_id, year, ctry, v_usd, v_ton))
        if cur.fetchone():
            ins += 1
            continue

        cur.execute("""
            UPDATE ttr.import_values t
            SET value_usd_mln = COALESCE(%s, t.value_usd_mln),
                value_tons    = COALESCE(%s, t.value_tons)
            WHERE t.good_id=%s AND t.year=%s AND t.country=%s
              AND ( (%s IS NOT NULL AND t.value_usd_mln IS DISTINCT FROM %s)
                 OR (%s IS NOT NULL AND t.value_tons    IS DISTINCT FROM %s) )
            RETURNING 1;
        """, (v_usd, v_ton, good_id, year, ctry, v_usd, v_usd, v_ton, v_ton))
        if cur.fetchone():
            upd += 1
    return ins, upd

def upsert_goods_flags(cur, good_id, in_techreg, in_pp1875, in_order4114):
    cur.execute("""
        INSERT INTO ttr.goods_flags(good_id, in_techreg, in_pp1875, in_order4114)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (good_id) DO UPDATE
        SET in_techreg=%s, in_pp1875=%s, in_order4114=%s, updated_at=now()
        WHERE ttr.goods_flags.good_id=%s
        RETURNING 1;
    """, (good_id, in_techreg, in_pp1875, in_order4114,
          in_techreg, in_pp1875, in_order4114, good_id))

def upsert_country_dict(cur, df):
    """
    Ожидает колонки (без учёта регистра/пробелов):
      'страна' | 'страна капс' | 'недружественная' | 'регион'
    """
    # нормализуем имена колонок
    cmap = {}
    for c in df.columns:
        k = re.sub(r'\s+', ' ', str(c).strip().lower())
        cmap[k] = c

    need = {"страна", "страна капс", "недружественная", "регион"}
    if not need.issubset(cmap.keys()):
        return 0, 0

    ins = upd = 0
    for _, r in df.iterrows():
        # код берём из «Страна капс» (до дефиса)
        caps_raw = str(r[cmap["страна капс"]]) if not pd.isna(r[cmap["страна капс"]]) else ""
        country_code = parse_code_from_caps(caps_raw)

        # русское имя: из «Страна»; если пусто — из хвоста «Страна капс»
        ru_raw = str(r[cmap["страна"]]) if not pd.isna(r[cmap["страна"]]) else ""
        country_ru = ru_raw.strip() or name_ru_from_caps(caps_raw) or None

        region = str(r[cmap["регион"]]).strip() if not pd.isna(r[cmap["регион"]]) else None
        grouping = text_to_grouping(str(r[cmap["недружественная"]]))

        # если нет кода — пропускаем строку (код — PK и NOT NULL)
        if not country_code:
            continue

        # INSERT
        cur.execute("""
            INSERT INTO ttr.country_dict(country_code, country_ru, country_caps, region, grouping)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (country_code) DO NOTHING
            RETURNING 1;
        """, (country_code, country_ru, caps_raw, region, grouping))
        if cur.fetchone():
            ins += 1
            continue

        # UPDATE только если что-то изменилось
        cur.execute("""
            UPDATE ttr.country_dict d
            SET country_ru  = COALESCE(%s, d.country_ru),
                country_caps= COALESCE(%s, d.country_caps),
                region      = COALESCE(%s, d.region),
                grouping    = %s
            WHERE d.country_code = %s
              AND ( d.country_ru  IS DISTINCT FROM %s
                 OR d.country_caps IS DISTINCT FROM %s
                 OR d.region      IS DISTINCT FROM %s
                 OR d.grouping    IS DISTINCT FROM %s )
            RETURNING 1;
        """, (country_ru, caps_raw, region, grouping,
              country_code, country_ru, caps_raw, region, grouping))
        if cur.fetchone():
            upd += 1

    return ins, upd

# ---------- ОСНОВНОЙ ПРОЦЕСС ----------
def main():
    print("Загрузка данных ТТР в PostgreSQL...\n")

    # мастер
    df_master = pd.read_excel(MASTER_PATH, sheet_name="данные")
    row_applied = df_master.iloc[0]
    row_wto     = df_master.iloc[1]
    row_prod    = df_master.iloc[2]
    row_cons    = df_master.iloc[3]
    row_flag_tr   = df_master.iloc[4]  # техрег
    row_flag_1875 = df_master.iloc[5]
    row_flag_4114 = df_master.iloc[6]

    # импорты: все листы
    imp_lifts = read_import_workbook(IMPORT_LIFTS_PATH)
    imp_perf  = read_import_workbook(IMPORT_PERF_PATH)
    imp_atm   = read_import_workbook(IMPORT_ATM_PATH)

    # справочник стран
    df_dict = None
    try:
        df_dict = pd.read_excel(DICT_STRANA_PATH)
    except Exception:
        pass

    goods_def = [
        {"name":"Лифты",      "hs":"8428 10", "col":"Лифты",      "imp":imp_lifts},
        {"name":"Парфюмерия", "hs":"3303 00", "col":"Парфюмерия", "imp":imp_perf},
        {"name":"Банкоматы",  "hs":"8472 90", "col":"Банкоматы",  "imp":imp_atm},
    ]

    conn = psycopg2.connect(**DB)
    conn.autocommit = False
    cur = conn.cursor()

    total = {
        "goods_ins":0,"goods_dup":0,
        "tariff_ins":0,"tariff_upd":0,
        "prod_ins":0,"prod_upd":0,
        "cons_ins":0,"cons_upd":0,
        "imp_ins":0,"imp_upd":0,
        "flags_upd":0,
        "cd_ins":0,"cd_upd":0
    }

    try:
        # страны
        if df_dict is not None:
            ins, upd = upsert_country_dict(cur, df_dict)
            total["cd_ins"] += ins; total["cd_upd"] += upd

        # товары
        for g in goods_def:
            name, hs, col, imp_rows = g["name"], g["hs"], g["col"], g["imp"]

            gid, inserted = upsert_goods(cur, name, hs)
            total["goods_ins" if inserted else "goods_dup"] += 1

            applied = norm_rate(row_applied[col])
            wto     = norm_rate(row_wto[col])
            ins, upd = upsert_tariffs(cur, gid, applied, wto)
            total["tariff_ins"] += ins; total["tariff_upd"] += upd

            ins1, upd1 = upsert_series(cur, "production",  gid, parse_year_series_money(row_prod[col]))
            ins2, upd2 = upsert_series(cur, "consumption", gid, parse_year_series_money(row_cons[col]))
            total["prod_ins"] += ins1; total["prod_upd"] += upd1
            total["cons_ins"] += ins2; total["cons_upd"] += upd2

            # флаги «да/нет»
            to_bool = lambda x: str(x).strip().lower().startswith("д")
            in_tr   = to_bool(row_flag_tr[col])
            in_1875 = to_bool(row_flag_1875[col])
            in_4114 = to_bool(row_flag_4114[col])
            upsert_goods_flags(cur, gid, in_tr, in_1875, in_4114)
            total["flags_upd"] += 1

            # импорт (млн $, тонны)
            ins, upd = upsert_import_values(cur, gid, imp_rows)
            total["imp_ins"] += ins; total["imp_upd"] += upd

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("\n❌ Ошибка, транзакция откатена:\n", e)
        raise
    finally:
        cur.close()
        conn.close()

    # лог
    print("\n=== РЕЗУЛЬТАТ ЗАГРУЗКИ ===")
    print(f"goods:         +{total['goods_ins']} new, {total['goods_dup']} existed")
    print(f"tariffs:       +{total['tariff_ins']} inserted, ~{total['tariff_upd']} updated")
    print(f"production:    +{total['prod_ins']} inserted, ~{total['prod_upd']} updated")
    print(f"consumption:   +{total['cons_ins']} inserted, ~{total['cons_upd']} updated")
    print(f"imports:       +{total['imp_ins']} inserted, ~{total['imp_upd']} updated")
    print(f"goods_flags:   ~{total['flags_upd']} upserted")
    if df_dict is not None:
        print(f"country_dict:  +{total['cd_ins']} inserted, ~{total['cd_upd']} updated")
    print("==========================\n")
    print("✅ Готово.")

if __name__ == "__main__":
    main()
