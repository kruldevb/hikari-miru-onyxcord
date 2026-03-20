# miru.onyx - Label Component
"""Label component dataclass."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from miru.onyx.types import LabelChildT

__all__ = ["Label"]


@dataclass
class Label:
    """Label component (type 18) - wraps modal components with text.

    Attributes
    ----------
    label : str
        Label text (max 45 characters)
    component : Any
        Child component to wrap
    description : str | None
        Optional description text (max 100 characters)
    id : int | None
        Optional component ID
    type : Literal[18]
        Component type (always 18)
    """

    label: str
    component: Any  # LabelChildT - using Any to avoid circular import
    description: str | None = None
    id: int | None = None
    type: Literal[18] = 18

    def __post_init__(self) -> None:
        if len(self.label) > 45:
            raise ValueError(f"Label text must be 45 characters or less (got {len(self.label)})")
        if self.description is not None and len(self.description) > 100:
            raise ValueError(f"Description must be 100 characters or less (got {len(self.description)})")
