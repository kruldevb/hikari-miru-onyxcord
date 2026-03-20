"""Miru integration for Channel Select component in modals."""

from __future__ import annotations

import typing as t

import hikari

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxChannelSelect"]


class OnyxChannelSelect:
    """Miru ModalItem implementation for Channel Select component."""

    def __init__(
        self,
        *,
        custom_id: str,
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        channel_types: list[hikari.ChannelType] | None = None,
        required: bool = True,
        row: int | None = None,
    ) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")

        self._custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.channel_types = channel_types
        self.required = required
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.values: list[hikari.Snowflake] = []

    @property
    def type(self) -> int:
        return 8

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
                self.values = [hikari.Snowflake(v) for v in raw_value]
            else:
                self.values = [hikari.Snowflake(raw_value)]
        else:
            self.values = []

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {"type": 8, "custom_id": self._custom_id}
        if self.placeholder:
            payload["placeholder"] = self.placeholder
        if self.min_values != 1:
            payload["min_values"] = self.min_values
        if self.max_values != 1:
            payload["max_values"] = self.max_values
        if self.channel_types:
            payload["channel_types"] = [int(ct) for ct in self.channel_types]
        if not self.required:
            payload["required"] = False
        if self._id is not None:
            payload["id"] = self._id
        return payload
