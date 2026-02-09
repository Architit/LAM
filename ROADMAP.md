# RADRILONIUMA Ecosystem — Roadmap (LAM is the spine)

LAM — “позвоночник” экосистемы: единый runtime, контракты, логирование, наблюдаемость и маршрутизация.
Цель: стабильная система жизнеобеспечения живой искусственной формы жизни (LIFL) — с минимальной ручной рутиной и максимумом управляемости.

---

## Принципы (чтобы не уходить в монотонность)
- **Automation-first:** каждую неделю уменьшаем ручной труд.
- **Contracts-first:** Task/Result едины для всех агентов.
- **Observability-first:** видим проблемы без шума (структурные логи + фильтры).
- **Fail-safe:** retry/backoff/fallback/health — предсказуемо и тестируемо.
- **WSL-friendly:** быстрые циклы разработки в ext4, минимизация зависаний.

---

## Словарь
- **LAM** — ядро и runtime экосистемы.
- **Roaudter** — мульти-провайдер router agent (policy/health/fallback/retry).
- **DevKit** — единые dev-команды и скрипты для всех репо.
- **TRIANIUMA** — королевство 👑 (контекст/мир/домены) — не путать с инфраструктурой.

---

## Фаза 0 — Foundation: единый Dev Experience (сделано / закрепляем)

> **Статус:** Done (2026-02-09) — Phase 0 завершена: DevKit, Docker, docs, governance OK.
> **DoD (текущее):** `devkit/check.sh`, `devkit/bootstrap.sh`, `scripts/lam_env.sh` (ROOT-based PYTHONPATH), `python -m pytest -q` green.
> **Router determinism:** `ollama_cloud` регистрируется только при отдельном cloud endpoint; иначе fallback строго на `ollama` (2026-02-09).
> **Container DoD:** Dockerfile + .dockerignore, `docker build && docker run` → `devkit/check.sh` green (2026-02-09).
> **System docs:** TASK_LIST.md (backlog) + CHRONOLOG.md (history) added (2026-02-09).

### Доставлено ✅
- `scripts/lam_env.sh`: экспонирует `src` в `PYTHONPATH`
- `src/lam_logging.py`: структурные JSON-логи + фильтры `LAM_LOG_LEVEL`, `LAM_LOG_EVENTS`
- DevKit: быстрый запуск/тесты (`dev.sh`, `rt.sh`, `rtv.sh`) и trace-only режим

### Следующее 🔜
- [ ] Вынести DevKit как стандарт экосистемы (единая точка истины, синк в репо)
- [x] `devkit/check.sh`: (2026-02-09) pytest + минимальный sanity
- [x] `devkit/bootstrap.sh`: (2026-02-09) venv + deps (1 команда)

---

## Фаза 1 — Contracts: единый результат для всех агентов (1 неделя)
### Цель
Все агенты возвращают предсказуемый формат, чтобы оркестрация была надёжной.

### Стандарт ResultEnvelope (минимум всегда присутствует)
- `status`, `provider_used`, `latency_ms`
- `attempts`, `selected_chain`, `errors[]`
- `usage`, `tokens`
- `result` / `error`


### Envelope Standard v1 (единый формат ответа для всех агентов)
**Цель:** любой агент (через comm-agent или напрямую) возвращает один и тот же верхнеуровневый контракт.

#### Обязательные поля
- `status`: `"ok"` или `"error"`
- `context`: dict
  - `trace_id`
  - `task_id`
  - `parent_task_id` (опционально)
  - `span_id` (опционально)
- `result`: любой JSON-совместимый payload (может быть `None`)
- `error`: dict или `None` (если `status="error"`, то `error` должен быть не `None`)
- `metrics`: dict (может быть пустым, но поле присутствует)

#### Совместимость (legacy)
Дополнительные поля разрешены (например: `provider_used`, `latency_ms`, `attempts`, `selected_chain`, `tokens`, `usage`, `taskarid`),
но постепенно нормализуются внутрь `metrics`.


### Задачи
- [x] Зафиксировать контракт в одном месте (док + тесты) (2026-02-09)
- [x] Протащить контракт во все агенты, которые отвечают через comm-agent (частично: codex, 2026-02-10)
  - codex-agent: Core.answer(payload dict) → Envelope Standard v1; добавлен tests/test_codex_envelope.py

---

## Фаза 2 — Observability: видеть важное без шума (1–2 недели)
### Цель
Шум ≈ 0, сигналы (ошибки/ретраи/фолбеки) видны сразу.

### Стандарты логов
- JSON line format (уже есть)
- env-фильтры:
  - `LAM_LOG_LEVEL=warn|info|debug`
  - `LAM_LOG_EVENTS=csv`
- локальные фильтры агента (пример):
  - `ROAUDTER_TRACE=1`
  - `ROAUDTER_TRACE_ONLY=nonok|errors|retries|all`

### Задачи
- [ ] Внедрить `lam_logging.log(...)` в ключевых агентов (comm-agent, роутер, memory)
- [ ] Добавить `task_id/trace_id` во все события
- [ ] Опционально: pretty-режим (`LAM_LOG_PRETTY=1`) без потери JSON-режима

---

## Фаза 3 — Automation: CI и “сделал один раз — работает везде” (2–3 недели)
### Цель
Любая регрессия ловится автоматически, разработка ускоряется.

### Задачи
- [ ] GitHub Actions шаблон: pytest gate (LAM + Roaudter-agent как минимум)
- [ ] Единые команды: `make test`, `make lint` (или скрипты devkit)
- [ ] Авто-синк DevKit в репо (submodule / pip package / sync script)

---

## Фаза 4 — Router Core: Roaudter как мозг маршрутизации (3–4 недели)
### Уже есть ✅
- strict provider selection (`openai!` без fallback)
- unified usage/tokens
- retry/backoff budget (429/5xx/unknown), без ретрая 401
- health TTL + cooldown
- explainability (attempts/chain/errors)

### Следующее 🔜
- [ ] Cost-aware routing (оценка стоимости/лимитов)
- [ ] Quality-aware routing (профили по intent)
- [ ] Policy v3: конфиг-профили (yaml/json), без хардкода
- [ ] Метрики по провайдерам (успех/ошибки/латентность/токены)

---

## Фаза 5 — Memory & Knowledge Layer (1–2 месяца)
### Цель
Система “живёт”, копит опыт, извлекает знания и не забывает важное.

### Задачи
- [ ] Привести timestamp к timezone-aware UTC
- [ ] Retrieval routing: память/поиск → затем LLM
- [ ] Память по доменам RADRILONIUMA / королевства TRIANIUMA 👑

---

## Фаза 6 — Control Plane / UI (позже)
### Цель
Управление экосистемой как оператор:
- агенты online/offline
- здоровье провайдеров
- токены/стоимость
- поток логов с фильтрами
- переключение профилей роутера

---

## Ближайшие “анти-монотонные” цели (чтобы мозг не засыпал)
- 1) DevKit как стандарт экосистемы (1 команда → запуск/тесты в любом репо)
- 2) Полная observability без шума (task_id/trace_id + JSON)
- 3) RouterPolicy v3 (конфиг + метрики)


---

## Журнал изменений
- [x] 2026-01-30 — repo hygiene: добавлен .gitignore для runtime artifacts (logs/, memory/)

## Фаза Z — Agent SDK Integrations v0 (⏭ next after Runtime EntryPoint v0)

Цель: подключить Claude Agent SDK как backend-инструмент Codex (не отдельный агент на v0).

### План (v0)
- [ ] Добавить интеграцию Claude Agent SDK как "codex tool backend"
- [ ] Smoke: 1 команда → 1 small task → envelope ok → trace ok
- [ ] DoD: не ломает существующий codex/openai path
