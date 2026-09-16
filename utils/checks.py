import discord
from discord.ext import commands
from typing import Optional
from config import Config

config = Config()

def is_owner() -> commands.check:
    """Check if user is bot owner."""
    async def predicate(ctx: commands.Context) -> bool:
        return ctx.author.id in config.OWNER_IDS
    return commands.check(predicate)

def is_admin() -> commands.check:
    """Check if user has admin permissions."""
    async def predicate(ctx: commands.Context) -> bool:
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def is_moderator() -> commands.check:
    """Check if user has moderator permissions."""
    async def predicate(ctx: commands.Context) -> bool:
        return ctx.author.guild_permissions.moderate_members or ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def has_permissions(**perms) -> commands.check:
    """Check if user has specific permissions."""
    async def predicate(ctx: commands.Context) -> bool:
        return all(getattr(ctx.author.guild_permissions, perm, False) for perm in perms)
    return commands.check(predicate)