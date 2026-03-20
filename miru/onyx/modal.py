"""OnyxCord Modal - Custom modal implementation for OnyxCord components."""

from __future__ import annotations

import typing as t
import asyncio
import logging

import hikari
from miru.modal import Modal as _MiruModal
from miru.context.modal import ModalContext as _MiruModalContext
from miru.response import ModalBuilder as _MiruModalBuilder

if t.TYPE_CHECKING:
    from miru.client import Client as _MiruClient

__all__ = ["OnyxModal", "OnyxModalRegistry", "install_modal_handler"]

logger = logging.getLogger(__name__)


class OnyxModalRegistry:
    """Registry for managing active OnyxCord modals.

    This registry maintains a mapping of custom_id -> modal instance
    and handles modal lifecycle (registration, timeout, removal).
    """

    def __init__(self):
        self._modals: dict[str, OnyxModal] = {}
        self._timeouts: dict[str, asyncio.Task] = {}

    def register(self, modal: OnyxModal) -> None:
        """Register a modal in the registry."""
        custom_id = modal.custom_id
        self._modals[custom_id] = modal

        if modal.timeout is not None and modal.timeout > 0:
            task = asyncio.create_task(self._timeout_modal(custom_id, modal.timeout))
            self._timeouts[custom_id] = task

        logger.debug(f"✅ Registered OnyxModal: {custom_id}")

    def unregister(self, custom_id: str) -> None:
        """Unregister a modal from the registry."""
        if custom_id in self._modals:
            del self._modals[custom_id]
            logger.debug(f"🗑️ Unregistered OnyxModal: {custom_id}")

        if custom_id in self._timeouts:
            self._timeouts[custom_id].cancel()
            del self._timeouts[custom_id]

    def get(self, custom_id: str) -> OnyxModal | None:
        """Get a modal by custom_id."""
        return self._modals.get(custom_id)

    async def _timeout_modal(self, custom_id: str, timeout: float) -> None:
        """Handle modal timeout."""
        try:
            await asyncio.sleep(timeout)
            modal = self._modals.get(custom_id)
            if modal:
                logger.debug(f"⏱️ Modal timed out: {custom_id}")
                if hasattr(modal, 'on_timeout'):
                    try:
                        await modal.on_timeout()
                    except Exception as e:
                        logger.error(f"Error in modal on_timeout: {e}", exc_info=True)
                self.unregister(custom_id)
        except asyncio.CancelledError:
            pass


# Global registry instance
_global_registry = OnyxModalRegistry()


def install_modal_handler(bot: hikari.GatewayBot) -> None:
    """Install the OnyxCord modal submit handler on a bot.

    This function sets up an event listener that intercepts modal submit
    interactions and routes them to OnyxCord modals for processing.

    Parameters
    ----------
    bot : hikari.GatewayBot
        The bot instance to install the handler on

    Example
    -------
    ```python
    import hikari
    from miru.onyx import install_modal_handler

    bot = hikari.GatewayBot(token="...")
    install_modal_handler(bot)
    ```
    """
    _raw_payloads: dict[str, dict] = {}

    @bot.listen(hikari.ShardPayloadEvent)
    async def _capture_raw_payload(event: hikari.ShardPayloadEvent) -> None:
        """Capture raw payload before Hikari discards unknown components."""
        if event.name != "INTERACTION_CREATE":
            return
        data = event.payload
        if data.get("type") != 5:  # type 5 = modal submit
            return
        interaction_id = data.get("id")
        if interaction_id:
            _raw_payloads[interaction_id] = data
            logger.debug(f"📦 Captured raw modal submit payload for {interaction_id}")

    @bot.listen()
    async def _onyx_modal_submit_handler(event: hikari.InteractionCreateEvent) -> None:
        """Handle modal submit interactions for OnyxCord modals."""
        if not isinstance(event.interaction, hikari.ModalInteraction):
            return

        custom_id = event.interaction.custom_id
        modal = _global_registry.get(custom_id)

        if modal is None:
            return

        logger.info(f"🔍 Processing OnyxModal submit: {custom_id}")

        interaction_id = str(event.interaction.id)
        raw_data = _raw_payloads.get(interaction_id)

        if raw_data:
            logger.debug(f"✅ Found raw data for interaction {interaction_id}")
            del _raw_payloads[interaction_id]
        else:
            logger.warning(f"⚠️ No raw data found for interaction {interaction_id}")

        try:
            await modal._handle_submit(event.interaction, raw_data)
        except Exception as e:
            logger.error(f"❌ Error handling OnyxModal submit: {e}", exc_info=True)
            try:
                await event.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_CREATE,
                    f"❌ Erro ao processar modal: {str(e)}",
                    flags=hikari.MessageFlag.EPHEMERAL,
                )
            except Exception:
                pass

    print("✅ OnyxCord modal handler installed")
    logger.info("✅ OnyxCord modal handler installed")


class OnyxModal(_MiruModal):
    """Custom Modal implementation that supports OnyxCord components.

    This modal extends miru.Modal to properly serialize OnyxCord components
    (Label, FileUpload, RadioGroup, CheckboxGroup, Checkbox) which are not
    natively supported by hikari's modal builder.

    Example
    -------
    ```python
    from miru.onyx import OnyxModal, OnyxLabel, OnyxFileUpload
    import miru

    class MyModal(OnyxModal, title="My Modal", custom_id="my_modal"):
        name_input = miru.TextInput(label="Name", required=True)

        file_upload = OnyxLabel(
            label="Upload File",
            component=OnyxFileUpload(custom_id="file", required=False)
        )

        async def callback(self, ctx: miru.ModalContext) -> None:
            await ctx.respond(f"Name: {self.name_input.value}")
    ```
    """

    def __init_subclass__(cls, *, title: str | None = None, custom_id: str | None = None, **kwargs: t.Any) -> None:
        """Handle custom_id parameter in class definition."""
        super().__init_subclass__(title=title, **kwargs)
        if custom_id is not None:
            cls._custom_id = custom_id

    def __init__(self, *, title: str | None = None, custom_id: str | None = None, timeout: float | None = 300.0) -> None:
        """Initialize the modal with optional custom_id override."""
        if custom_id is None and hasattr(self.__class__, '_custom_id'):
            custom_id = self.__class__._custom_id
            logger.debug(f"🔍 Using class-level custom_id for {self.__class__.__name__}: {custom_id}")

        super().__init__(title=title, custom_id=custom_id, timeout=timeout)
        logger.debug(f"✅ Modal {self.__class__.__name__} initialized with custom_id: {self.custom_id}")

        _global_registry.register(self)

    async def _handle_submit(self, interaction: hikari.ModalInteraction, raw_data: dict[str, t.Any] | None = None) -> None:
        """Handle modal submit interaction."""
        from miru.onyx.parser.modal_submit import parse_modal_submit
        from miru.onyx.entity_factory import get_raw_payload, clear_raw_components

        interaction_id = str(interaction.id)
        raw_payload = get_raw_payload(interaction_id)

        if raw_payload and 'data' in raw_payload:
            data = raw_payload['data']
            payload = {
                "components": data.get('components', []),
                "resolved": data.get('resolved', {}),
            }
            logger.debug("✅ Using raw payload from OnyxEntityFactory")
        elif raw_data and 'data' in raw_data:
            data = raw_data['data']
            payload = {
                "components": data.get('components', []),
                "resolved": data.get('resolved', {}),
            }
            logger.debug("Using raw data from fallback")
        else:
            logger.warning("Could not access raw components, using hikari's parsed components")
            raw_components_list = []
            if interaction.components:
                for action_row in interaction.components:
                    row_dict: dict[str, t.Any] = {"type": 1, "components": []}
                    for component in action_row.components:
                        comp_dict = self._component_to_dict(component)
                        if comp_dict:
                            row_dict["components"].append(comp_dict)
                    if row_dict["components"]:
                        raw_components_list.append(row_dict)
            payload = {"components": raw_components_list, "resolved": {}}

        logger.debug(f"Raw payload for parsing: {payload}")

        try:
            parsed_values = parse_modal_submit(payload)
            logger.debug(f"Parsed values: {parsed_values}")
        except Exception as e:
            logger.error(f"Failed to parse modal submit: {e}", exc_info=True)
            parsed_values = {}
        finally:
            clear_raw_components(interaction_id)

        self._inject_values(parsed_values)

        values_dict: dict[t.Any, str] = {}
        for item in self.children:
            if hasattr(item, 'custom_id') and hasattr(item, '_value'):
                for action_row in interaction.components:
                    for component in action_row.components:
                        if hasattr(component, 'custom_id') and component.custom_id == item.custom_id:
                            if hasattr(component, 'value'):
                                item._value = component.value
                                values_dict[item] = component.value
                            break

        client = getattr(self, '_client', None)
        if client is None:
            logger.warning("Modal has no client, creating minimal context")

        ctx = _MiruModalContext(
            modal=self,
            client=client,
            interaction=interaction,
            values=values_dict,
        )

        try:
            await self.callback(ctx)
        except Exception as e:
            logger.error(f"Error in modal callback: {e}", exc_info=True)
            raise
        finally:
            _global_registry.unregister(self.custom_id)

    def _component_to_dict(self, component: t.Any) -> dict[str, t.Any] | None:
        """Convert a hikari component to a dictionary."""
        try:
            if isinstance(component, dict):
                logger.debug(f"Component is already a dict (unknown type preserved): {component.get('type')}")
                return component

            comp_dict: dict[str, t.Any] = {}
            if hasattr(component, 'type'):
                comp_dict['type'] = int(component.type)
            if hasattr(component, 'custom_id'):
                comp_dict['custom_id'] = component.custom_id
            if hasattr(component, 'value'):
                comp_dict['value'] = component.value
            elif hasattr(component, 'values'):
                comp_dict['values'] = list(component.values)
            if hasattr(component, 'label'):
                comp_dict['label'] = component.label
            logger.debug(f"Converted component to dict: {comp_dict}")
            return comp_dict if comp_dict else None
        except Exception as e:
            logger.debug(f"Failed to convert component to dict: {e}")
            return None

    def _inject_values(self, parsed_values: dict[str, t.Any]) -> None:
        """Inject parsed values into component attributes."""
        for cls in reversed(type(self).__mro__):
            for name, val in vars(cls).items():
                if name.startswith("_"):
                    continue
                try:
                    instance_val = getattr(self, name, None)
                except (RuntimeError, AttributeError):
                    continue
                if instance_val is None:
                    continue

                if hasattr(instance_val, 'component'):
                    child = instance_val.component
                    if hasattr(child, 'custom_id'):
                        custom_id = child.custom_id
                        if custom_id in parsed_values:
                            response = parsed_values[custom_id]
                            if hasattr(response, 'values'):
                                child.values = response.values
                            if hasattr(response, 'attachments'):
                                child.attachments = response.attachments
                            if hasattr(response, 'value'):
                                if hasattr(child, '_value'):
                                    child._value = response.value
                                else:
                                    child.value = response.value

                elif hasattr(instance_val, 'custom_id'):
                    custom_id = instance_val.custom_id
                    if custom_id in parsed_values:
                        response = parsed_values[custom_id]
                        if hasattr(response, 'values'):
                            instance_val.values = response.values
                        if hasattr(response, 'attachments'):
                            instance_val.attachments = response.attachments
                        if hasattr(response, 'value'):
                            if hasattr(instance_val, '_value'):
                                instance_val._value = response.value
                            else:
                                instance_val.value = response.value

    def build_response(self, client: _MiruClient) -> _MiruModalBuilder:
        """Build the modal response with OnyxCord component support."""
        self._client = client
        builder = OnyxModalBuilder(self.title, self.custom_id, self)
        builder._client = client
        return builder


class OnyxModalBuilder:
    """Custom modal builder that properly serializes OnyxCord components."""

    def __init__(self, title: str, custom_id: str, modal: OnyxModal):
        self.title = title
        self.custom_id = custom_id
        self.modal = modal
        self._client: _MiruClient | None = None

    async def create_modal_response(self, interaction: hikari.ModalResponseMixin) -> None:
        """Create a modal response with properly serialized components."""
        components = self._build_components()

        route = hikari.internal.routes.POST_INTERACTION_RESPONSE.compile(
            interaction=interaction.id,
            token=interaction.token,
        )

        payload = {
            "type": hikari.ResponseType.MODAL,
            "data": {
                "custom_id": self.custom_id,
                "title": self.title,
                "components": components,
            },
        }

        await interaction.app.rest._request(route, json=payload)

    def _build_components(self) -> list[dict[str, t.Any]]:
        """Build components as raw JSON dictionaries."""
        components: list[dict[str, t.Any]] = []
        seen_ids: set[int] = set()

        attrs: list[t.Any] = []
        for cls in reversed(type(self.modal).__mro__):
            for name, val in vars(cls).items():
                if name.startswith("_"):
                    continue
                try:
                    instance_val = getattr(self.modal, name, None)
                except (RuntimeError, AttributeError):
                    continue
                if instance_val is None:
                    continue
                obj_id = id(instance_val)
                if obj_id in seen_ids:
                    continue
                if hasattr(instance_val, "to_payload"):
                    seen_ids.add(obj_id)
                    attrs.append(instance_val)
                elif hasattr(instance_val, "_build") and hasattr(instance_val, "custom_id"):
                    seen_ids.add(obj_id)
                    attrs.append(instance_val)

        for item in attrs:
            if hasattr(item, "to_payload"):
                component_payload = item.to_payload()
                component_type = component_payload.get("type")

                if component_type == 18:
                    components.append(component_payload)
                elif component_type in (23, 19, 21, 22):
                    custom_id = component_payload.get("custom_id", "input")
                    label_text = custom_id.replace("_", " ").title()
                    label_wrapper = {
                        "type": 18,
                        "label": label_text[:45],
                        "component": component_payload,
                    }
                    components.append(label_wrapper)
                elif component_type in (3, 5, 6, 7, 8):
                    custom_id = component_payload.get("custom_id", "select")
                    label_text = component_payload.get("placeholder", custom_id.replace("_", " ").title())
                    label_wrapper = {
                        "type": 18,
                        "label": label_text[:45],
                        "component": component_payload,
                    }
                    components.append(label_wrapper)
                elif component_type == 4:
                    action_row = {"type": 1, "components": [component_payload]}
                    components.append(action_row)
                else:
                    custom_id = component_payload.get("custom_id", "component")
                    label_text = custom_id.replace("_", " ").title()
                    label_wrapper = {
                        "type": 18,
                        "label": label_text[:45],
                        "component": component_payload,
                    }
                    components.append(label_wrapper)
            else:
                action_row = hikari.impl.ModalActionRowBuilder()
                item._build(action_row)
                built = action_row.build()
                if built:
                    components.append(built)

        return components
