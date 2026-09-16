import discord
from discord.ext import commands
from typing import Optional, Callable, Any

class PaginatedView(discord.ui.View):
    """Paginated embed view with next/previous buttons."""
    
    def __init__(self, embeds: list[discord.Embed], timeout: int = 180):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0
    
    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Previous page button."""
        if self.current_page > 0:
            self.current_page -= 1
        else:
            self.current_page = len(self.embeds) - 1
        
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Next page button."""
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        else:
            self.current_page = 0
        
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

class ConfirmView(discord.ui.View):
    """Simple yes/no confirmation view."""
    
    def __init__(self, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.result: Optional[bool] = None
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Confirm button."""
        self.result = True
        self.stop()
        await interaction.response.defer()
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Cancel button."""
        self.result = False
        self.stop()
        await interaction.response.defer()