"""
Exemplo de uso do componente Section (Components v2).

Section é um componente visual que exibe texto ao lado de um acessório
(botão, link ou thumbnail) de forma organizada.
"""

import hikari
import arc
from miru.onyx.v2 import (
    Section,
    TextDisplay,
    Button,
    LinkButton,
    Thumbnail,
    Container,
    Separator,
)

bot = hikari.GatewayBot(token="YOUR_TOKEN")
client = arc.GatewayClient(bot)


# ============================================================================
# EXEMPLO 1: Section com Botão
# ============================================================================

@client.include
@arc.slash_command("section_button", "Section com botão")
async def section_button(ctx: arc.GatewayContext):
    """Section simples com um botão ao lado do texto."""
    
    section = Section(
        TextDisplay("# Bem-vindo! 👋"),
        TextDisplay("Clique no botão para começar."),
        accessory=Button("Começar", "start_btn", style=hikari.ButtonStyle.SUCCESS)
    )
    
    await ctx.respond(
        component=section.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 2: Section com Link Button
# ============================================================================

@client.include
@arc.slash_command("section_link", "Section com link")
async def section_link(ctx: arc.GatewayContext):
    """Section com link button para site externo."""
    
    section = Section(
        TextDisplay("# 📚 Documentação"),
        TextDisplay("Acesse nossa documentação completa para aprender mais."),
        accessory=LinkButton("Ver Docs", "https://docs.hikari-py.dev/")
    )
    
    await ctx.respond(
        component=section.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 3: Section com Thumbnail
# ============================================================================

@client.include
@arc.slash_command("section_thumb", "Section com thumbnail")
async def section_thumb(ctx: arc.GatewayContext):
    """Section com imagem thumbnail ao lado."""
    
    section = Section(
        TextDisplay("# 🎨 Novo Produto!"),
        TextDisplay("Confira nosso mais novo lançamento."),
        TextDisplay("-# Disponível agora"),
        accessory=Thumbnail("https://picsum.photos/200")
    )
    
    await ctx.respond(
        component=section.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 4: Múltiplas Sections
# ============================================================================

@client.include
@arc.slash_command("multiple_sections", "Várias sections")
async def multiple_sections(ctx: arc.GatewayContext):
    """Várias sections em sequência."""
    
    # Section 1: Informação
    section1 = Section(
        TextDisplay("# ℹ️ Informação"),
        TextDisplay("Esta é a primeira seção com informações importantes."),
        accessory=Button("Saiba Mais", "info_btn", style=hikari.ButtonStyle.PRIMARY)
    )
    
    # Separador
    separator = Separator()
    
    # Section 2: Ação
    section2 = Section(
        TextDisplay("# ⚡ Ação Rápida"),
        TextDisplay("Execute uma ação rápida clicando no botão."),
        accessory=Button("Executar", "action_btn", style=hikari.ButtonStyle.SUCCESS)
    )
    
    # Separador
    separator2 = Separator()
    
    # Section 3: Link
    section3 = Section(
        TextDisplay("# 🔗 Recursos Externos"),
        TextDisplay("Acesse recursos adicionais em nosso site."),
        accessory=LinkButton("Visitar Site", "https://github.com")
    )
    
    # Criar lista de componentes
    components = [
        section1.build(),
        separator.build(),
        section2.build(),
        separator2.build(),
        section3.build(),
    ]
    
    await ctx.respond(
        components=components,
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 5: Section dentro de Container
# ============================================================================

@client.include
@arc.slash_command("section_container", "Section em container")
async def section_container(ctx: arc.GatewayContext):
    """Section dentro de um container colorido."""
    
    container = Container(
        TextDisplay("# 🎯 Painel de Controle"),
        Separator(),
        
        Section(
            TextDisplay("**Configurações**"),
            TextDisplay("Ajuste as configurações do sistema."),
            accessory=Button("Configurar", "config_btn", style=hikari.ButtonStyle.PRIMARY)
        ),
        
        Separator(),
        
        Section(
            TextDisplay("**Estatísticas**"),
            TextDisplay("Veja as estatísticas detalhadas."),
            accessory=Button("Ver Stats", "stats_btn", style=hikari.ButtonStyle.SECONDARY)
        ),
        
        Separator(),
        
        Section(
            TextDisplay("**Ajuda**"),
            TextDisplay("Precisa de ajuda? Acesse nossa documentação."),
            accessory=LinkButton("Documentação", "https://docs.example.com")
        ),
        
        accent_color="#5865F2"  # Discord Blurple
    )
    
    await ctx.respond(
        component=container.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 6: Section com Emoji e Formatação
# ============================================================================

@client.include
@arc.slash_command("section_fancy", "Section estilizada")
async def section_fancy(ctx: arc.GatewayContext):
    """Section com emojis e formatação markdown."""
    
    section = Section(
        TextDisplay("# 🚀 Lançamento Especial!"),
        TextDisplay("**Novidade:** Acabamos de lançar uma nova funcionalidade incrível!"),
        TextDisplay(""),
        TextDisplay("✨ Mais rápido"),
        TextDisplay("🎨 Mais bonito"),
        TextDisplay("🔒 Mais seguro"),
        TextDisplay(""),
        TextDisplay("-# Disponível para todos os usuários"),
        accessory=Button("Experimentar Agora", "try_btn", style=hikari.ButtonStyle.SUCCESS, emoji="🎉")
    )
    
    await ctx.respond(
        component=section.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 7: Perfil de Usuário com Section
# ============================================================================

@client.include
@arc.slash_command("user_profile", "Perfil com section")
async def user_profile(ctx: arc.GatewayContext):
    """Perfil de usuário usando section."""
    
    user = ctx.author
    
    container = Container(
        TextDisplay(f"# 👤 Perfil de {user.username}"),
        Separator(),
        
        Section(
            TextDisplay("**Informações**"),
            TextDisplay(f"ID: `{user.id}`"),
            TextDisplay(f"Criado em: <t:{int(user.created_at.timestamp())}:D>"),
            accessory=Thumbnail(str(user.avatar_url or user.default_avatar_url))
        ),
        
        Separator(),
        
        Section(
            TextDisplay("**Ações**"),
            TextDisplay("Envie uma mensagem direta para este usuário."),
            accessory=Button("Enviar DM", f"dm_{user.id}", style=hikari.ButtonStyle.PRIMARY)
        ),
        
        accent_color="#43B581"  # Verde
    )
    
    await ctx.respond(
        component=container.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 8: Notificação com Section
# ============================================================================

@client.include
@arc.slash_command("notification", "Notificação com section")
async def notification(ctx: arc.GatewayContext):
    """Notificação estilo alerta."""
    
    container = Container(
        Section(
            TextDisplay("# ⚠️ Atenção"),
            TextDisplay("Seu servidor será reiniciado em 5 minutos para manutenção."),
            TextDisplay(""),
            TextDisplay("**Duração estimada:** 10 minutos"),
            TextDisplay("**Impacto:** Serviço temporariamente indisponível"),
            accessory=Button("Entendi", "ack_btn", style=hikari.ButtonStyle.DANGER)
        ),
        
        accent_color="#FAA61A"  # Amarelo/Laranja
    )
    
    await ctx.respond(
        component=container.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# EXEMPLO 9: Menu de Opções com Sections
# ============================================================================

@client.include
@arc.slash_command("menu", "Menu com sections")
async def menu(ctx: arc.GatewayContext):
    """Menu de opções usando múltiplas sections."""
    
    container = Container(
        TextDisplay("# 📋 Menu Principal"),
        TextDisplay("Escolha uma opção abaixo:"),
        Separator(),
        
        Section(
            TextDisplay("**🎮 Jogar**"),
            TextDisplay("Iniciar um novo jogo"),
            accessory=Button("Jogar", "play_btn", style=hikari.ButtonStyle.SUCCESS)
        ),
        
        Separator(visible=False),  # Espaçamento invisível
        
        Section(
            TextDisplay("**📊 Ranking**"),
            TextDisplay("Ver o ranking de jogadores"),
            accessory=Button("Ver Ranking", "rank_btn", style=hikari.ButtonStyle.PRIMARY)
        ),
        
        Separator(visible=False),
        
        Section(
            TextDisplay("**⚙️ Configurações**"),
            TextDisplay("Ajustar suas preferências"),
            accessory=Button("Configurar", "settings_btn", style=hikari.ButtonStyle.SECONDARY)
        ),
        
        Separator(visible=False),
        
        Section(
            TextDisplay("**❓ Ajuda**"),
            TextDisplay("Aprenda como jogar"),
            accessory=LinkButton("Tutorial", "https://example.com/tutorial")
        ),
        
        accent_color="#5865F2"
    )
    
    await ctx.respond(
        component=container.build(),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2
    )


# ============================================================================
# Handler para os botões
# ============================================================================

@bot.listen()
async def on_interaction(event: hikari.InteractionCreateEvent):
    """Handle button clicks."""
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    
    custom_id = event.interaction.custom_id
    
    responses = {
        "start_btn": "✅ Você começou!",
        "info_btn": "ℹ️ Aqui estão mais informações...",
        "action_btn": "⚡ Ação executada com sucesso!",
        "config_btn": "⚙️ Abrindo configurações...",
        "stats_btn": "📊 Carregando estatísticas...",
        "try_btn": "🎉 Experimentando a nova funcionalidade!",
        "ack_btn": "✅ Notificação confirmada!",
        "play_btn": "🎮 Iniciando jogo...",
        "rank_btn": "📊 Carregando ranking...",
        "settings_btn": "⚙️ Abrindo configurações...",
    }
    
    if custom_id in responses:
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            responses[custom_id],
            flags=hikari.MessageFlag.EPHEMERAL
        )
    elif custom_id.startswith("dm_"):
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "📨 Funcionalidade de DM não implementada neste exemplo.",
            flags=hikari.MessageFlag.EPHEMERAL
        )


if __name__ == "__main__":
    print("🚀 Bot iniciado!")
    print("📝 Comandos disponíveis:")
    print("  /section_button      - Section com botão")
    print("  /section_link        - Section com link")
    print("  /section_thumb       - Section com thumbnail")
    print("  /multiple_sections   - Várias sections")
    print("  /section_container   - Section em container")
    print("  /section_fancy       - Section estilizada")
    print("  /user_profile        - Perfil com section")
    print("  /notification        - Notificação")
    print("  /menu                - Menu com sections")
    bot.run()
