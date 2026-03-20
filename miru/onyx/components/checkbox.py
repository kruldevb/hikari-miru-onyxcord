# miru.onyx - Checkbox Component
"""Checkbox component dataclass."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["Checkbox"]


@dataclass
class Checkbox:
    """Checkbox component (type 23) - single yes/no choice.

    Attributes
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    default : bool
        Whether the checkbox is checked by default
    id : int | None
        Optional component ID
    type : Literal[23]
        Component type (always 23)
    """

    custom_id: str
    default: bool = False
    id: int | None = None
    type: Literal[23] = 23

    def __post_init__(self) -> None:
        if not 1 <= len(self.custom_id) <= 100:
            raise ValueError(
                f"custom_id must be 1-100 characters (got {len(self.custom_id)})"
            )
