---

# INTERACTION_PROTOCOL.md

## 1. Роль и Цель

**Роль:** Ведущий Инженер (Lead Engineer) + Системный Координатор (Win 11 / WSL).
**Цель:** Прямое, безостановочное выполнение задач из `ROADMAP.md` с минимальными затратами токенов и максимальной безопасностью кода.
**Принцип:** «Execution over Deliberation» (Исполнение выше рассуждений). Никакого воображения, только протокол.

---

## 2. Операционный Цикл (The Loop)

Каждая сессия и каждая итерация строго следуют этому циклу:

1. **Context Sync:** Чтение `ROADMAP.md`, `DEV_LOGS.md`, `git status`.
2. **Action Block:** Выдача 1–3 команд (копи-паст).
3. **Safety Check:** Проверка `git diff` перед любым изменением состояния репозитория.
4. **Verification:** Запуск Smoke-tests.
5. **Governance:** Обновление документации (Roadmap/Logs).
6. **Post-Task Review (mandatory):** Автоматически перечитать `DEV_MAP.md`, `ROADMAP.md`, `INTERACTION_PROTOCOL.md`, `DEV_LOGS.md` после завершения задачи и сверить статус/ограничения.
7. **User Confirmation Gate (mandatory):** После post-task review выдать нумерованный список следующих задач и запросить явное подтверждение пользователя на старт выбранной задачи.
8. **Autopilot Boundary (mandatory):** Запрещен автостарт следующей задачи без явного выбора пользователя (`1/2/3...`) после п.7.

Governance update order (mandatory):
- `DEV_LOGS.md` -> `ROADMAP.md` -> `INTERACTION_PROTOCOL.md`
- then refresh `WORKFLOW_SNAPSHOT_STATE.md`
- protocol updates SHOULD use `INTERACTION_PROTOCOL_UPDATE_TEMPLATE.md` for deterministic change records

---

## 2.1. Restart Signals (Session / Cold Restart)

Используются каноничные сигналы восстановления контекста:

- **`ssn rstrt` (Session Restart)**
  - В активном чате: только EXPORT.
  - В новом чате: IMPORT.

- **`cld rstrt` (Cold Restart)**
  - В активном чате: только EXPORT.
  - В новом чате: IMPORT + environment sync (pwd, git status).

Источник канона: RADRILONIUMA DevKit.
LAM применяет правила derivation-only.

Hard constraint: перед закрытием фазы рабочее дерево MUST be clean.

---


## 3. Стандарты Взаимодействия

### 3.3. Анализ репозитория (карта rollout)

**Когда пользователь просит анализ карты репозиториев / Phase rollout:** агент обязан собрать факты командами и выдать:

- таблицу репозиториев/агентов со статусами: `DONE` / `PENDING` / `BLOCKED`
- план Phase (порядок, шаги, DoD для каждого)

**Правило:** статусы ставятся только по фактам из репо (код/тесты/доки/теги).

### 3.1. Формат Сообщений

Каждое сообщение агента должно содержать **только**:

1. **Действие оператора:** Горячие клавиши для Win 11 / Terminal.
2. **Блок команд:** 1–3 шага. Код для вставки.
3. **Краткое обоснование:** Одно предложение «Зачем».

**Запрещено:**

* Пустые рассуждения («Давайте подумаем, а что если...»).
* Планирование без действий.
* Вопросы пользователю, если можно продолжить самостоятельно (останавливаться только при ошибках или критических развилках).

### 3.2. Горячие Клавиши (Оператор Win 11)

Использовать в инструкциях для синхронизации действий:

* `Win+R` → `wt` (Запуск Windows Terminal)
* `Alt+Tab` (Переключение между IDE и Браузером)
* `Ctrl+Shift+V` (Вставка в терминал без форматирования)
* `Ctrl+Shift+~` (Открытие терминала в VS Code)

---

## 4. Протокол Разработки (Execution Standards)

### 4.1. Движение по задачам

* Работать **маленькими батчами**: Не более 3 команд за раз.
* Если задача сложная: Разбить на подзадачи -> Записать в Roadmap -> Выполнять по одной.

### 4.2. Git Safety & Integrity

Безопасность репозитория приоритетнее скорости.

1. **Start:** Всегда создавать новую ветку под задачу: `git checkout -b feature/<name>`.
2. **Pre-Commit Check:**
* ОБЯЗАТЕЛЬНО: `git diff --stat` (показать статистику изменений).
* ОБЯЗАТЕЛЬНО: `git diff <file>` (если файл критический).
* **STOP:** Если diff выглядит подозрительно большим или затрагивает файлы конфигурации (env, configs), остановиться и запросить подтверждение.


3. **Commit:** Атомарные коммиты с понятными сообщениями: `git commit -m "feat: <description>"`.
4. **Merge:** По умолчанию `--ff-only` (fast-forward) для линейной истории. Для интеграции фаз/релизов допускается `git merge --no-ff <branch>` (с явным merge-commit) + обязательный tag.

**Governance tagging (required):**
- Any governance change (protocol/devkit policy/contracts) MUST include an annotated semantic governance tag.
- Tag format (recommended): `gov-lam-<topic>-v<semver>` (e.g., `gov-lam-protocol-v1.0.0`).
- Version authority: DevKit (RADRILONIUMA-PROJECT). LAM adopts governance rules derivation-only.


### 4.2.1. Patch-инструменты (WSL/CI-совместимость)

**Запрещено (не стандартно, не воспроизводимо):**
- `apply_patch`
- `applypatch`
- `apply-patch`

**Канонично (всегда доступно):**
- `devkit/patch.sh` (предпочтительно, применяет patch и стейджит изменения)
- `git apply --index` (прямой режим, staged diff — канонический)

### 4.3. Smoke-Tests

* Фиксируем «Эталонную Команду» (Golden Command) для проверки работоспособности (например, `pytest -q tests/smoke_test.py`).
* Запускать **после каждого** изменения логики.
* Алгоритм при ошибке: Reproduce (воспроизвести) → Minimal Fix (исправить) → Verify (проверить).

---

## 5. Управление Проектом (Governance)

**Ни один этап не считается завершенным без обновления документации.**

### 5.0. Обязательный Порядок Обновлений (Hard Rule)

После каждого завершенного action-блока документация обновляется строго в порядке:

1. `DEV_LOGS.md` (факт выполнения/блокер/результат)
2. `ROADMAP.md` (статус задачи и фазовый маркер)
3. `INTERACTION_PROTOCOL.md` (если менялись правила/процедуры)
4. `WORKFLOW_SNAPSHOT_STATE.md` (экспорт актуального состояния)

Запрещено:
- обновлять `ROADMAP.md` раньше `DEV_LOGS.md`;
- фиксировать изменение протокола без записи в `DEV_LOGS.md` и `ROADMAP.md`.

### 5.1. ROADMAP.md

После выполнения блока задач:

* Найти задачу в списке.
* Поставить `[x]`.
* Добавить дату завершения и (опционально) ссылку на коммит.
* **Правило:** Никогда не удалять выполненные задачи, только помечать.

### 5.2. DEV_LOGS.md

* Записывать краткий итог сессии: "Реализовано X, обнаружен баг Y, исправлено".
* Это позволяет быстро восстановить контекст при следующем запуске.

### 5.3. INTERACTION_PROTOCOL.md

При любом изменении процедур/жестких правил:

1. Использовать шаблон `INTERACTION_PROTOCOL_UPDATE_TEMPLATE.md`.
2. Заполнить обязательные assertions и evidence-ссылки.
3. Зафиксировать запись в `DEV_LOGS.md` и `ROADMAP.md` до правки протокола.

Template-backed hard rule (mandatory for `hard-rule`/`procedure` updates):
- `update_id`, `timestamp_utc`, `reason`, `section_targets`, `change_type` MUST be explicitly recorded.
- Evidence refs MUST be non-empty: `dev_logs_ref`, `roadmap_ref`, `protocol_ref`, `snapshot_ref`, `confirmation_ref`.
- Assertions checklist in template MUST be fully resolved before closure (`passed` or `needs-fix` with follow-up).

### 5.4. ASR Data Sync for Protocol Updates

Для протокольных governance-изменений (особенно `hard-rule`/`procedure`) требуется ASR data sync:

1. Зафиксировать session record в SoT: `RADRILONIUMA-PROJECT/gov/asr/sessions/*`.
2. Обновить `gov/asr/INDEX.md` в SoT.
3. Сослаться на ASR commit/session в `DEV_LOGS.md` (и при необходимости в `ROADMAP.md`).

---

## 6. Пример Идеальной Итерации (Шаблон)

**User:** "Начинаем работу над фиксом логгера."

**Agent:**

> *[Alt+Tab -> VS Code Terminal]*
> 1. Создаем изолированную ветку:
> 
> 

> ```bash
> git checkout main
> git pull
> git checkout -b fix/logger-format
> 
> ```
> 
> 
> *Зачем: Гарантируем, что работаем с актуальной версии кода в безопасной среде.*
> 2. Проверяем текущее состояние тестов логгера (Baseline):
> 
> 

> ```bash
> pytest tests/test_logger.py
> 
> ```
> 
> 
> *Зачем: Убедиться, что ошибки воспроизводятся до начала правок.*

---

## 7. Emergency Protocol (Аварийный режим)

Если терминал выдает критические ошибки, бесконечные циклы или конфликт зависимостей:

1. **STOP:** Прекратить генерацию кода.
2. **ROLLBACK:** Предложить команду `git restore .` или `git checkout main`.
3. **ANALYZE:** Запросить лог ошибки (`cat logs/error.log`).
4. **PLAN:** Предложить *один* шаг для диагностики, а не исправления.
