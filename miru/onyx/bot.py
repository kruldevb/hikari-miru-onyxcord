"""OnyxCord Bot - GatewayBot with OnyxEntityFactory."""

from __future__ import annotations

import typing as t

import hikari

from miru.onyx.entity_factory import OnyxEntityFactory

__all__ = ["OnyxBot"]


class OnyxBot(hikari.GatewayBot):
    """Custom GatewayBot that uses OnyxEntityFactory.

    This bot automatically uses the OnyxEntityFactory which preserves
    unknown modal component types, enabling OnyxCord modals to work.

    Usage is identical to hikari.GatewayBot:

    ```python
    from miru.onyx import OnyxBot

    bot = OnyxBot(token="...")
    bot.run()
    ```
    """

    def __init__(
        self,
        token: str,
        *,
        allow_color: bool = True,
        banner: str | None = "hikari",
        executor: t.Any | None = None,
        force_color: bool = False,
        cache_settings: hikari.api.CacheSettings | None = None,
        http_settings: hikari.api.HTTPSettings | None = None,
        intents: hikari.Intents = hikari.Intents.ALL_UNPRIVILEGED,
        auto_chunk_members: bool = True,
        logs: str | int | dict[str, t.Any] | None = "INFO",
        max_rate_limit: float = 300.0,
        max_retries: int = 3,
        proxy_settings: hikari.api.ProxySettings | None = None,
        rest_url: str | None = None,
    ) -> None:
        """Initialize the OnyxBot with OnyxEntityFactory.

        Parameters are identical to hikari.GatewayBot.
        """
        super().__init__(
            token=token,
            allow_color=allow_color,
            banner=banner,
            executor=executor,
            force_color=force_color,
            cache_settings=cache_settings,
            http_settings=http_settings,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            logs=logs,
            max_rate_limit=max_rate_limit,
            max_retries=max_retries,
            proxy_settings=proxy_settings,
            rest_url=rest_url,
        )

        # Replace entity factory with our custom one AFTER parent init
        self._entity_factory = OnyxEntityFactory(self)

        # Update REST client to use new entity factory
        if hasattr(self, '_rest'):
            self._rest._entity_factory = self._entity_factory
