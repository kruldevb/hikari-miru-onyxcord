"""Miru integration for FileUpload component."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.components.file_upload import FileUpload

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxFileUpload"]


class OnyxFileUpload:
    """Miru ModalItem implementation for FileUpload component.

    Parameters
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    min_values : int
        Minimum number of files (0-10, default 1)
    max_values : int
        Maximum number of files (1-10, default 1)
    required : bool
        Whether the field is required (default True)
    row : int | None
        Row position in the modal
    """

    def __init__(
        self,
        *,
        custom_id: str,
        min_values: int = 1,
        max_values: int = 1,
        required: bool = True,
        row: int | None = None,
    ) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")
        if not 0 <= min_values <= 10:
            raise ValueError(f"min_values must be 0-10 (got {min_values})")
        if not 1 <= max_values <= 10:
            raise ValueError(f"max_values must be 1-10 (got {max_values})")
        if min_values > max_values:
            raise ValueError(f"min_values ({min_values}) cannot exceed max_values ({max_values})")

        self._custom_id = custom_id
        self.min_values = min_values
        self.max_values = max_values
        self.required = required
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.values: list[str] = []
        self.attachments: list[t.Any] = []

    @property
    def type(self) -> int:
        return 19

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def row(self) -> int | None:
        return self._row

    def _build(self, action_row: hikari.api.ModalActionRowBuilder) -> None:
        self._payload: dict[str, t.Any] = self.to_payload()

    async def _refresh_state(self, context: ModalContext) -> None:
        raw_value = context.values.get(self)  # type: ignore[arg-type]
        if raw_value is not None:
            if isinstance(raw_value, list):
                self.values = [str(v) for v in raw_value]
            elif isinstance(raw_value, str):
                self.values = [raw_value] if raw_value else []
            else:
                self.values = []
        else:
            self.values = []

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {
            "type": 19,
            "custom_id": self._custom_id,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "required": self.required,
        }
        if self._id is not None:
            payload["id"] = self._id
        return payload

    def to_component(self) -> FileUpload:
        return FileUpload(
            custom_id=self._custom_id,
            min_values=self.min_values,
            max_values=self.max_values,
            required=self.required,
            id=self._id,
        )
