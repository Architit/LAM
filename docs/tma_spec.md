# Test Matrix Aggregator (TMA)

![Container Diagram](diagrams/tma_container.mmd)

TMA orchestrates automated test runs across a matrix of environments. It schedules
jobs, runs pytest, and aggregates the results into a concise report.

## Key Components

- **CLI (`cli.py`)** – triggers test runs and displays metrics.
- **Scheduler (`scheduler.py`)** – Celery app using Redis for message passing and
  result storage.
- **Aggregator (`aggregator.py`)** – executes pytest for a matrix expression and
  produces XML/HTML reports.
- **Metrics Store (`storage.py`)** – saves counts of tests, failures and skipped
  cases in YAML.
- **HTTP API (`api.py`)** – exposes `/trigger` and `/metrics` endpoints.
- **Configuration** – defined in `tma.yaml`; values may be overridden with
  environment variables.

## Workflow

1. A user or CI job calls `tma trigger --matrix <opts>` or posts to `/trigger`.
2. `schedule()` enqueues `run_tests` via Celery.
3. Workers run `aggregate_results()` which executes pytest and updates
   `reports/` files.
4. Metrics are persisted through `MetricsStore`.
5. The CLI or `/metrics` endpoint returns current statistics for dashboards or
   gating conditions.

---

В предыдущих версиях документа разделы с 1 по 25 содержали однотипные описания
поведения и взаимодействия модулей. Их заменила краткая сводка выше.

TMA включает CLI, планировщик Celery, модуль агрегации результатов и HTTP‑API.
Пользователь запускает задачу, планировщик ставит её в очередь, воркеры
выполняют тесты и сохраняют показатели в YAML. Статистику можно получить через
CLI или API.
