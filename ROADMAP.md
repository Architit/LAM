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
- **Cold-restart-safe:** продолжение работы только после явного сигнала; recovery начинается с read-only sync (pwd, git status -sb).

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

### Срочно (Governance override)
- [!] DevKit обязателен для всех репозиториев RADRILONIUMA
- [!] `apply_patch` / `applypatch` / `apply-patch` запрещены (не часть окружения / недетерминировано)
- [!] Каноничный патчер: `devkit/patch.sh` (или `git apply --index` только при починке самого DevKit)
- [!] Цель: срочная унификация patcher между LAM и RADRILONIUMA-PROJECT, затем авто-синк DevKit

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
  - comm-agent: enforcement legacy {'reply': ...} → Envelope v1 (2026-02-10)
  - codex-agent: Core.answer(payload dict) → Envelope Standard v1; добавлен tests/test_codex_envelope.py
  - E2E: taskarid → codex → roaudter: trace/context сохранён; codex отдаёт Envelope v1 (2026-02-10)
  - Phase 1.1: DoD — roaudter дублирует provider_used/latency_ms/attempts в metrics (тест: tests/test_roaudter_metrics_mirror_v11.py) (2026-02-10)
  - Infra: scripts/run_comm_* добавляют ROAUDTER_SRC в sys.path + Sink гарантирует context dict (2026-02-10)

---

## Фаза 2 — Observability: видеть важное без шума (1–2 недели)
- [x] Phase 2 CLOSED: comm/roaudter/mem/evt observability tests green (tests: test_comm_agent_observability_logging, test_roaudter_observability_logging, test_memory_observability_logging, test_event_manager_observability_logging) (2026-02-11 07:24 UTC)
- [!] Scope: Phase 2 closure is currently confirmed only for repository LAM. Ecosystem-wide (15 repos) closure is not yet confirmed.

- [x] Observability verified: comm.enqueue/comm.dequeue + roaudter.route/result/deliver (tests: test_comm_agent_observability_logging, test_roaudter_observability_logging) (2026-02-11 07:19 UTC)

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
- Learning Signals v1 (contracts-only, derivation-only) — Phase 4.2 (2026-02-10)

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
- [x] 2026-02-10 — governance: Safety Check for untracked files clarified (staged diff canonical)
- [x] 2026-02-10 — contracts: PolicyConstraint v1 added (policy boundaries, contract-only)
- [x] 2026-02-10 — governance: Phase 3 closure recorded (Semantics/Memory/Reflection)
- [x] 2026-02-10 — protocol: Cold Restart / Workflow Recovery v1 documented (docs/protocols)
- [x] 2026-01-30 — repo hygiene: добавлен .gitignore для runtime artifacts (logs/, memory/)

- [x] 2026-02-12 — governance: P2 baseline matrix (15 repos) completed in DEV_MAP (DONE=2, BLOCKED=1, PENDING=12)

## Фаза Z — Agent SDK Integrations v0 (⏭ next after Runtime EntryPoint v0)

Цель: подключить Claude Agent SDK как backend-инструмент Codex (не отдельный агент на v0).

### План (v0)
- [ ] Добавить интеграцию Claude Agent SDK как "codex tool backend"
- [ ] Smoke: 1 команда → 1 small task → envelope ok → trace ok
- [ ] DoD: не ломает существующий codex/openai path

### Phase 4 Review Findings (pre-4.3)
- [ ] R1: Spec drift — derivation mentions non-existent fields:
  - ReflectionSnapshot.snapshot_id references `input_fingerprints` (field missing)
  - LearningSignal.signal_id references `source_fingerprints` (field missing)
- [ ] R2: PolicyConstraint.condition.predicates underspecified (op set, field-path format, AND/OR, missing-field semantics)
- [ ] R3: Policy vs Learning boundary risk: `freeze_learning` / `rate_limit_adaptation` + learning proxies/attribution weights can be misread as runtime bridge
- [ ] R4: PolicyConstraint wording: deterministic derivation/representation vs governance-defined semantics/effect needs explicit separation
- [ ] R5: PolicyConstraint lacks explicit Non-Goals (no enforcement / no execution blocking / no conflict resolution), unlike ReflectionSnapshot “proposal-only” guardrails
- [ ] Recommendation: address findings via **v1.x addenda (contract-only)** before starting Phase 4.3 (Adaptation Proposals)


- [x] 2026-02-12 — governance: P2 remediation wave-1 validated (Roaudter-agent, LAM-Codex_Agent, LAM_Comunication_Agent, Operator_Agent) -> DONE=6, BLOCKED=0, PENDING=9

- [x] 2026-02-12 — governance: P2 remediation wave-2 validated (Archivator_Agent, CORE, J.A.R.V.I.S) -> DONE=9, BLOCKED=0, PENDING=6

- [x] 2026-02-12 — governance: P2 remediation wave-3 validated (LAM_DATA_Src, LAM_Test_Agent, System-, TRIANIUMA_DATA_BASE, Trianiuma, Trianiuma_MEM_CORE) -> DONE=15, BLOCKED=0, PENDING=0

- [x] 2026-02-12 — governance: P2.4 runtime closure proof matrix initialized in DEV_MAP (governance_done=15/15, runtime_proof DONE=1, PENDING=14)

- [x] 2026-02-12 — governance: P2.4 wave R1 executed (Roaudter-agent, LAM-Codex_Agent, LAM_Comunication_Agent); no promotions (DONE=1, PENDING=14), blockers logged

- [x] 2026-02-12 — governance: P2.4 wave R2 executed (Archivator_Agent, CORE, J.A.R.V.I.S); no promotions (DONE=1, PENDING=14), blockers logged

- [x] 2026-02-12 — governance: P2.4 wave R3 executed (LAM_DATA_Src, LAM_Test_Agent, Operator_Agent); no promotions (DONE=1, PENDING=14), blockers logged

- [x] 2026-02-12 — governance: P2.4 wave R4 executed (System-, TRIANIUMA_DATA_BASE, Trianiuma, Trianiuma_MEM_CORE); no promotions (DONE=1, PENDING=14), blockers logged

- [x] 2026-02-12 — governance: P2.4 wave R5 planned in DEV_MAP as unblock package (pytest bootstrap policy + runtime smoke template + promotion evidence checklist), no status promotion by design

- [x] 2026-02-12 — governance: P2.4 wave R5 published in LAM (bootstrap policy + smoke template + evidence checklist + operator blocks); R6 queued, no status promotion by design

- [x] 2026-02-13 — governance: P2.4/R6 strict gate defined (`python3 >= 3.10` + mandatory `.venv/bin/python` runner for promotion evidence)

- [x] 2026-02-13 — governance: P2.4/R6 readiness audit completed (14 pending repos; BLOCKED=14 by missing `.venv` runner and smoke template)

- [x] 2026-02-13 — governance: P2.4 wave R6.1 executed for first 3 repos; no promotions due offline `pytest` bootstrap failure (PyPI/DNS unavailable)

- [x] 2026-02-13 — governance: R6.1 offline wheelhouse fallback policy published and linked to bootstrap/operator/checklist contracts

- [x] 2026-02-13 — governance: P2.4 wave R6.1 retry executed (same 3 repos); no promotions due missing `wheelhouse/` in all targets

- [x] 2026-02-13 — governance: R6.1 retry blocker root-cause recorded (`lam-wheelhouse-py312.tgz` missing before unpack/distribution)

- [x] 2026-02-13 — governance: runtime-proof host-role contract fixed (builder online vendoring / runner offline `--no-index --find-links`)
