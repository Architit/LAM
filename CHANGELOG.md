# Changelog

## [Unreleased]
### Added
- Container DoD: Dockerfile + .dockerignore run devkit/check.sh (pytest green)
- DevKit v0: devkit/bootstrap.sh and devkit/check.sh
- TASK_LIST.md (source of truth backlog)
- CHRONOLOG.md (system history)

### Changed
- scripts/lam_env.sh: deterministic ROOT-based PYTHONPATH (repo root + src + agents)

### Fixed
- Roaudter: deterministic ollama_cloud registration (explicit cloud endpoint only; fallback to ollama)

## 0.1.0
- Initial release of TMA modules, Dockerfile, and workflow integration.
