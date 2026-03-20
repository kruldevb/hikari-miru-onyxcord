"""Miru integration for String Select component in modals."""

from __future__ import annotations

import typing as t

import hikari

if t.TYPE_CHECKING:
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxStringSelect", "StringSelectOption"]


class StringSelectOption:
    """Option for String Select component.

    Parameters
    ----------
    label : str
        User-facing name of the option (max 100 characters)
    value : str
        Developer-defined value (max 100 characters)
    description : str | None
        Additional description (max 100 characters)
    emoji : str | None
        Emoji for the option
    default : bool
        Whether this option is selected by default
    """

    def __init__(
        self,
        *,
        label: str,
        value: str,
        description: str | None = None,
        emoji: str | None = None,
        default: bool = False,
    ) -> None:
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {"label": self.label, "value": self.value}
        if self.description:
            payload["description"] = self.description
        if self.emoji:
            payload["emoji"] = {"name": self.emoji}
        if self.default:
            payload["default"] = self.default
        return payload


class OnyxStringSelect:
    """Miru ModalItem implementation for String Select component.

    Parameters
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    options : list[StringSelectOption]
        List of options (max 25)
    placeholder : str | None
        Placeholder text (max 150 characters)
    min_values : int
        Minimum number of selections (default 1)
    max_values : int
        Maximum number of selections (default 1)
    required : bool
        Whether this field is required (default True)
    row : int | None
        Row position in the modal
    """

    def __init__(
        self,
        *,
        custom_id: str,
        options: list[StringSelectOption],
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        required: bool = True,
        row: int | None = None,
    ) -> None:
        if not 1 <= len(custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(custom_id)})")
        if not options:
            raise ValueError("options list cannot be empty")
        if len(options) > 25:
            raise ValueError(f"options list cannot exceed 25 items (got {len(options)})")

        self._custom_id = custom_id
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.required = required
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None
        self.values: list[str] = []

    @property
    def type(self) -> int:
        return 3

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
                self.values = raw_value
            else:
                self.values = [str(raw_value)]
        else:
            self.values = []

    def to_payload(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {
            "type": 3,
            "custom_id": self._custom_id,
            "options": [opt.to_payload() for opt in self.options],
        }
        if self.placeholder:
            payload["placeholder"] = self.placeholder
        if self.min_values != 1:
            payload["min_values"] = self.min_values
        if self.max_values != 1:
            payload["max_values"] = self.max_values
        if not self.required:
            payload["required"] = False
        if self._id is not None:
            payload["id"] = self._id
        return payload
