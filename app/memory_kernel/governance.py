from app.memory_kernel.contracts import GovernanceDecision, MemoryKernelRequest


class MemoryGovernance:
    """Applies kernel-level governance before retrieval and context construction."""

    def authorize(self, request: MemoryKernelRequest) -> GovernanceDecision:
        filters = request.filters.model_copy(deep=True)
        if filters.is_latest is None:
            filters.is_latest = True
        return GovernanceDecision(
            allowed=True,
            filters=filters,
            reason="Phase 1 governance enforces latest-version filtering; full RBAC/ABAC is TODO.",
        )

