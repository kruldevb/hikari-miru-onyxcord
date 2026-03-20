"""Fluent builder for Label components."""

from typing import Any, Self
from miru.onyx.components.label import Label

__all__ = ["LabelBuilder"]


class LabelBuilder:
    """Fluent builder for Label components."""

    def __init__(self) -> None:
        self._label: str | None = None
        self._description: str | None = None
        self._component: Any | None = None
        self._id: int | None = None

    def set_label(self, label: str) -> Self:
        if len(label) > 45:
            raise ValueError(f"Label text must be 45 characters or less (got {len(label)})")
        self._label = label
        return self

    def set_description(self, description: str) -> Self:
        if len(description) > 100:
            raise ValueError(f"Description must be 100 characters or less (got {len(description)})")
        self._description = description
        return self

    def set_component(self, component: Any) -> Self:
        self._component = component
        return self

    def set_id(self, id: int) -> Self:
        self._id = id
        return self

    def build(self) -> Label:
        if self._label is None:
            raise ValueError("Label text is required")
        if self._component is None:
            raise ValueError("Child component is required")
        return Label(
            label=self._label,
            component=self._component,
            description=self._description,
            id=self._id,
        )
