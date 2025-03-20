import discord
import os
import threading
from discord.ext import commands
from flask import Flask
from dotenv import load_dotenv
from modules import greetings, news  # Importar correctamente

# Cargar variables de entorno
load_dotenv()

# Configurar intents del bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Inicializar el bot
bot = commands.Bot(command_prefix='/', intents=intents)

# Cargar módulos del bot
greetings.setup(bot)
news.setup(bot)

# Crear servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Discord bot is running'

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user.name} is online and ready!')

@bot.event
async def on_command_error(ctx, error):
    print(f"⚠️ Error: {error}")

def run_bot():
    """Función para iniciar el bot de Discord."""
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("⚠️ Missing BOT_TOKEN in .env file")
        return
    bot.run(TOKEN)

def run_server():
    """Función para iniciar el servidor Flask en un hilo separado."""
    app.run(host="localhost", port=5080, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Iniciar Flask en un hilo separado para que no bloquee la ejecución del bot
    threading.Thread(target=run_server, daemon=True).start()
    
    # Iniciar el bot
    run_bot()
