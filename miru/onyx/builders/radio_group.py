"""Fluent builder for RadioGroup components."""

from typing import Self
from miru.onyx.components.radio_group import RadioGroup, RadioGroupOption

__all__ = ["RadioGroupBuilder"]


class RadioGroupBuilder:
    """Fluent builder for RadioGroup components."""

    def __init__(self) -> None:
        self._custom_id: str | None = None
        self._options: list[RadioGroupOption] = []
        self._required: bool = True
        self._id: int | None = None

    def set_custom_id(self, custom_id: str) -> Self:
        self._custom_id = custom_id
        return self

    def add_option(self, value: str, label: str, description: str | None = None, default: bool = False) -> Self:
        self._options.append(RadioGroupOption(value=value, label=label, description=description, default=default))
        return self

    def set_required(self, required: bool) -> Self:
        self._required = required
        return self

    def set_id(self, id: int) -> Self:
        self._id = id
        return self

    def build(self) -> RadioGroup:
        if self._custom_id is None:
            raise ValueError("custom_id is required")
        if len(self._options) < 2:
            raise ValueError("At least 2 options are required")
        return RadioGroup(
            custom_id=self._custom_id,
            options=self._options,
            required=self._required,
            id=self._id,
        )
