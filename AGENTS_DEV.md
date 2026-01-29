# Agent Dev Guide (LAM)

Эта инструкция — “контракт разработки” для людей и агентных помощников (Codex/LLM),
чтобы изменения в репо оставались устойчивыми, воспроизводимыми и тестируемыми.

## Правила внесения изменений

### 1) Делай маленькие PR/коммиты
- 1 задача = 1 коммит (или небольшая серия)
- Коммит-сообщения: `feat:`, `fix:`, `chore:`, `test:`, `obs:`

### 2) Никаких “магических” правок без тестов
Если меняешь поведение:
- добавь/обнови тест
- или добавь runtime smoke script (если это интеграционный путь)

### 3) Нормализация контрактов (Envelope / Context)
- Reply payload должен соответствовать Envelope Standard v1:
  - `status`, `context`, `result`, `error`, `metrics`
- Context propagation обязательна:
  - `trace_id`, `task_id`, `parent_task_id`, `span_id`
- Если agent создаёт задачи/подзадачи — `parent_task_id` должен указывать на родителя.

### 4) Observability (JSONL)
Используем `src/lam_logging.py`:
- `lam_logging.log(level, event, msg, **fields)` печатает 1 JSON на строку (grep-friendly)
- глобальные фильтры:
  - `LAM_LOG_LEVEL=error|warn|info|debug`
  - `LAM_LOG_EVENTS=csv` (например: `comm.enqueue,roaudter.route,mem.write`)

События должны быть стабильными (не менять название без причины).

### 5) Runtime smoke (обязателен для интеграционных цепочек)
Если ты добавил/изменил “путь” между агентами — добавь smoke:
- пример: `scripts/obs_smoke_roundtrip.py`

### 6) Запуск локальных проверок перед push
Минимум:
- `python -m compileall -q src && echo OK`
- `pytest -q` (или релевантный subset)

### 7) Не засоряй репо артефактами
- никаких логов/данных в git
- временные файлы: `/tmp`, `.venv`, `.pytest_cache` и т.п.

## Чек-лист перед merge
- [ ] Есть тест или smoke на новый/изменённый путь
- [ ] Не сломаны существующие тесты
- [ ] Логи JSONL фильтруются env
- [ ] Context не теряется (trace/task/parent/span)
- [ ] Коммиты маленькие и читаемые
