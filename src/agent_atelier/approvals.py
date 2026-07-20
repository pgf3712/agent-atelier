"""Scoped, single-use human approvals for sensitive action proposals."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import secrets


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CONSUMED = "consumed"


@dataclass
class ApprovalRequest:
    request_id: str
    action: str
    argument_digest: str
    explanation: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    token: str | None = None


class ApprovalStore:
    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}

    def propose(self, action: str, arguments: dict[str, object], explanation: str) -> ApprovalRequest:
        if action not in {"export_brief"}:
            raise ValueError("Action is not eligible for approval.")
        if not explanation.strip():
            raise ValueError("Approval explanation must not be empty.")
        digest = _digest_arguments(arguments)
        request_id = f"APR-{secrets.token_hex(4)}"
        request = ApprovalRequest(request_id, action, digest, explanation.strip())
        self._requests[request_id] = request
        return request

    def resolve(self, request_id: str, *, approve: bool) -> ApprovalRequest:
        request = self._get_pending(request_id)
        request.status = ApprovalStatus.APPROVED if approve else ApprovalStatus.DENIED
        request.token = secrets.token_urlsafe(18) if approve else None
        return request

    def consume(self, request_id: str, token: str, action: str, arguments: dict[str, object]) -> ApprovalRequest:
        request = self._requests.get(request_id)
        if request is None or request.status != ApprovalStatus.APPROVED:
            raise ValueError("Approval is not active.")
        if not secrets.compare_digest(request.token or "", token):
            raise ValueError("Approval token is invalid.")
        if request.action != action or request.argument_digest != _digest_arguments(arguments):
            raise ValueError("Approval scope does not match the proposed action.")
        request.status = ApprovalStatus.CONSUMED
        request.token = None
        return request

    def _get_pending(self, request_id: str) -> ApprovalRequest:
        request = self._requests.get(request_id)
        if request is None or request.status != ApprovalStatus.PENDING:
            raise ValueError("Approval request is not pending.")
        return request


def _digest_arguments(arguments: dict[str, object]) -> str:
    canonical = repr(sorted((str(key), repr(value)) for key, value in arguments.items()))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
