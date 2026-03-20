"""Helper utilities for Components v2."""

from typing import Union, Optional, List
import hikari
from miru.onyx.v2.builders import (
    Container,
    TextDisplay,
    Separator,
    ActionRow,
    Button,
    LinkButton,
    SelectMenu,
    SelectOption,
    MediaGallery,
    MediaGalleryItem,
    File,
    Section,
    Thumbnail,
)


# Re-export hikari enums for convenience
ButtonStyle = hikari.ButtonStyle
SpacingType = hikari.SpacingType


class Colors:
    """Predefined color palette for containers."""

    # Discord brand colors
    BLURPLE = "#5865F2"
    GREEN = "#57F287"
    YELLOW = "#FEE75C"
    FUCHSIA = "#EB459E"
    RED = "#ED4245"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

    # Additional colors
    BLUE = "#3498DB"
    PURPLE = "#9B59B6"
    ORANGE = "#E67E22"
    TEAL = "#1ABC9C"
    PINK = "#FF69B4"
    GRAY = "#95A5A6"
    DARK_GRAY = "#607D8B"

    # Status colors
    SUCCESS = "#43B581"
    WARNING = "#FAA61A"
    ERROR = "#F04747"
    INFO = "#00B0F4"


def quick_container(
    *content: Union[str, TextDisplay, Separator, ActionRow, MediaGallery, File, Section],
    accent_color: Optional[Union[str, hikari.Color]] = None,
) -> Container:
    """Quick helper to create a container with automatic text conversion.

    Strings are automatically converted to TextDisplay components.

    Example:
        container = quick_container(
            "# Welcome!",
            "This is some text",
            Separator(),
            Section(
                TextDisplay("Text with button"),
                accessory=Button("Click", "btn")
            ),
            accent_color=Colors.BLURPLE
        )
    """
    components = []
    for item in content:
        if isinstance(item, str):
            components.append(TextDisplay(item))
        else:
            components.append(item)
    return Container(*components, accent_color=accent_color)


def button_row(*buttons: Union[Button, LinkButton]) -> ActionRow:
    """Quick helper to create an ActionRow with buttons.

    Example:
        row = button_row(
            Button("Yes", "yes_btn", style=ButtonStyle.SUCCESS),
            Button("No", "no_btn", style=ButtonStyle.DANGER),
        )
    """
    return ActionRow(*buttons)


def select_row(
    custom_id: str,
    *options: Union[SelectOption, tuple],
    placeholder: Optional[str] = None,
    min_values: int = 1,
    max_values: int = 1,
) -> ActionRow:
    """Quick helper to create an ActionRow with a select menu.

    Options can be SelectOption instances or tuples of (label, value).

    Example:
        row = select_row(
            "my_select",
            ("Option 1", "opt1"),
            ("Option 2", "opt2"),
            placeholder="Choose an option",
        )
    """
    select_options = []
    for opt in options:
        if isinstance(opt, tuple):
            label, value = opt
            select_options.append(SelectOption(label, value))
        else:
            select_options.append(opt)

    menu = SelectMenu(
        custom_id=custom_id,
        options=select_options,
        placeholder=placeholder,
        min_values=min_values,
        max_values=max_values,
    )
    return ActionRow(menu)


def image_gallery(*urls: str, descriptions: Optional[List[str]] = None) -> MediaGallery:
    """Quick helper to create a media gallery from URLs.

    Example:
        gallery = image_gallery(
            "https://example.com/image1.png",
            "https://example.com/image2.png",
            descriptions=["First image", "Second image"]
        )
    """
    items = []
    for i, url in enumerate(urls):
        desc = descriptions[i] if descriptions and i < len(descriptions) else None
        items.append(MediaGalleryItem(url, description=desc))
    return MediaGallery(*items)


def divider(spacing: hikari.SpacingType = hikari.SpacingType.SMALL) -> Separator:
    """Quick helper to create a visible separator/divider."""
    return Separator(visible=True, spacing=spacing)


def spacer(spacing: hikari.SpacingType = hikari.SpacingType.SMALL) -> Separator:
    """Quick helper to create an invisible spacer."""
    return Separator(visible=False, spacing=spacing)


# Convenience aliases
Text = TextDisplay
Row = ActionRow
Gallery = MediaGallery
