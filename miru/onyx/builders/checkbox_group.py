"""Fluent builder for CheckboxGroup components."""

from typing import Self
from miru.onyx.components.checkbox_group import CheckboxGroup, CheckboxGroupOption

__all__ = ["CheckboxGroupBuilder"]


class CheckboxGroupBuilder:
    """Fluent builder for CheckboxGroup components."""

    def __init__(self) -> None:
        self._custom_id: str | None = None
        self._options: list[CheckboxGroupOption] = []
        self._min_values: int = 1
        self._max_values: int | None = None
        self._required: bool = True
        self._id: int | None = None

    def set_custom_id(self, custom_id: str) -> Self:
        self._custom_id = custom_id
        return self

    def add_option(self, value: str, label: str, description: str | None = None, default: bool = False) -> Self:
        self._options.append(CheckboxGroupOption(value=value, label=label, description=description, default=default))
        return self

    def set_min_values(self, min_values: int) -> Self:
        self._min_values = min_values
        return self

    def set_max_values(self, max_values: int) -> Self:
        self._max_values = max_values
        return self

    def set_required(self, required: bool) -> Self:
        self._required = required
        return self

    def set_id(self, id: int) -> Self:
        self._id = id
        return self

    def build(self) -> CheckboxGroup:
        if self._custom_id is None:
            raise ValueError("custom_id is required")
        if not self._options:
            raise ValueError("At least one option is required")
        return CheckboxGroup(
            custom_id=self._custom_id,
            options=self._options,
            min_values=self._min_values,
            max_values=self._max_values,
            required=self._required,
            id=self._id,
        )
