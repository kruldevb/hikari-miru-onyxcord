# miru.onyx - CheckboxGroup Component
"""CheckboxGroup component dataclass."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["CheckboxGroupOption", "CheckboxGroup"]


@dataclass
class CheckboxGroupOption:
    """Option for CheckboxGroup component.

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
class CheckboxGroup:
    """CheckboxGroup component (type 22) - multi-selection.

    Attributes
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    options : list[CheckboxGroupOption]
        List of checkbox options (1-10 options)
    min_values : int
        Minimum number of selections (0-10, default 1)
    max_values : int | None
        Maximum number of selections (1-10, defaults to len(options))
    required : bool
        Whether the field is required (default True)
    id : int | None
        Optional component ID
    type : Literal[22]
        Component type (always 22)
    """

    custom_id: str
    options: list[CheckboxGroupOption]
    min_values: int = 1
    max_values: int | None = None
    required: bool = True
    id: int | None = None
    type: Literal[22] = 22

    def __post_init__(self) -> None:
        if not 1 <= len(self.custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(self.custom_id)})")
        if not 1 <= len(self.options) <= 10:
            raise ValueError(f"CheckboxGroup must have 1-10 options (got {len(self.options)})")
        if not 0 <= self.min_values <= 10:
            raise ValueError(f"min_values must be 0-10 (got {self.min_values})")
        if self.max_values is not None and not 1 <= self.max_values <= 10:
            raise ValueError(f"max_values must be 1-10 (got {self.max_values})")
        if self.min_values == 0 and self.required:
            raise ValueError("required must be False when min_values is 0")
