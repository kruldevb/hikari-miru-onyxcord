"""Response data for CheckboxGroup component."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["CheckboxGroupResponse"]


@dataclass
class CheckboxGroupResponse:
    """Response data for CheckboxGroup component.

    Attributes
    ----------
    id : int
        Component ID assigned by Discord
    custom_id : str
        Custom identifier for the component
    values : list[str]
        List of selected option values
    type : Literal[22]
        Component type (always 22)
    """

    id: int
    custom_id: str
    values: list[str]
    type: Literal[22] = 22
