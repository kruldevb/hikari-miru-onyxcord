# miru.onyx - FileUpload Component
"""FileUpload component dataclass."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["FileUpload"]


@dataclass
class FileUpload:
    """FileUpload component (type 19) - allows file uploads in modals.

    Attributes
    ----------
    custom_id : str
        Custom identifier (1-100 characters)
    min_values : int
        Minimum number of files (0-10, default 1)
    max_values : int
        Maximum number of files (1-10, default 1)
    required : bool
        Whether the field is required (default True)
    id : int | None
        Optional component ID
    type : Literal[19]
        Component type (always 19)
    """

    custom_id: str
    min_values: int = 1
    max_values: int = 1
    required: bool = True
    id: int | None = None
    type: Literal[19] = 19

    def __post_init__(self) -> None:
        if not 1 <= len(self.custom_id) <= 100:
            raise ValueError(f"custom_id must be 1-100 characters (got {len(self.custom_id)})")
        if not 0 <= self.min_values <= 10:
            raise ValueError(f"min_values must be 0-10 (got {self.min_values})")
        if not 1 <= self.max_values <= 10:
            raise ValueError(f"max_values must be 1-10 (got {self.max_values})")
        if self.min_values > self.max_values:
            raise ValueError(f"min_values ({self.min_values}) cannot exceed max_values ({self.max_values})")
