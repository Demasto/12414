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