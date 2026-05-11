from __future__ import annotations

from dataclasses import dataclass

from app.services.asset_catalog.contracts import SourceView
from app.services.asset_catalog.readonly_connector import AssetCatalogReadonlyConnectorShell
from app.services.asset_catalog.readonly_preflight import (
    DB4A_REQUIRED_VIEW_FIELDS,
    AssetCatalogReadonlyPreflightResult,
)


@dataclass(frozen=True)
class AssetCatalogReadonlyLiveSmokeFinding:
    source_view: str
    code: str
    message: str
    field: str | None = None
    severity: str = "error"


@dataclass(frozen=True)
class AssetCatalogReadonlyLiveSmokeResult:
    sample_mode: str
    real_sample_data_used: bool
    mainline_agent_updated: bool
    column_names_by_view: dict[SourceView, tuple[str, ...]]
    findings: tuple[AssetCatalogReadonlyLiveSmokeFinding, ...]
    preflight: AssetCatalogReadonlyPreflightResult
    writes_db: bool = False
    writes_documents: bool = False
    writes_chunks: bool = False
    writes_opensearch: bool = False
    writes_qdrant: bool = False


class AssetCatalogReadonlyLiveSmokeRunner:
    """DB-4C live-smoke guard around the readonly connector shell."""

    def __init__(
        self,
        *,
        enabled: bool,
        connector: AssetCatalogReadonlyConnectorShell,
        mainline_agent_updated: bool = False,
        allow_real_sample_data: bool = False,
    ) -> None:
        self.enabled = enabled
        self.connector = connector
        self.mainline_agent_updated = mainline_agent_updated
        self.allow_real_sample_data = allow_real_sample_data

    def run(self) -> AssetCatalogReadonlyLiveSmokeResult:
        if not self.enabled:
            raise ValueError("readonly live smoke disabled")
        if self._uses_real_sample_data() and not (
            self.mainline_agent_updated and self.allow_real_sample_data
        ):
            raise ValueError(
                "real sample data requires mainline enterprise agent update "
                "and explicit authorization"
            )

        column_names_by_view = self.connector.load_column_names_by_view()
        findings = self._validate_columns(column_names_by_view)
        preflight = self.connector.run_preflight()
        return AssetCatalogReadonlyLiveSmokeResult(
            sample_mode=self.connector.sample_mode,
            real_sample_data_used=self._uses_real_sample_data(),
            mainline_agent_updated=self.mainline_agent_updated,
            column_names_by_view=column_names_by_view,
            findings=findings,
            preflight=preflight,
        )

    def _uses_real_sample_data(self) -> bool:
        return self.connector.sample_mode == "limit"

    def _validate_columns(
        self,
        column_names_by_view: dict[SourceView, tuple[str, ...]],
    ) -> tuple[AssetCatalogReadonlyLiveSmokeFinding, ...]:
        findings: list[AssetCatalogReadonlyLiveSmokeFinding] = []
        for source_view, required_fields in DB4A_REQUIRED_VIEW_FIELDS.items():
            available_fields = set(column_names_by_view.get(source_view, ()))
            for field in required_fields:
                if field not in available_fields:
                    findings.append(
                        AssetCatalogReadonlyLiveSmokeFinding(
                            source_view=source_view,
                            code="missing_required_column",
                            field=field,
                            message=f"{source_view} is missing required column {field}",
                        )
                    )
        return tuple(findings)
