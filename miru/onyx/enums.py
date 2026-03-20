# miru.onyx - Component Type Enums
"""Enums for OnyxCord component types."""

from enum import IntEnum

__all__ = ["OnyxComponentType"]


class OnyxComponentType(IntEnum):
    """Component types for OnyxCord components.

    These component types extend the Discord API component types
    to support new modal components.
    """

    LABEL = 18
    FILE_UPLOAD = 19
    RADIO_GROUP = 21
    CHECKBOX_GROUP = 22
    CHECKBOX = 23
