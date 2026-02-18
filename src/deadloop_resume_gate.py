from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ResumeGateResult:
    decision: str
    missing_fields: list[str]
    reason: str


def evaluate_resume_gate(
    *,
    code_delta_refs: list[str],
    test_delta_refs: list[str],
    validation_command: list[str],
    validation_result: str,
    operator_confirmed: bool,
) -> ResumeGateResult:
    missing: list[str] = []

    if not code_delta_refs:
        missing.append("code_delta_refs")
    if not test_delta_refs:
        missing.append("test_delta_refs")
    if not validation_command:
        missing.append("validation_command")
    if not validation_result:
        missing.append("validation_result")
    if not operator_confirmed:
        missing.append("operator_confirmation")

    if missing:
        return ResumeGateResult(
            decision="HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
            missing_fields=missing,
            reason="resume tuple is incomplete",
        )

    if validation_result.strip().upper() != "PASS":
        return ResumeGateResult(
            decision="HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
            missing_fields=[],
            reason="validation_result is not PASS",
        )

    return ResumeGateResult(
        decision="PASS",
        missing_fields=[],
        reason="resume tuple complete and operator confirmed",
    )
