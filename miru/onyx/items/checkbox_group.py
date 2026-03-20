"""Miru integration for CheckboxGroup component."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.components.checkbox_group import CheckboxGroup, CheckboxGroupOption

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxCheckboxGroup"]


class OnyxCheckboxGroup:
    """Miru ModalItem implementation for CheckboxGroup component.

    Parameters
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    options : list[CheckboxGroupOption]
        List of checkbox options (1-10 options)
    min_values : int
        Minimum number of selections (0-10, default 1)
    max_values : int | None
        Maximum number of selections (1-10, defaults to len(options))
    required : bool
        Whether the field is required (default True)
    row : int | None
        Row position in the modal
    """

    def __init__(
        self,
        *,
        custom_id: str,
        options: list[CheckboxGroupOption],
        min_values: int = 1,
        max_values: int | None = None,
        required: bool = True,
        row: int | None = None,
    ) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")
        if not 1 <= len(options) <= 10:
            raise ValueError(f"CheckboxGroup must have 1-10 options (got {len(options)})")
        if not 0 <= min_values <= 10:
            raise ValueError(f"min_values must be 0-10 (got {min_values})")
        if max_values is not None and not 1 <= max_values <= 10:
            raise ValueError(f"max_values must be 1-10 (got {max_values})")
        if min_values == 0 and required:
            raise ValueError("required must be False when min_values is 0")

        self._custom_id = custom_id
        self.options = options
        self.min_values = min_values
        self.max_values = max_values
        self.required = required
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.values: list[str] = []

    @property
    def type(self) -> int:
        return 22

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
            "type": 22,
            "custom_id": self._custom_id,
            "required": self.required,
            "min_values": self.min_values,
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
        if self.max_values is not None:
            payload["max_values"] = self.max_values
        if self._id is not None:
            payload["id"] = self._id
        return payload

    def to_component(self) -> CheckboxGroup:
        return CheckboxGroup(
            custom_id=self._custom_id,
            options=self.options,
            min_values=self.min_values,
            max_values=self.max_values,
            required=self.required,
            id=self._id,
        )
