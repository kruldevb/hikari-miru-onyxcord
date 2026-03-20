"""Fluent builder for Checkbox components."""

from typing import Self
from miru.onyx.components.checkbox import Checkbox

__all__ = ["CheckboxBuilder"]


class CheckboxBuilder:
    """Fluent builder for Checkbox components."""

    def __init__(self) -> None:
        self._custom_id: str | None = None
        self._default: bool = False
        self._id: int | None = None

    def set_custom_id(self, custom_id: str) -> Self:
        self._custom_id = custom_id
        return self

    def set_default(self, default: bool) -> Self:
        self._default = default
        return self

    def set_id(self, id: int) -> Self:
        self._id = id
        return self

    def build(self) -> Checkbox:
        if self._custom_id is None:
            raise ValueError("custom_id is required")
        return Checkbox(custom_id=self._custom_id, default=self._default, id=self._id)
