diff --git a/ROADMAP.md b/ROADMAP.md
index 0000000..0000000 100644
--- a/ROADMAP.md
+++ b/ROADMAP.md
@@ -12,6 +12,44 @@ LAM — “позвоночник” экосистемы: единый runtime, контракты, логирование, наблюдаемость и маршрутизация.
 - **Fail-safe:** retry/backoff/fallback/health — предсказуемо и тестируемо.
 - **WSL-friendly:** быстрые циклы разработки в ext4, минимизация зависаний.
 
+---
+
+## Dev Protocol (agents + users)
+Цель: минимальный шум, воспроизводимость, устойчивые контракты.
+
+### Общие правила
+- Не “болтаем”: каждое сообщение/коммит — либо фикс/патч, либо проверка, либо следующий шаг.
+- Никаких “подожди/сделаю позже”: работаем циклом **патч → тест → вывод → push**.
+- Любое изменение обязано иметь:
+  1) тест, 2) логику, 3) grep-able JSONL observability, 4) зафиксированную версию (push).
+- Не ломаем импорт-пути:
+  - runtime-скрипты либо используют официальный entrypoint, либо явно добавляют `sys.path` для submodules/agents.
+- Любой `reply_to` в comm-agent обязан быть зарегистрирован (Sink/mailbox), иначе будут `unknown_recipient`.
+
+### Стандарты данных
+- **Envelope Standard v1:** `context.trace_id`, `context.task_id`, опционально `parent_task_id`, `span_id`. :contentReference[oaicite:1]{index=1}
+- `taskarid = "{trace_id}:{task_id}"` для трассировки.
+- Observability события должны быть фильтруемы через:
+  - `LAM_LOG_LEVEL`
+  - `LAM_LOG_EVENTS` :contentReference[oaicite:2]{index=2}
+
+### Definition of Done
+- `python -m compileall -q` проходит
+- `pytest -q` проходит (минимум: unit + smoke)
+- Есть runtime smoke script/entrypoint (1 команда) для проверки фичи
+- Логи (JSONL) валидны: корректный `event` + ключевые поля (trace/task ids)
+
 ---
 
 ## Словарь

