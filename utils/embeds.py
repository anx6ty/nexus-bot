import discord
from typing import Optional, List
from config import Config

config = Config()

class Embeds:
    """Centralized embed builder for consistent styling."""
    
    @staticmethod
    def success(title: str = "Success", description: str = "", **kwargs) -> discord.Embed:
        """Create a success embed."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=config.Color.SUCCESS,
            **kwargs
        )
        embed.set_footer(text="Nexus Bot")
        return embed
    
    @staticmethod
    def error(title: str = "Error", description: str = "", **kwargs) -> discord.Embed:
        """Create an error embed."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=config.Color.ERROR,
            **kwargs
        )
        embed.set_footer(text="Nexus Bot")
        return embed
    
    @staticmethod
    def warning(title: str = "Warning", description: str = "", **kwargs) -> discord.Embed:
        """Create a warning embed."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=config.Color.WARNING,
            **kwargs
        )
        embed.set_footer(text="Nexus Bot")
        return embed
    
    @staticmethod
    def info(title: str = "Info", description: str = "", **kwargs) -> discord.Embed:
        """Create an info embed."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=config.Color.INFO,
            **kwargs
        )
        embed.set_footer(text="Nexus Bot")
        return embed
    
    @staticmethod
    def main(title: str = "", description: str = "", **kwargs) -> discord.Embed:
        """Create a main theme embed (dark seamless)."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=config.Color.MAIN,
            **kwargs
        )
        embed.set_footer(text="Nexus Bot")
        return embed