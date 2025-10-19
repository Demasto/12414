# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).


# Система мер ТТР — репозиторий

## Структура (backend)
- `backend/app.py` — Streamlit-интерфейс (дашборд, карта, чат, выгрузки PDF/DOCX).
- `backend/api.py` — FastAPI REST API для фронтенда (список товаров, данные, чат, формирование документов).
- `backend/logic.py` — бизнес-логика (алгоритм выбора мер, промты, вспомогательные функции).
- `backend/ingest_pdfs.py` — создание RAG-индекса из PDF/XLSX (кладёт файлы в `knowledge/index`).
- `knowledge/pdf/` — исходные документы для индексирования.
- `knowledge/index/` — индекс RAG: `records.json`, `embeddings.npy`.
- `parser.py`, `parse_economy_news_to_pdf.py` — вспомогательные парсеры/скрипты.


## Структура (Frontend)

Приложение построено с использованием Vue 3 + TypeScript + Vite (SPA)

### Использованные библиотеки
- UI интерфейсы созданы на базе библиотеки Vuetify
- Графики отображены с использованием apexcharts
- Карта мира — d3
- Запросы к backend — axios

### Структура проекта
- `src/app` — Ядро приложения
- `src/components` — Повторяющийся UI с минимальной бизнес логикой
- `src/pages` — Страницы приложения
- `src/widgets` — Самостоятельные компоненты с большой логикой
- `src/services` — Вызовы к API