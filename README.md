# hikari-miru - OnyxCord Modified Version

> **Fork modificado por Gustavo S.**
> 
> Esta é uma versão modificada do [hikari-miru](https://github.com/hypergonial/hikari-miru) para suportar os novos componentes de modais do Discord através do OnyxCord.

<div align="center">

[![Original PyPI](https://img.shields.io/pypi/v/hikari-miru)](https://pypi.org/project/hikari-miru)
[![Original Repo](https://img.shields.io/badge/original-hypergonial/hikari--miru-blue)](https://github.com/hypergonial/hikari-miru)

</div>

A component handler for [hikari](https://github.com/hikari-py/hikari), aimed at making the creation & management of Discord UI components easy.

## Modificações

Este fork inclui modificações para suportar os novos componentes de modais do Discord (tipos 18-23):
- Label (tipo 18)
- Separator (tipo 19)
- TextArea (tipo 20)
- MediaGallery (tipo 21)
- Checkbox (tipo 22)
- RadioGroup (tipo 23)

As modificações permitem que o miru trabalhe em conjunto com o OnyxCord para criar modais avançados com os novos componentes.

> [!TIP]
> Like what you see? Check out [arc](https://arc.hypergonial.com), a command handler with a focus on type-safety and correctness.

## Instalação

### A partir do Git (Recomendado para OnyxCord)

```sh
pip install git+https://github.com/kruldevb/hikari-miru-onyxcord.git
```

### Desenvolvimento Local

```sh
pip install -e .
```

### Versão Original

Para instalar a versão original não modificada:

```sh
pip install -U hikari-miru
```

## Usage

```py
import hikari
import miru

# REST bots are also supported
bot = hikari.GatewayBot(token="...")

# Wrap the bot in a miru client
client = miru.Client(bot)

class MyView(miru.View):

    @miru.button(label="Rock", emoji="\N{ROCK}", style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond("Paper!")

    @miru.button(label="Paper", emoji="\N{SCROLL}", style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond("Scissors!")

    @miru.button(label="Scissors", emoji="\N{BLACK SCISSORS}", style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, ctx: miru.ViewContext,  button: miru.Button) -> None:
        await ctx.respond("Rock!")

    @miru.button(emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=1)
    async def stop_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.stop() # Stop listening for interactions


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    # Ignore bots or webhooks pinging us
    if not event.is_human:
        return

    me = bot.get_me()

    # If the bot is mentioned
    if me.id in event.message.user_mentions_ids:
        view = MyView()  # Create a new view
        # Send the view as message components
        await event.message.respond("Rock Paper Scissors!", components=view)
        client.start_view(view) # Attach to the client & start it

bot.run()
```

To get started with `miru`, see the [documentation](https://miru.hypergonial.com), or the [examples](https://github.com/hypergonial/hikari-miru/tree/main/examples).

## Extensions

miru has two extensions built-in:

- [`ext.nav`](https://miru.hypergonial.com/guides/navigators/) - To make it easier to build navigators (sometimes called paginators).
- [`ext.menu`](https://miru.hypergonial.com/guides/menus/) - To make it easier to create nested menus.

Check the corresponding documentation and the [examples](https://github.com/hypergonial/hikari-miru/tree/main/examples) on how to use them.

## Issues and support

For general usage help or questions, see the `#miru` channel in the [hikari discord](https://discord.gg/hikari), if you have found a bug or have a feature request, feel free to [open an issue](https://github.com/hypergonial/hikari-miru/issues/new)!

## Contributing

See [Contributing](./CONTRIBUTING.md)

## Links

- [**Repositório Original**](https://github.com/hypergonial/hikari-miru)
- [**Documentação Original**](https://miru.hypergonial.com)
- [**Examples**](https://github.com/hypergonial/hikari-miru/tree/main/examples)
- [**License**](https://github.com/hypergonial/hikari-miru/blob/main/LICENSE)

---

**Modificado por:** Gustavo S.  
**Versão Base:** hikari-miru (hypergonial)  
**Propósito:** Suporte aos novos componentes de modais do Discord via OnyxCord
