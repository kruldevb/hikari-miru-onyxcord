"""OnyxCord Entity Factory - Preserves unknown component types."""

from __future__ import annotations

import typing as t
import logging

import hikari
from hikari.impl import entity_factory

logger = logging.getLogger(__name__)

# Global storage for raw modal payloads
_raw_modal_payloads: dict[str, dict[str, t.Any]] = {}


def get_raw_components(interaction_id: str) -> list[dict[str, t.Any]] | None:
    """Get raw components for a modal interaction before Hikari processes them.

    Parameters
    ----------
    interaction_id : str
        The interaction ID

    Returns
    -------
    list[dict[str, Any]] | None
        Raw component data, or None if not found
    """
    payload = _raw_modal_payloads.get(interaction_id)
    if payload:
        return payload.get("data", {}).get("components", [])
    return None


def get_raw_payload(interaction_id: str) -> dict[str, t.Any] | None:
    """Get complete raw payload for a modal interaction.

    Parameters
    ----------
    interaction_id : str
        The interaction ID

    Returns
    -------
    dict[str, Any] | None
        Complete raw payload including resolved data, or None if not found
    """
    return _raw_modal_payloads.get(interaction_id)


def clear_raw_components(interaction_id: str) -> None:
    """Clear raw components for an interaction after processing.

    Parameters
    ----------
    interaction_id : str
        The interaction ID
    """
    if interaction_id in _raw_modal_payloads:
        del _raw_modal_payloads[interaction_id]


class OnyxEntityFactory(entity_factory.EntityFactoryImpl):
    """Custom entity factory that preserves unknown modal component types.

    This factory extends Hikari's default entity factory to store raw modal
    interaction payloads before processing, allowing OnyxCord to access
    component types (18-23) that Hikari doesn't natively support.
    """

    def deserialize_modal_interaction(
        self,
        payload: hikari.internal.data_binding.JSONObject,
    ) -> hikari.ModalInteraction:
        """Deserialize a modal interaction, storing raw payload first."""
        # Store raw payload before Hikari processes it
        interaction_id = payload.get("id")
        if interaction_id:
            _raw_modal_payloads[interaction_id] = payload
            logger.debug(f"📦 Stored raw modal payload for interaction {interaction_id}")

        # Call parent implementation
        return super().deserialize_modal_interaction(payload)


__all__ = ["OnyxEntityFactory", "get_raw_components", "get_raw_payload", "clear_raw_components"]
