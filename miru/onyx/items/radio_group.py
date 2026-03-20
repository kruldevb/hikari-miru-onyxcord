"""Miru integration for RadioGroup component."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.components.radio_group import RadioGroup, RadioGroupOption

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxRadioGroup"]


class OnyxRadioGroup:
    """Miru ModalItem implementation for RadioGroup component.

    Parameters
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    options : list[RadioGroupOption]
        List of radio options (2-10 options)
    required : bool
        Whether the field is required (default True)
    row : int | None
        Row position in the modal
    """

    def __init__(
        self,
        *,
        custom_id: str,
        options: list[RadioGroupOption],
        required: bool = True,
        row: int | None = None,
    ) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")
        if not 2 <= len(options) <= 10:
            raise ValueError(f"RadioGroup must have 2-10 options (got {len(options)})")

        self._custom_id = custom_id
        self.options = options
        self.required = required
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.value: str | None = None

    @property
    def type(self) -> int:
        return 21

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def row(self) -> int | None:
        return self._row

    def _build(self, action_row: hikari.api.ModalActionRowBuilder) -> None:
        self._payload: dict[str, t.Any] = {
            "type": 21,
            "custom_id": self._custom_id,
            "required": self.required,
            "options": [
                {
                    "value": opt.value,
                    "label": opt.label,
                    **({
                        "description": opt.description} if opt.description is not None else {}),
                    **({"default": opt.default} if opt.default else {}),
                }
                for opt in self.options
            ],
        }

    async def _refresh_state(self, context: ModalContext) -> None:
        raw_value = context.values.get(self)  # type: ignore[arg-type]
        if raw_value is not None:
            self.value = str(raw_value)

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {
            "type": 21,
            "custom_id": self._custom_id,
            "required": self.required,
            "options": [
                {
                    "value": opt.value,
                    "label": opt.label,
                    **({
                        "description": opt.description} if opt.description is not None else {}),
                    **({"default": opt.default} if opt.default else {}),
                }
                for opt in self.options
            ],
        }
        if self._id is not None:
            payload["id"] = self._id
        return payload

    def to_component(self) -> RadioGroup:
        return RadioGroup(
            custom_id=self._custom_id,
            options=self.options,
            required=self.required,
            id=self._id,
        )
