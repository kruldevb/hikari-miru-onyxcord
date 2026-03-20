"""Response data for RadioGroup component."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["RadioGroupResponse"]


@dataclass
class RadioGroupResponse:
    """Response data for RadioGroup component.

    Attributes
    ----------
    id : int
        Component ID assigned by Discord
    custom_id : str
        Custom identifier for the component
    value : str | None
        Selected option value or None
    type : Literal[21]
        Component type (always 21)
    """

    id: int
    custom_id: str
    value: str | None
    type: Literal[21] = 21
