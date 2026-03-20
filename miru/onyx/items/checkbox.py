"""Miru integration for Checkbox component."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.components.checkbox import Checkbox

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxCheckbox"]


class OnyxCheckbox:
    """Miru ModalItem implementation for Checkbox component.

    Parameters
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    default : bool
        Whether the checkbox is checked by default
    row : int | None
        Row position in the modal
    """

    def __init__(self, *, custom_id: str, default: bool = False, row: int | None = None) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")
        self._custom_id = custom_id
        self.default = default
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.value: bool = default

    @property
    def type(self) -> int:
        return 23

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
            if isinstance(raw_value, bool):
                self.value = raw_value
            elif isinstance(raw_value, str):
                self.value = raw_value.lower() in ("true", "1", "yes")
            else:
                self.value = bool(raw_value)
        else:
            self.value = self.default

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {"type": 23, "custom_id": self._custom_id}
        if self.default:
            payload["default"] = self.default
        if self._id is not None:
            payload["id"] = self._id
        return payload

    def to_component(self) -> Checkbox:
        return Checkbox(custom_id=self._custom_id, default=self.default, id=self._id)
