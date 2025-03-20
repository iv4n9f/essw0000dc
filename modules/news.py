import discord
import feedparser
from discord.ext import commands, tasks

# Diccionario para evitar enviar noticias duplicadas
sent_articles = {}

# Diccionario de categorías con múltiples fuentes RSS
rss_feeds = {
    "Technology": [
        "https://www.wired.com/feed/rss",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    ],
    "Sports": [
        "https://www.espn.com/espn/rss/news",
        "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml"
    ],
    "Science": [
        "https://www.sciencenews.org/feed",
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"
    ],
    "World News": [
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    ],
    "Anime": [
        "https://www.crunchyroll.com/rss/anime",
        "https://www.animenewsnetwork.com/news/rss.xml"
    ],
    "Business": [
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
    ]
}

# Diccionario que asigna un canal de Discord a cada categoría
category_channels = {
    "Technology": 1309126232436117555,
    "Sports": 1309132071368786013,
    "Science": 1351890919896649828,
    "World News": 1351890959733887039,
    "Anime": 1309140126458314862,
    "Business": 1351891000141938780
}

# Diccionario de colores para cada categoría
category_colors = {
    "Technology": discord.Color.blue(),
    "Sports": discord.Color.red(),
    "Science": discord.Color.green(),
    "World News": discord.Color.gold(),
    "Anime": discord.Color.purple(),
    "Business": discord.Color.orange()
}

def parse_feed(feed_url):
    """Parsea el feed RSS y devuelve una lista de artículos."""
    feed = feedparser.parse(feed_url)
    articles = []
    
    for entry in feed.entries[:3]:  # Tomamos solo las 3 últimas noticias para evitar spam
        article = {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary if hasattr(entry, "summary") else "No summary available",
            "published": entry.published if hasattr(entry, "published") else "Unknown date"
        }
        articles.append(article)
    
    return articles

async def send_article(bot, article, category):
    """Envia un artículo al canal correspondiente."""
    embed = discord.Embed(
        title=f"📰 {category}: {article['title']}",
        description=article["summary"][:500] + "...",
        url=article["link"],
        color=category_colors.get(category, discord.Color.default())
    )
    embed.set_footer(text=f"Published: {article['published']}")

    channel_id = category_channels.get(category)
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)
        else:
            print(f"⚠️ Error: No se encontró el canal ID {channel_id} para {category}.")
    else:
        print(f"⚠️ Advertencia: No hay un canal asignado para la categoría {category}.")

async def send_latest_news(bot):
    """Envía las últimas noticias al iniciar el bot."""
    for category, feeds in rss_feeds.items():
        for feed_url in feeds:
            articles = parse_feed(feed_url)
            
            for article in articles:
                await send_article(bot, article, category)  # Enviar la noticia inmediatamente
                sent_articles[article["link"]] = True  # Marcar como enviada

def setup(bot):
    @tasks.loop(minutes=5)
    async def check_rss():
        """Verifica cada 5 minutos si hay nuevas noticias y las envía."""
        for category, feeds in rss_feeds.items():
            for feed_url in feeds:
                articles = parse_feed(feed_url)
                
                for article in articles:
                    if article["link"] not in sent_articles:
                        await send_article(bot, article, category)
                        sent_articles[article["link"]] = True  # Marcar como enviada

    @bot.event
    async def on_ready():
        """Al iniciar el bot, envía noticias iniciales y arranca el loop de monitoreo."""
        print("✅ Bot is ready. Sending latest news...")
        await send_latest_news(bot)  # Enviar noticias iniciales al arrancar
        
        if not check_rss.is_running():
            check_rss.start()
            print("✅ RSS feed monitoring started!")
