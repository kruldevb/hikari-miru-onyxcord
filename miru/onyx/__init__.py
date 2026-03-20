# miru.onyx — OnyxCord integration for hikari-miru
"""OnyxCord extends hikari-miru with support for new Discord modal components and Components v2 helpers."""

__version__ = "0.1.0"

# Enums
from miru.onyx.enums import OnyxComponentType

# Component dataclasses
from miru.onyx.components.checkbox import Checkbox
from miru.onyx.components.checkbox_group import CheckboxGroup, CheckboxGroupOption
from miru.onyx.components.file_upload import FileUpload
from miru.onyx.components.label import Label
from miru.onyx.components.radio_group import RadioGroup, RadioGroupOption

# Builders
from miru.onyx.builders import (
    CheckboxBuilder,
    CheckboxGroupBuilder,
    FileUploadBuilder,
    LabelBuilder,
    RadioGroupBuilder,
)

# Responses
from miru.onyx.responses import (
    CheckboxGroupResponse,
    CheckboxResponse,
    FileUploadResponse,
    LabelResponse,
    RadioGroupResponse,
)

# Parser
from miru.onyx.parser import (
    ComponentNotFoundError,
    InvalidComponentTypeError,
    ParseError,
    parse_modal_submit,
)

# Hikari integration
from miru.onyx.entity_factory import OnyxEntityFactory
from miru.onyx.bot import OnyxBot

# Miru modal items
from miru.onyx.items import (
    OnyxCheckbox,
    OnyxCheckboxGroup,
    OnyxChannelSelect,
    OnyxFileUpload,
    OnyxLabel,
    OnyxRadioGroup,
    OnyxRoleSelect,
    OnyxStringSelect,
    OnyxUserSelect,
    CheckboxGroupOption as ItemCheckboxGroupOption,
    RadioGroupOption as ItemRadioGroupOption,
    StringSelectOption,
)

# Modal system
from miru.onyx.modal import OnyxModal, OnyxModalRegistry, install_modal_handler

__all__ = [
    # Version
    "__version__",
    # Enums
    "OnyxComponentType",
    # Component dataclasses
    "Label",
    "FileUpload",
    "RadioGroup",
    "RadioGroupOption",
    "CheckboxGroup",
    "CheckboxGroupOption",
    "Checkbox",
    # Builders
    "LabelBuilder",
    "FileUploadBuilder",
    "RadioGroupBuilder",
    "CheckboxGroupBuilder",
    "CheckboxBuilder",
    # Responses
    "LabelResponse",
    "FileUploadResponse",
    "RadioGroupResponse",
    "CheckboxGroupResponse",
    "CheckboxResponse",
    # Parser
    "parse_modal_submit",
    "ParseError",
    "ComponentNotFoundError",
    "InvalidComponentTypeError",
    # Hikari integration
    "OnyxEntityFactory",
    "OnyxBot",
    # Miru modal items
    "OnyxCheckbox",
    "OnyxCheckboxGroup",
    "OnyxChannelSelect",
    "OnyxFileUpload",
    "OnyxLabel",
    "OnyxRadioGroup",
    "OnyxRoleSelect",
    "OnyxStringSelect",
    "OnyxUserSelect",
    "StringSelectOption",
    # Modal system
    "OnyxModal",
    "OnyxModalRegistry",
    "install_modal_handler",
]
