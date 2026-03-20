"""Parser for Discord modal submit payloads."""

from typing import Any

from miru.onyx.responses import (
    CheckboxGroupResponse,
    CheckboxResponse,
    FileUploadResponse,
    LabelResponse,
    RadioGroupResponse,
)

__all__ = ["parse_modal_submit", "ParseError", "ComponentNotFoundError", "InvalidComponentTypeError"]


class ParseError(Exception):
    """Raised when modal submit parsing fails."""
    pass


class ComponentNotFoundError(ParseError):
    """Raised when a component is not found in the modal submit."""
    pass


class InvalidComponentTypeError(ParseError):
    """Raised when a component has an invalid type."""
    pass


def parse_modal_submit(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse a Discord modal submit payload into typed response objects.

    Parameters
    ----------
    payload : dict[str, Any]
        The raw modal submit payload from Discord

    Returns
    -------
    dict[str, Any]
        Dictionary mapping custom_ids to response objects
    """
    if not isinstance(payload, dict):
        raise ParseError("Payload must be a dictionary")

    components = payload.get("components", [])
    if not isinstance(components, list):
        raise ParseError("Components must be a list")

    resolved = payload.get("resolved", {})
    responses: dict[str, Any] = {}

    for item in components:
        if not isinstance(item, dict):
            continue

        item_type = item.get("type")

        # Handle ActionRow (type 1)
        if item_type == 1:
            row_components = item.get("components", [])
            if not isinstance(row_components, list):
                continue

            for component in row_components:
                if not isinstance(component, dict):
                    continue
                component_type = component.get("type")
                if component_type is None:
                    continue
                try:
                    response = _parse_component(component, resolved)
                    if response:
                        custom_id = component.get("custom_id")
                        if custom_id:
                            responses[custom_id] = response
                except (KeyError, ValueError, TypeError) as e:
                    raise ParseError(f"Failed to parse component: {e}") from e

        # Handle top-level components (Label, etc.)
        else:
            try:
                response = _parse_component(item, resolved)
                if response:
                    if item_type == 18 and hasattr(response, 'component'):
                        child = response.component
                        if hasattr(child, 'custom_id'):
                            responses[child.custom_id] = child
                    else:
                        custom_id = item.get("custom_id")
                        if custom_id:
                            responses[custom_id] = response
            except (KeyError, ValueError, TypeError) as e:
                raise ParseError(f"Failed to parse component: {e}") from e

    return responses


def _parse_component(component: dict[str, Any], resolved: dict[str, Any] | None = None) -> Any:
    """Parse a single component into a response object."""
    if resolved is None:
        resolved = {}

    component_type = component.get("type")

    if component_type == 18:  # Label
        return _parse_label(component, resolved)
    elif component_type == 19:  # FileUpload
        return _parse_file_upload(component, resolved)
    elif component_type == 21:  # RadioGroup
        return _parse_radio_group(component)
    elif component_type == 22:  # CheckboxGroup
        return _parse_checkbox_group(component)
    elif component_type == 23:  # Checkbox
        return _parse_checkbox(component)
    elif component_type in (3, 5, 6, 7, 8):  # Select menus
        return _parse_select_menu(component)
    elif component_type == 4:  # TextInput
        return _parse_text_input(component)
    else:
        return None


def _parse_label(component: dict[str, Any], resolved: dict[str, Any]) -> LabelResponse:
    """Parse a Label component."""
    component_id = component.get("id")
    if component_id is None:
        raise ParseError("Label component missing id")

    child_component = component.get("component")
    if not child_component:
        raise ParseError("Label component missing child component")

    child_response = _parse_component(child_component, resolved)
    return LabelResponse(id=component_id, component=child_response)


def _parse_file_upload(component: dict[str, Any], resolved: dict[str, Any]) -> FileUploadResponse:
    """Parse a FileUpload component."""
    from miru.onyx.responses.file_upload import AttachmentData

    component_id = component.get("id")
    if component_id is None:
        raise ParseError("FileUpload component missing id")

    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("FileUpload component missing custom_id")

    values = component.get("values", [])
    if not isinstance(values, list):
        raise ParseError("FileUpload values must be a list")

    attachments = []
    resolved_attachments = resolved.get("attachments", {})
    for attachment_id in values:
        attachment_data = resolved_attachments.get(attachment_id)
        if attachment_data:
            attachments.append(AttachmentData(
                id=attachment_id,
                filename=attachment_data.get("filename", "unknown"),
                size=attachment_data.get("size", 0),
                url=attachment_data.get("url", ""),
                proxy_url=attachment_data.get("proxy_url", ""),
                content_type=attachment_data.get("content_type"),
            ))

    return FileUploadResponse(id=component_id, custom_id=custom_id, values=values, attachments=attachments)


def _parse_radio_group(component: dict[str, Any]) -> RadioGroupResponse:
    """Parse a RadioGroup component."""
    component_id = component.get("id")
    if component_id is None:
        raise ParseError("RadioGroup component missing id")
    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("RadioGroup component missing custom_id")
    value = component.get("value")
    return RadioGroupResponse(id=component_id, custom_id=custom_id, value=value)


def _parse_checkbox_group(component: dict[str, Any]) -> CheckboxGroupResponse:
    """Parse a CheckboxGroup component."""
    component_id = component.get("id")
    if component_id is None:
        raise ParseError("CheckboxGroup component missing id")
    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("CheckboxGroup component missing custom_id")
    values = component.get("values", [])
    if not isinstance(values, list):
        raise ParseError("CheckboxGroup values must be a list")
    return CheckboxGroupResponse(id=component_id, custom_id=custom_id, values=values)


def _parse_checkbox(component: dict[str, Any]) -> CheckboxResponse:
    """Parse a Checkbox component."""
    component_id = component.get("id")
    if component_id is None:
        raise ParseError("Checkbox component missing id")
    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("Checkbox component missing custom_id")
    value = component.get("value", False)
    if not isinstance(value, bool):
        raise ParseError("Checkbox value must be a boolean")
    return CheckboxResponse(id=component_id, custom_id=custom_id, value=value)


def _parse_select_menu(component: dict[str, Any]) -> Any:
    """Parse a Select Menu component."""
    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("Select menu component missing custom_id")
    values = component.get("values", [])
    if not isinstance(values, list):
        raise ParseError("Select menu values must be a list")

    class SelectMenuResponse:
        def __init__(self, custom_id: str, values: list[str]):
            self.custom_id = custom_id
            self.values = values

    return SelectMenuResponse(custom_id=custom_id, values=values)


def _parse_text_input(component: dict[str, Any]) -> Any:
    """Parse a TextInput component."""
    custom_id = component.get("custom_id")
    if not custom_id:
        raise ParseError("TextInput component missing custom_id")
    value = component.get("value", "")

    class TextInputResponse:
        def __init__(self, custom_id: str, value: str):
            self.custom_id = custom_id
            self.value = value

    return TextInputResponse(custom_id=custom_id, value=value)
