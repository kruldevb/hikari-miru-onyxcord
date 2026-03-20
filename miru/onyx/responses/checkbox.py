"""Response data for Checkbox component."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["CheckboxResponse"]


@dataclass
class CheckboxResponse:
    """Response data for Checkbox component.

    Attributes
    ----------
    id : int
        Component ID assigned by Discord
    custom_id : str
        Custom identifier for the component
    value : bool
        True if checked, False if unchecked
    type : Literal[23]
        Component type (always 23)
    """

    id: int
    custom_id: str
    value: bool
    type: Literal[23] = 23
