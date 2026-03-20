"""Response data for Label component."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from miru.onyx.types import LabelResponseChildT

__all__ = ["LabelResponse"]


@dataclass
class LabelResponse:
    """Response data for Label component.

    Attributes
    ----------
    id : int
        Component ID assigned by Discord
    component : LabelResponseChildT
        The child component response data
    type : Literal[18]
        Component type (always 18)
    """

    id: int
    component: "LabelResponseChildT"
    type: Literal[18] = 18
