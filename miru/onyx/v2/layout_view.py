"""LayoutView - Discord.py-like syntax for Hikari Components v2.

Example:
    class MyComponents(LayoutView):
        container1 = Container(
            TextDisplay("Hello World!"),
            Section(
                TextDisplay("Text with button"),
                accessory=Button("Click me", "btn1")
            ),
            accent_color="#8CC4C2"
        )

    view = MyComponents()
    await ctx.respond(component=view.build(), flags=hikari.MessageFlag.IS_COMPONENTS_V2)
"""

from typing import List, Union, Optional, Any
import hikari
from miru.onyx.v2.builders import (
    Container,
    TextDisplay,
    Separator,
    ActionRow,
    Button,
    LinkButton,
    SelectMenu,
    MediaGallery,
    File,
    Section,
    Thumbnail,
)


class LayoutView:
    """Base class for creating Components v2 layouts with a discord.py-like syntax.

    Define your components as class attributes and they will be automatically
    collected and built when you call build().

    Example:
        class MyView(LayoutView):
            container1 = Container(
                TextDisplay("Welcome!"),
                Section(
                    TextDisplay("Info"),
                    accessory=Button("Click", "btn_id")
                ),
            )
            separator1 = Separator()
            text1 = TextDisplay("More content")

        view = MyView()
        component = view.build()
    """

    def __init__(self):
        self._components: List[Any] = []
        self._collect_components()

    def _collect_components(self) -> None:
        """Collect all component attributes from the class."""
        for attr_name in dir(self.__class__):
            if attr_name.startswith('_') or callable(getattr(self.__class__, attr_name)):
                continue

            attr_value = getattr(self.__class__, attr_name)

            if isinstance(attr_value, (
                Container,
                TextDisplay,
                Separator,
                ActionRow,
                MediaGallery,
                File,
                Section,
            )):
                self._components.append(attr_value)

    def build(self) -> Union[hikari.impl.ContainerComponentBuilder, List[hikari.api.ComponentBuilder]]:
        """Build all components into Hikari builders."""
        if not self._components:
            raise ValueError("No components defined in LayoutView")

        if len(self._components) == 1 and isinstance(self._components[0], Container):
            return self._components[0].build()

        built = []
        for comp in self._components:
            built.append(comp.build())
        return built

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(components={len(self._components)})"


def create_components(
    *components: Union[Container, TextDisplay, Separator, ActionRow, MediaGallery, File, Section],
) -> List[hikari.api.ComponentBuilder]:
    """Quick helper to create a list of components without defining a class.

    Example:
        components = create_components(
            TextDisplay("Before container"),
            Container(
                TextDisplay("Inside container"),
                Section(
                    TextDisplay("Text with button"),
                    accessory=Button("Click", "btn")
                ),
                accent_color=Colors.BLURPLE
            ),
            TextDisplay("After container"),
        )
    """
    return [comp.build() for comp in components]


def components(
    *items: Union[Container, TextDisplay, Separator, ActionRow, MediaGallery, File, Section],
) -> List[hikari.api.ComponentBuilder]:
    """Alias for create_components - shorter name for inline usage.

    Example:
        await ctx.respond(
            components=components(
                TextDisplay("# Title"),
                Container(
                    Section(
                        TextDisplay("Info text"),
                        accessory=Button("Click", "btn")
                    ),
                    accent_color=Colors.BLURPLE
                ),
            ),
            flags=hikari.MessageFlag.IS_COMPONENTS_V2
        )
    """
    return create_components(*items)
