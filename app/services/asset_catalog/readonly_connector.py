from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, cast

from app.services.asset_catalog.contracts import SOURCE_VIEWS, SourceView
from app.services.asset_catalog.readonly_preflight import (
    AssetCatalogReadonlyPreflightResult,
    AssetCatalogReadonlyPreflightValidator,
)

DB4B_READONLY_MAX_SAMPLE_LIMIT = 30
DB4B_READONLY_SAMPLE_MODES = ("structure_only", "limit")


class AssetCatalogReadonlyConnectorShell:
    """Disabled-by-default DB-4B shell for readonly View smoke tests.

    The shell intentionally depends only on a DB-API-shaped connection factory.
    It does not import or create any real database client.
    """

    def __init__(
        self,
        *,
        enabled: bool,
        connection_factory: Callable[[], Any] | None = None,
        sample_mode: str = "structure_only",
        sample_limit: int = DB4B_READONLY_MAX_SAMPLE_LIMIT,
        validator: AssetCatalogReadonlyPreflightValidator | None = None,
    ) -> None:
        self.enabled = enabled
        self.connection_factory = connection_factory
        self.sample_mode = sample_mode
        self.sample_limit = sample_limit
        self.validator = validator or AssetCatalogReadonlyPreflightValidator()
        self._validate_policy()

    def build_view_queries(self) -> dict[SourceView, str]:
        return {source_view: self.build_view_query(source_view) for source_view in SOURCE_VIEWS}

    def build_view_query(self, source_view: str) -> str:
        validated_view = self._validate_source_view(source_view)
        if self.sample_mode == "structure_only":
            return f"SELECT * FROM {validated_view} WHERE 1 = 0"
        return f"SELECT * FROM {validated_view} LIMIT {self.sample_limit}"

    def load_rows_by_view(self) -> dict[SourceView, list[dict[str, Any]]]:
        if not self.enabled:
            raise ValueError("readonly connector disabled")
        if self.connection_factory is None:
            raise ValueError("readonly connector requires a connection factory")

        connection = self.connection_factory()
        rows_by_view: dict[SourceView, list[dict[str, Any]]] = {}
        for source_view, sql in self.build_view_queries().items():
            rows_by_view[source_view] = self._execute_select(connection, sql)
        return rows_by_view

    def run_preflight(self) -> AssetCatalogReadonlyPreflightResult:
        return self.validator.validate(self.load_rows_by_view())

    def _execute_select(self, connection: Any, sql: str) -> list[dict[str, Any]]:
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            return self._rows_from_cursor(cursor)
        finally:
            close = getattr(cursor, "close", None)
            if callable(close):
                close()

    def _rows_from_cursor(self, cursor: Any) -> list[dict[str, Any]]:
        description: Sequence[Sequence[Any]] = cursor.description or ()
        columns = tuple(str(column[0]) for column in description)
        return [
            dict(zip(columns, row, strict=True))
            for row in cursor.fetchall()
        ]

    def _validate_policy(self) -> None:
        if self.sample_mode not in DB4B_READONLY_SAMPLE_MODES:
            raise ValueError("unsupported readonly sample mode")
        if not 1 <= self.sample_limit <= DB4B_READONLY_MAX_SAMPLE_LIMIT:
            raise ValueError("readonly sample limit must be between 1 and 30")

    def _validate_source_view(self, source_view: str) -> SourceView:
        if source_view not in SOURCE_VIEWS:
            raise ValueError("unsupported source view")
        return cast(SourceView, source_view)
