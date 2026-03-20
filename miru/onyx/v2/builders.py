"""Simplified builders for Hikari Components v2.

Includes Section and Thumbnail components (NEW - not in original OnyxCord).

Example:
    # Section with button accessory
    section = Section(
        TextDisplay("Never trust a lizard with a banana."),
        accessory=Button("Friendly Monkey", "btn_id")
    )

    # Section with thumbnail accessory
    section = Section(
        TextDisplay("Some text here"),
        accessory=Thumbnail("https://example.com/image.png")
    )

    # Section with link button accessory
    section = Section(
        TextDisplay("Click the link!"),
        accessory=LinkButton("Google", "https://google.com")
    )
"""

from typing import Optional, Union, List, Any
import hikari


class TextDisplay:
    """Simplified TextDisplay component builder."""

    def __init__(self, content: str):
        self.content = content

    def build(self) -> hikari.impl.TextDisplayComponentBuilder:
        return hikari.impl.TextDisplayComponentBuilder(content=self.content)


class Separator:
    """Simplified Separator component builder."""

    def __init__(
        self,
        visible: bool = True,
        spacing: hikari.SpacingType = hikari.SpacingType.SMALL,
    ):
        self.visible = visible
        self.spacing = spacing

    def build(self) -> hikari.impl.SeparatorComponentBuilder:
        return hikari.impl.SeparatorComponentBuilder(
            divider=self.visible,
            spacing=self.spacing,
        )


class SelectOption:
    """Simplified SelectOption builder."""

    def __init__(
        self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[Union[str, hikari.Emoji]] = None,
        default: bool = False,
    ):
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def build(self) -> hikari.impl.SelectOptionBuilder:
        # Only include emoji if it's not None
        kwargs = {
            "label": self.label,
            "value": self.value,
            "is_default": self.default,
        }
        
        if self.description is not None:
            kwargs["description"] = self.description
        
        if self.emoji is not None:
            kwargs["emoji"] = self.emoji
        
        return hikari.impl.SelectOptionBuilder(**kwargs)


class SelectMenu:
    """Simplified SelectMenu builder."""

    def __init__(
        self,
        custom_id: str,
        options: List[SelectOption],
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
    ):
        self.custom_id = custom_id
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values

    def build(self) -> hikari.impl.TextSelectMenuBuilder:
        return hikari.impl.TextSelectMenuBuilder(
            custom_id=self.custom_id,
            options=[opt.build() for opt in self.options],
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
        )


class Button:
    """Simplified interactive Button builder."""

    def __init__(
        self,
        label: str,
        custom_id: str,
        style: hikari.ButtonStyle = hikari.ButtonStyle.PRIMARY,
        emoji: Optional[Union[str, hikari.Emoji]] = None,
        disabled: bool = False,
    ):
        self.label = label
        self.custom_id = custom_id
        self.style = style
        self.emoji = emoji
        self.disabled = disabled

    def build(self) -> hikari.impl.InteractiveButtonBuilder:
        kwargs = {
            "style": self.style,
            "label": self.label,
            "custom_id": self.custom_id,
            "is_disabled": self.disabled,
        }
        
        # Only include emoji if it's not None
        if self.emoji is not None:
            kwargs["emoji"] = self.emoji
        
        return hikari.impl.InteractiveButtonBuilder(**kwargs)


class LinkButton:
    """Simplified link Button builder."""

    def __init__(
        self,
        label: str,
        url: str,
        emoji: Optional[Union[str, hikari.Emoji]] = None,
        disabled: bool = False,
    ):
        self.label = label
        self.url = url
        self.emoji = emoji
        self.disabled = disabled

    def build(self) -> hikari.impl.LinkButtonBuilder:
        kwargs = {
            "url": self.url,
            "label": self.label,
            "is_disabled": self.disabled,
        }
        
        # Only include emoji if it's not None
        if self.emoji is not None:
            kwargs["emoji"] = self.emoji
        
        return hikari.impl.LinkButtonBuilder(**kwargs)


class ActionRow:
    """Simplified ActionRow builder."""

    def __init__(self, *components: Union[Button, LinkButton, SelectMenu]):
        self.components = components

    def build(self) -> hikari.impl.MessageActionRowBuilder:
        return hikari.impl.MessageActionRowBuilder(
            components=[comp.build() for comp in self.components]
        )


class MediaGalleryItem:
    """Simplified MediaGalleryItem builder."""

    def __init__(
        self,
        media: str,
        description: Optional[str] = None,
        spoiler: bool = False,
    ):
        self.media = media
        self.description = description
        self.spoiler = spoiler

    def build(self) -> hikari.impl.MediaGalleryItemBuilder:
        return hikari.impl.MediaGalleryItemBuilder(
            media=self.media,
            description=self.description,
            spoiler=self.spoiler,
        )


class MediaGallery:
    """Simplified MediaGallery builder."""

    def __init__(self, *items: MediaGalleryItem):
        self.items = items

    def build(self) -> hikari.impl.MediaGalleryComponentBuilder:
        return hikari.impl.MediaGalleryComponentBuilder(
            items=[item.build() for item in self.items]
        )


class File:
    """Simplified File component builder."""

    def __init__(
        self,
        file: str,
        description: Optional[str] = None,
        spoiler: bool = False,
    ):
        self.file = file
        self.description = description
        self.spoiler = spoiler

    def build(self) -> hikari.impl.FileComponentBuilder:
        return hikari.impl.FileComponentBuilder(
            file=self.file,
            description=self.description,
            spoiler=self.spoiler,
        )


class Thumbnail:
    """Simplified Thumbnail component builder.

    Can be used standalone or as an accessory in a Section component.

    Example:
        # As Section accessory
        section = Section(
            TextDisplay("Some text"),
            accessory=Thumbnail("https://example.com/image.png")
        )
    """

    def __init__(
        self,
        media: str,
        description: Optional[str] = None,
        spoiler: bool = False,
    ):
        self.media = media
        self.description = description
        self.spoiler = spoiler

    def build(self) -> hikari.impl.ThumbnailComponentBuilder:
        return hikari.impl.ThumbnailComponentBuilder(
            media=self.media,
        )


class Section:
    """Simplified Section component builder.

    A Section displays text content alongside an accessory component
    (Button, LinkButton, or Thumbnail) side by side.

    Layout: [text content] [accessory]

    IMPORTANT: Discord's Section component only accepts ONE TextDisplay.
    If you pass multiple TextDisplay components, they will be automatically
    combined into a single TextDisplay with line breaks (\n) between them.

    Example:
        # Single text (recommended)
        section = Section(
            TextDisplay("Never trust a lizard with a banana."),
            accessory=Button("Friendly Monkey", "btn_id")
        )

        # Multiple texts (auto-combined with \n)
        section = Section(
            TextDisplay("# Welcome!"),
            TextDisplay("Click the button to start."),
            accessory=Button("Start", "btn_id")
        )
        # Results in: "# Welcome!\nClick the button to start."

        # With link button
        section = Section(
            TextDisplay("Click the link!"),
            accessory=LinkButton("Google", "https://google.com")
        )

        # With thumbnail
        section = Section(
            TextDisplay("Some description text"),
            accessory=Thumbnail("https://example.com/image.png")
        )
    """

    def __init__(
        self,
        *components: TextDisplay,
        accessory: Union[Button, LinkButton, Thumbnail],
    ):
        if not components:
            raise ValueError("Section must have at least one TextDisplay component")
        self.components = components
        self.accessory = accessory

    def build(self) -> hikari.impl.SectionComponentBuilder:
        # Discord's Section only accepts ONE TextDisplay
        # If multiple are provided, combine them with line breaks
        if len(self.components) == 1:
            text_component = self.components[0]
        else:
            # Combine multiple TextDisplay into one with \n
            combined_text = "\n".join(comp.content for comp in self.components)
            text_component = TextDisplay(combined_text)
        
        return hikari.impl.SectionComponentBuilder(
            accessory=self.accessory.build(),
            components=[text_component.build()],
        )


class Container:
    """Simplified Container builder with pythonic syntax.

    Container is like a styled "embed" that groups components together with an accent color.

    IMPORTANT: Containers CANNOT be nested inside other containers.

    Example:
        container = Container(
            TextDisplay("# Title"),
            Separator(),
            Section(
                TextDisplay("Text with button"),
                accessory=Button("Click", "btn")
            ),
            ActionRow(Button("Click", "btn_id")),
            accent_color="#8CC4C2"
        )
    """

    def __init__(
        self,
        *components: Union[
            TextDisplay,
            Separator,
            ActionRow,
            MediaGallery,
            File,
            Section,
        ],
        accent_color: Optional[Union[str, hikari.Color]] = None,
    ):
        for comp in components:
            if isinstance(comp, Container):
                raise ValueError(
                    "Cannot nest Container inside another Container. "
                    "Containers are like styled 'embeds' and cannot be nested. "
                    "Use components outside the container if you need multiple sections."
                )

        self.components = components
        self.accent_color = accent_color

    def build(self) -> hikari.impl.ContainerComponentBuilder:
        color = None
        if self.accent_color:
            if isinstance(self.accent_color, str):
                color = hikari.Color.from_hex_code(self.accent_color)
            else:
                color = self.accent_color

        built_components = []
        for comp in self.components:
            built_components.append(comp.build())

        return hikari.impl.ContainerComponentBuilder(
            accent_color=color,
            components=built_components,
        )

    def __repr__(self) -> str:
        return f"Container(components={len(self.components)}, accent_color={self.accent_color})"
