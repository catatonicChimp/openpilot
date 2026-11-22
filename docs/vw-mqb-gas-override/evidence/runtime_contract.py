"""Executable review model only; not production vehicle-control code.

No timing thresholds, CAN serialization, or platform authority inference lives here.
The purpose is to compute prerequisites that Sigil's branch simulator cannot.
"""
from dataclasses import dataclass
from enum import Enum


class State(Enum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    OVERRIDE = 'override'
    FAULTED = 'faulted'


@dataclass(frozen=True)
class Request:
    state: State
    inputs_fresh: bool
    authority_valid: bool
    fault_present: bool
    permit_allowed: bool
    safety_authorized: bool
    # Deliberately untrusted: caller-selected output state cannot grant authority.
    claimed_output_state: State


def active_command_eligible(request: Request) -> bool:
    """Eligibility for a new active/override request, NOT all inactive/fault CAN."""
    return (
        request.inputs_fresh
        and request.authority_valid
        and not request.fault_present
        and request.state in (State.ACTIVE, State.OVERRIDE)
        and request.permit_allowed
        and request.safety_authorized
    )


@dataclass(frozen=True)
class Candidate:
    controller: str
    safety: str
    resolved_headers: str
    firmware: str
    configuration: str
    target_group: str


@dataclass(frozen=True)
class Approval:
    candidate: Candidate
    action: str


class ApprovalRegistry:
    """Serialized reference lifecycle; no claims about cross-process atomicity."""

    def __init__(self, candidate: Candidate):
        self.current = candidate
        self.approvals: dict[str, Approval] = {}
        self.invalidations = 0

    def approve(self, action: str) -> None:
        self.approvals[action] = Approval(self.current, action)

    def change_candidate(self, candidate: Candidate) -> None:
        if self.current != candidate:
            self.current = candidate
            self.approvals.clear()
            self.invalidations += 1

    def can_execute(self, action: str) -> bool:
        approval = self.approvals.get(action)
        return approval is not None and approval.candidate == self.current

    def execute(self, action: str, runner) -> bool:
        # In a real executor, serialize check + use or consume an immutable snapshot.
        # This model has no callbacks between the check and action invocation.
        if not self.can_execute(action):
            return False
        runner(self.current)
        return True


@dataclass
class RuntimeSession:
    """Serial event trace model; watchdog detection time is supplied, not invented."""
    retained_state: State
    authorized: bool = True

    def watchdog_revoke(self) -> None:
        self.authorized = False

    def attempt(self, request: Request) -> bool:
        # A stale request cannot restore the independently revoked session authority.
        from dataclasses import replace
        return active_command_eligible(replace(
            request, state=self.retained_state,
            authority_valid=self.authorized and request.authority_valid,
        ))
