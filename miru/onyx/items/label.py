"""Miru integration for Label component."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.components.label import Label

if t.TYPE_CHECKING:
    from miru.abc.item import ModalItem
    from miru.context.modal import ModalContext
    from miru.modal import Modal

__all__ = ["OnyxLabel"]


class OnyxLabel:
    """Miru ModalItem implementation for Label component.

    Parameters
    ----------
    label : str
        Label text (max 45 characters)
    component : ModalItem
        Child component to wrap
    description : str | None
        Optional description text (max 100 characters)
    custom_id : str | None
        Custom identifier for the label
    row : int | None
        Row position in the modal
    """

    def __init__(
        self,
        *,
        label: str,
        component: t.Any,
        description: str | None = None,
        custom_id: str | None = None,
        row: int | None = None,
    ) -> None:
        if len(label) > 45:
            raise ValueError(f"Label text must be 45 characters or less (got {len(label)})")
        if description is not None and len(description) > 100:
            raise ValueError(f"Description must be 100 characters or less (got {len(description)})")

        self.label = label
        self.description = description
        self.component = component
        self._custom_id = custom_id or f"onyx_label_{id(self)}"
        self._row = row
        self._handler: Modal | None = None
        self._id: int | None = None

    @property
    def type(self) -> int:
        return 18

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def row(self) -> int | None:
        return self._row

    def _build(self, action_row: hikari.api.ModalActionRowBuilder) -> None:
        self._payload: dict[str, t.Any] = self.to_payload()

    async def _refresh_state(self, context: ModalContext) -> None:
        if hasattr(self.component, "_refresh_state"):
            await self.component._refresh_state(context)

    def to_payload(self) -> dict[str, t.Any]:
        if hasattr(self.component, "to_payload"):
            child_payload = self.component.to_payload()
        elif hasattr(self.component, "_build"):
            action_row = hikari.impl.ModalActionRowBuilder()
            self.component._build(action_row)
            built = action_row.build()
            if built and "components" in built and len(built["components"]) > 0:
                child_payload = built["components"][0]
                if "label" in child_payload:
                    del child_payload["label"]
            else:
                child_payload = {
                    "type": getattr(self.component, "type", 4),
                    "custom_id": getattr(self.component, "custom_id", ""),
                    "style": int(getattr(self.component, "style", 1)),
                    "required": getattr(self.component, "required", True),
                }
                if hasattr(self.component, "placeholder") and self.component.placeholder:
                    child_payload["placeholder"] = self.component.placeholder
                if hasattr(self.component, "value") and self.component.value:
                    child_payload["value"] = self.component.value
                if hasattr(self.component, "min_length") and self.component.min_length is not None:
                    child_payload["min_length"] = self.component.min_length
                if hasattr(self.component, "max_length") and self.component.max_length is not None:
                    child_payload["max_length"] = self.component.max_length
        else:
            child_payload = {
                "type": getattr(self.component, "type", 4),
                "custom_id": getattr(self.component, "custom_id", ""),
                "style": int(getattr(self.component, "style", 1)),
                "required": getattr(self.component, "required", True),
            }

        payload: dict[str, t.Any] = {
            "type": 18,
            "label": self.label,
            "component": child_payload,
        }
        if self.description is not None:
            payload["description"] = self.description
        if self._id is not None:
            payload["id"] = self._id
        return payload

    def to_component(self) -> Label:
        return Label(
            label=self.label,
            description=self.description,
            component=self.component,
            id=self._id,
        )
