"""
Example demonstrating the new ModalBuilder API for OnyxCord.

This example shows how to use the declarative ModalBuilder to create modals
with all the new Discord components in a clean, single-variable syntax.
"""

import hikari
import miru
from miru.onyx import (
    OnyxModal,
    ModalBuilder,
    Text,
    File,
    Radio,
    CheckboxGroupField,
    CheckboxField,
    install_modal_handler,
)

# Create bot
bot = hikari.GatewayBot(token="YOUR_TOKEN_HERE")
client = miru.Client(bot)

# Install OnyxCord modal handler
install_modal_handler(bot)


# ============================================================================
# EXAMPLE 1: Complete Form with All Components
# ============================================================================

class CompleteFormModal(OnyxModal, title="Complete Form"):
    """Modal with all component types using ModalBuilder."""
    
    # 🚀 ONE VARIABLE - ALL COMPONENTS!
    modal = ModalBuilder(
        # 📝 Text Input
        Text(
            label="Name",
            custom_id="name",
            placeholder="Enter your name...",
            required=True,
        ),
        
        # 📝 Multi-line Text
        Text(
            label="Description",
            custom_id="description",
            placeholder="Describe your issue...",
            style=hikari.TextInputStyle.PARAGRAPH,
            max_length=500,
        ),
        
        # 📁 File Upload
        File(
            custom_id="files",
            label="Attachments",
            max=3,
            file_types=["image/*", ".pdf", ".docx"],
        ),
        
        # 🔘 Radio Group (single choice)
        Radio(
            custom_id="priority",
            label="Priority Level",
            options=[
                ("🟢 Low", "low"),
                ("🟡 Medium", "medium"),
                ("🔴 High", "high"),
                ("🚨 Critical", "critical"),
            ],
            required=True,
        ),
        
        # ☑️ Checkbox Group (multiple choice)
        CheckboxGroupField(
            custom_id="features",
            label="Affected Features",
            options=[
                ("API", "api"),
                ("UI", "ui"),
                ("Database", "db"),
                ("Authentication", "auth"),
            ],
        ),
        
        # ✅ Single Checkbox
        CheckboxField(
            custom_id="confirm",
            label="I have read the guidelines",
            required=True,
        ),
    )
    
    async def callback(self, ctx: miru.ModalContext) -> None:
        """Handle form submission."""
        # 🎯 Get all values with ONE line!
        data = self.modal.get(self)
        
        # Build response
        response = f"""
**Form Submitted Successfully!**

**Name:** {data.name}
**Description:** {data.description or 'N/A'}
**Priority:** {data.priority}
**Features:** {', '.join(data.features) if data.features else 'None'}
**Confirmed:** {'✅ Yes' if data.confirm else '❌ No'}
**Files:** {len(data.files or [])} file(s) uploaded
"""
        
        # Add file links if any
        if data.files:
            response += "\n**Uploaded Files:**\n"
            for file in data.files:
                response += f"- [{file.filename}]({file.url}) ({file.size} bytes)\n"
        
        await ctx.respond(response, flags=hikari.MessageFlag.EPHEMERAL)


# ============================================================================
# EXAMPLE 2: Simple Feedback Form
# ============================================================================

class FeedbackModal(OnyxModal, title="Quick Feedback"):
    """Simple feedback form."""
    
    modal = ModalBuilder(
        Text(
            label="Your Name",
            custom_id="name",
            placeholder="John Doe",
            required=True,
        ),
        Radio(
            custom_id="rating",
            label="How would you rate us?",
            options=[
                ("⭐ Poor", "1"),
                ("⭐⭐ Fair", "2"),
                ("⭐⭐⭐ Good", "3"),
                ("⭐⭐⭐⭐ Great", "4"),
                ("⭐⭐⭐⭐⭐ Excellent", "5"),
            ],
            required=True,
        ),
        Text(
            label="Comments",
            custom_id="comments",
            placeholder="Tell us more...",
            style=hikari.TextInputStyle.PARAGRAPH,
        ),
        CheckboxField(
            custom_id="newsletter",
            label="Subscribe to newsletter",
        ),
    )
    
    async def callback(self, ctx: miru.ModalContext) -> None:
        data = self.modal.get(self)
        
        stars = "⭐" * int(data.rating)
        newsletter = "Yes" if data.newsletter else "No"
        
        await ctx.respond(
            f"Thanks {data.name}!\n"
            f"Rating: {stars}\n"
            f"Comments: {data.comments or 'None'}\n"
            f"Newsletter: {newsletter}",
            flags=hikari.MessageFlag.EPHEMERAL
        )


# ============================================================================
# EXAMPLE 3: Bug Report Form
# ============================================================================

class BugReportModal(OnyxModal, title="Report a Bug"):
    """Bug report form with file upload."""
    
    modal = ModalBuilder(
        Text(
            label="Bug Title",
            custom_id="title",
            placeholder="Brief description of the bug",
            required=True,
            max_length=100,
        ),
        Text(
            label="Steps to Reproduce",
            custom_id="steps",
            placeholder="1. Go to...\n2. Click on...\n3. See error",
            style=hikari.TextInputStyle.PARAGRAPH,
            required=True,
        ),
        Radio(
            custom_id="severity",
            label="Severity",
            options=[
                ("Minor", "minor"),
                ("Moderate", "moderate"),
                ("Major", "major"),
                ("Critical", "critical"),
            ],
            required=True,
        ),
        File(
            custom_id="screenshot",
            label="Screenshot",
            max=2,
            file_types=["image/*"],
        ),
        CheckboxGroupField(
            custom_id="platforms",
            label="Affected Platforms",
            options=[
                ("Windows", "windows"),
                ("macOS", "macos"),
                ("Linux", "linux"),
                ("Mobile", "mobile"),
            ],
        ),
    )
    
    async def callback(self, ctx: miru.ModalContext) -> None:
        data = self.modal.get(self)
        
        embed = hikari.Embed(
            title=f"🐛 Bug Report: {data.title}",
            description=data.steps,
            color=hikari.Color(0xFF0000),
        )
        embed.add_field("Severity", data.severity.upper(), inline=True)
        embed.add_field(
            "Platforms",
            ", ".join(data.platforms) if data.platforms else "Not specified",
            inline=True
        )
        
        if data.screenshot:
            embed.add_field(
                "Screenshots",
                f"{len(data.screenshot)} file(s) attached",
                inline=False
            )
        
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


# ============================================================================
# Commands to trigger modals
# ============================================================================

@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    """Listen for commands to open modals."""
    if not event.is_human:
        return
    
    content = event.content
    if not content:
        return
    
    # Create a button to open the modal
    if content.lower() == "!form":
        view = miru.View()
        view.add_item(
            miru.Button(label="Open Complete Form", custom_id="open_complete")
        )
        view.add_item(
            miru.Button(label="Give Feedback", custom_id="open_feedback", style=hikari.ButtonStyle.SUCCESS)
        )
        view.add_item(
            miru.Button(label="Report Bug", custom_id="open_bug", style=hikari.ButtonStyle.DANGER)
        )
        
        message = await event.message.respond(
            "Click a button to open a modal:",
            components=view
        )
        client.start_view(view)


@bot.listen()
async def on_interaction(event: hikari.InteractionCreateEvent) -> None:
    """Handle button clicks to open modals."""
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    
    custom_id = event.interaction.custom_id
    
    if custom_id == "open_complete":
        modal = CompleteFormModal()
        await modal.send(event.interaction)
    
    elif custom_id == "open_feedback":
        modal = FeedbackModal()
        await modal.send(event.interaction)
    
    elif custom_id == "open_bug":
        modal = BugReportModal()
        await modal.send(event.interaction)


# ============================================================================
# Run the bot
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting bot with ModalBuilder examples...")
    print("📝 Type !form in any channel to see the examples")
    bot.run()
