"""
Modal field builders for OnyxCord.

This module provides a clean, declarative API for building modals with the new Discord components.
Instead of creating multiple variables, you can define everything in a single ModalBuilder.
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    import hikari
    from miru.text_input import TextInput
    from .items.file_upload import FileUpload
    from .items.radio_group import RadioGroup
    from .items.checkbox_group import CheckboxGroup
    from .items.checkbox import Checkbox
    from .items.label import Label

__all__ = [
    "ModalBuilder",
    "Text",
    "File",
    "Radio",
    "CheckboxGroupField",
    "CheckboxField",
    "ModalData",
]


@dataclass
class ModalData:
    """Container for modal response data."""
    pass


class BaseField:
    """Base class for modal fields."""
    
    def __init__(self, custom_id: str):
        self.custom_id = custom_id
    
    def build(self) -> t.Any:
        """Build the actual component."""
        raise NotImplementedError
    
    def extract_value(self, component: t.Any) -> t.Any:
        """Extract value from the component after submission."""
        if hasattr(component, "value"):
            return component.value
        elif hasattr(component, "values"):
            return component.values
        elif hasattr(component, "attachments"):
            return component.attachments
        return None


class Text(BaseField):
    """Text input field.
    
    Args:
        label: Display label for the input
        custom_id: Unique identifier
        placeholder: Placeholder text
        required: Whether the field is required
        min_length: Minimum text length
        max_length: Maximum text length
        style: Text input style (SHORT or PARAGRAPH)
    """
    
    def __init__(
        self,
        label: str,
        custom_id: str,
        placeholder: str | None = None,
        required: bool = False,
        min_length: int | None = None,
        max_length: int | None = None,
        style: hikari.TextInputStyle = None,
    ):
        super().__init__(custom_id)
        self.label = label
        self.placeholder = placeholder
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.style = style
    
    def build(self) -> TextInput:
        from miru.text_input import TextInput
        
        kwargs = {
            "label": self.label,
            "custom_id": self.custom_id,
            "required": self.required,
        }
        
        if self.placeholder:
            kwargs["placeholder"] = self.placeholder
        if self.min_length is not None:
            kwargs["min_length"] = self.min_length
        if self.max_length is not None:
            kwargs["max_length"] = self.max_length
        if self.style is not None:
            kwargs["style"] = self.style
        
        return TextInput(**kwargs)


class File(BaseField):
    """File upload field.
    
    Args:
        custom_id: Unique identifier
        label: Display label
        max: Maximum number of files
        required: Whether the field is required
        file_types: Allowed file types (e.g., ["image/*", ".pdf"])
    """
    
    def __init__(
        self,
        custom_id: str,
        label: str = "Upload File",
        max: int = 1,
        required: bool = False,
        file_types: list[str] | None = None,
    ):
        super().__init__(custom_id)
        self.label = label
        self.max = max
        self.required = required
        self.file_types = file_types
    
    def build(self) -> FileUpload:
        from .items.file_upload import FileUpload
        
        return FileUpload(
            custom_id=self.custom_id,
            label=self.label,
            max_values=self.max,
            required=self.required,
            file_types=self.file_types or [],
        )


class Radio(BaseField):
    """Radio group field (single choice).
    
    Args:
        custom_id: Unique identifier
        label: Display label
        options: List of (label, value) tuples
        required: Whether the field is required
    """
    
    def __init__(
        self,
        custom_id: str,
        label: str = "Select Option",
        options: list[tuple[str, str]] | None = None,
        required: bool = False,
    ):
        super().__init__(custom_id)
        self.label = label
        self.options = options or []
        self.required = required
    
    def build(self) -> RadioGroup:
        from .items.radio_group import RadioGroup, RadioGroupOption
        
        return RadioGroup(
            custom_id=self.custom_id,
            label=self.label,
            options=[
                RadioGroupOption(label=label, value=value)
                for label, value in self.options
            ],
            required=self.required,
        )


class CheckboxGroupField(BaseField):
    """Checkbox group field (multiple choice).
    
    Args:
        custom_id: Unique identifier
        label: Display label
        options: List of (label, value) tuples
        required: Whether the field is required
    """
    
    def __init__(
        self,
        custom_id: str,
        label: str = "Select Options",
        options: list[tuple[str, str]] | None = None,
        required: bool = False,
    ):
        super().__init__(custom_id)
        self.label = label
        self.options = options or []
        self.required = required
    
    def build(self) -> CheckboxGroup:
        from .items.checkbox_group import CheckboxGroup, CheckboxGroupOption
        
        return CheckboxGroup(
            custom_id=self.custom_id,
            label=self.label,
            options=[
                CheckboxGroupOption(label=label, value=value)
                for label, value in self.options
            ],
            required=self.required,
        )


class CheckboxField(BaseField):
    """Single checkbox field.
    
    Args:
        custom_id: Unique identifier
        label: Display label
        required: Whether the field is required
    """
    
    def __init__(
        self,
        custom_id: str,
        label: str = "Checkbox",
        required: bool = False,
    ):
        super().__init__(custom_id)
        self.label = label
        self.required = required
    
    def build(self) -> Checkbox:
        from .items.checkbox import Checkbox
        
        return Checkbox(
            custom_id=self.custom_id,
            label=self.label,
            required=self.required,
        )


class ModalBuilder:
    """Builder for creating modals with a clean, declarative API.
    
    Example:
        ```python
        class MyModal(OnyxModal, title="Form"):
            modal = ModalBuilder(
                Text(
                    label="Name",
                    custom_id="name",
                    placeholder="Enter your name...",
                    required=True,
                ),
                File(
                    custom_id="files",
                    max=2
                ),
                Radio(
                    custom_id="priority",
                    options=[
                        ("Low", "low"),
                        ("Medium", "medium"),
                        ("High", "high"),
                    ],
                ),
            )
            
            async def callback(self, ctx):
                data = self.modal.get(self)
                await ctx.respond(f"Name: {data.name}")
        ```
    """
    
    def __init__(self, *fields: BaseField):
        """Initialize the modal builder with fields.
        
        Args:
            *fields: Variable number of field definitions
        """
        self.fields = fields
    
    def build(self, modal: t.Any) -> None:
        """Build all fields and add them to the modal.
        
        Args:
            modal: The modal instance to add fields to
        """
        for field in self.fields:
            item = field.build()
            setattr(modal, field.custom_id, item)
            modal.add_item(item)
    
    def get(self, modal: t.Any) -> ModalData:
        """Extract all values from the modal after submission.
        
        Args:
            modal: The modal instance with submitted values
            
        Returns:
            ModalData object with all field values as attributes
        """
        data = ModalData()
        
        for field in self.fields:
            component = getattr(modal, field.custom_id, None)
            if component is not None:
                value = field.extract_value(component)
                setattr(data, field.custom_id, value)
        
        return data
