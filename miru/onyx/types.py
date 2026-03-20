# miru.onyx - Type Definitions
"""Type hints and TypedDicts for OnyxCord components."""

from typing import TYPE_CHECKING, Literal, TypedDict, Union

__all__ = [
    "LabelChildT",
    "LabelResponseChildT",
    "ModalTopLevelT",
    "LabelPayload",
    "FileUploadPayload",
    "RadioGroupOptionPayload",
    "RadioGroupPayload",
    "CheckboxGroupOptionPayload",
    "CheckboxGroupPayload",
    "CheckboxPayload",
]

if TYPE_CHECKING:
    from miru.onyx.components.checkbox import Checkbox
    from miru.onyx.components.checkbox_group import CheckboxGroup
    from miru.onyx.components.file_upload import FileUpload
    from miru.onyx.components.label import Label
    from miru.onyx.components.radio_group import RadioGroup
    from miru.onyx.responses.checkbox import CheckboxResponse
    from miru.onyx.responses.checkbox_group import CheckboxGroupResponse
    from miru.onyx.responses.file_upload import FileUploadResponse
    from miru.onyx.responses.label import LabelResponse
    from miru.onyx.responses.radio_group import RadioGroupResponse


# Valid child components for Label
LabelChildT = Union[
    "TextInput",
    "StringSelect",
    "UserSelect",
    "RoleSelect",
    "MentionableSelect",
    "ChannelSelect",
    "FileUpload",
    "RadioGroup",
    "CheckboxGroup",
    "Checkbox",
]

# Valid child components for Label responses
LabelResponseChildT = Union[
    "TextInputResponse",
    "StringSelectResponse",
    "UserSelectResponse",
    "RoleSelectResponse",
    "MentionableSelectResponse",
    "ChannelSelectResponse",
    "FileUploadResponse",
    "RadioGroupResponse",
    "CheckboxGroupResponse",
    "CheckboxResponse",
]

# Top-level modal components
ModalTopLevelT = Union["Label", "ActionRow"]


# TypedDict definitions for component payloads


class LabelPayload(TypedDict, total=False):
    """TypedDict for Label component payload."""

    type: Literal[18]
    id: int | None
    label: str
    description: str | None
    component: dict


class FileUploadPayload(TypedDict, total=False):
    """TypedDict for FileUpload component payload."""

    type: Literal[19]
    id: int | None
    custom_id: str
    min_values: int
    max_values: int
    required: bool


class RadioGroupOptionPayload(TypedDict, total=False):
    """TypedDict for RadioGroup option payload."""

    value: str
    label: str
    description: str | None
    default: bool


class RadioGroupPayload(TypedDict, total=False):
    """TypedDict for RadioGroup component payload."""

    type: Literal[21]
    id: int | None
    custom_id: str
    options: list[RadioGroupOptionPayload]
    required: bool


class CheckboxGroupOptionPayload(TypedDict, total=False):
    """TypedDict for CheckboxGroup option payload."""

    value: str
    label: str
    description: str | None
    default: bool


class CheckboxGroupPayload(TypedDict, total=False):
    """TypedDict for CheckboxGroup component payload."""

    type: Literal[22]
    id: int | None
    custom_id: str
    options: list[CheckboxGroupOptionPayload]
    min_values: int
    max_values: int | None
    required: bool


class CheckboxPayload(TypedDict, total=False):
    """TypedDict for Checkbox component payload."""

    type: Literal[23]
    id: int | None
    custom_id: str
    default: bool
