import discord
from discord import app_commands
from discord.ext import commands

# Remplacez ceci par votre token secret (ne partagez pas ce token)
TOKEN = ""

# Crée une instance du bot
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True  # Autorise l'accès aux messages
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f'Bot connecté en tant que {self.user}')
        await self.tree.sync()  # Synchroniser l'arbre de commandes lorsque le bot est prêt

# Vérifie si l'utilisateur est administrateur
def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

# Instanciez le bot
bot = MyBot()

# Commande /make_bot
@bot.tree.command(name="make_bot")
@app_commands.describe(
    slash="Utiliser des commandes slash ?",
    clear="Inclure la commande clear ?",
    clear_admin="Inclure la commande clear_admin ?",
    prefix="Définir un préfix personnalisé"
)
async def make_bot(interaction: discord.Interaction, slash: int = 0, clear: int = 0, clear_admin: int = 0, prefix: str = "!"):
    # Création du squelette du bot
    bot_code = f"""
```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="{prefix}")

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {{bot.user}}")

"""

    # Si slash est 1, ajoute les commandes slash, sinon ajoute les commandes normales
    if slash == 1:
        if clear == 1:
            bot_code += f"""
@bot.tree.command()
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"J'ai supprimé {{amount}} messages.", ephemeral=True)

"""
        if clear_admin == 1:
            bot_code += f"""
@bot.tree.command()
@commands.has_permissions(administrator=True)
async def clear_admin(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"J'ai supprimé {{amount}} messages (admin).", ephemeral=True)

"""
        if clear == 1:
            bot_code += f"""
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"J'ai supprimé {{amount}} messages.")

"""
        if clear_admin == 1:
            bot_code += f"""
@bot.command()
@commands.has_permissions(administrator=True)
async def clear_admin(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"J'ai supprimé {{amount}} messages (admin).")

"""

    # Répondre à l'interaction
    await interaction.response.send_message("Voici le code généré :", ephemeral=True)
    await interaction.followup.send(f"```python\n{bot_code}\n```", ephemeral=True)

# Démarrer le bot
bot.run(TOKEN)
