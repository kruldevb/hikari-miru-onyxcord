# miru.onyx - RadioGroup Component
"""RadioGroup component dataclass."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["RadioGroupOption", "RadioGroup"]


@dataclass
class RadioGroupOption:
    """Option for RadioGroup component.

    Attributes
    ----------
    value : str
        Option value (max 100 characters)
    label : str
        Option label text (max 100 characters)
    description : str | None
        Optional description text (max 100 characters)
    default : bool
        Whether this option is selected by default
    """

    value: str
    label: str
    description: str | None = None
    default: bool = False


@dataclass
class RadioGroup:
    """RadioGroup component (type 21) - single-choice selection.

    Attributes
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    options : list[RadioGroupOption]
        List of radio options (2-10 options)
    required : bool
        Whether the field is required (default True)
    id : int | None
        Optional component ID
    type : Literal[21]
        Component type (always 21)
    """

    custom_id: str
    options: list[RadioGroupOption]
    required: bool = True
    id: int | None = None
    type: Literal[21] = 21

    def __post_init__(self) -> None:
        if not 1 <= len(self.custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(self.custom_id)})")
        if not 2 <= len(self.options) <= 10:
            raise ValueError(f"RadioGroup must have 2-10 options (got {len(self.options)})")
