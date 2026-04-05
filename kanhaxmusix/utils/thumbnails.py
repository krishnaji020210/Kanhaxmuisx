import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL
from ShashankMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def trim(text, font, max_w):
    try:
        while font.getbbox(text)[2] > max_w:
            text = text[:-1]
        return text + "..."
    except:
        return text


async def gen_thumb(videoid: str, player_username=None):
    if player_username is None:
        player_username = getattr(app, "username", "MusicBot")

    path = f"{CACHE_DIR}/{videoid}_final.png"
    if os.path.exists(path):
        return path

    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        res = await results.next()

        if not res.get("result"):
            raise ValueError

        data = res["result"][0]

        title = data.get("title", "Unknown")
        thumb_url = data.get("thumbnails", [{}])[0].get("url", YOUTUBE_IMG_URL)
        duration = data.get("duration", "Live")
        views = data.get("viewCount", {}).get("short", "0")
        channel = data.get("channel", {}).get("name", "Unknown Artist")

    except:
        title, thumb_url, duration, views, channel = (
            "Unknown",
            YOUTUBE_IMG_URL,
            "Live",
            "0",
            "Unknown Artist",
        )

    thumb_path = f"{CACHE_DIR}/{videoid}.png"

    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(thumb_url) as r:
                if r.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await r.read())
                else:
                    thumb_path = None
    except:
        thumb_path = None

    # =========================
    # MAIN BG
    # =========================
    bg = Image.new("RGB", (1280, 720), (5, 5, 5))

    glow = Image.new("RGB", (1280, 720), (0, 0, 0))
    g = ImageDraw.Draw(glow)

    # orange-red cinematic glows
    g.ellipse((650, 50, 1250, 650), fill=(120, 30, 10))
    g.ellipse((750, 120, 1180, 520), fill=(255, 90, 30))
    g.ellipse((150, 80, 700, 650), fill=(40, 10, 10))

    glow = glow.filter(ImageFilter.GaussianBlur(180))
    bg = Image.blend(bg, glow, 0.55)

    draw = ImageDraw.Draw(bg)

    # =========================
    # THUMB / ALBUM BOX
    # =========================
    try:
        thumb = Image.open(thumb_path).convert("RGBA").resize((420, 420))
    except:
        thumb = Image.new("RGBA", (420, 420), (25, 25, 25, 255))

    # rounded mask
    mask = Image.new("L", (420, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 420, 420), 35, fill=255)
    thumb.putalpha(mask)

    # outer dark shadow card
    shadow = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((0, 0, 500, 500), 50, fill=(35, 25, 25, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    bg.paste(shadow, (70, 115), shadow)

    # white rounded border
    border = Image.new("RGBA", (440, 440), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((0, 0, 440, 440), 38, outline=(255, 255, 255), width=4)

    bg.paste(thumb, (100, 145), thumb)
    bg.paste(border, (90, 135), border)

    # =========================
    # FONTS
    # =========================
    try:
        title_font = ImageFont.truetype("ShashankMusic/assets/font.ttf", 62)
        meta_font = ImageFont.truetype("ShashankMusic/assets/font.ttf", 34)
        small_font = ImageFont.truetype("ShashankMusic/assets/font.ttf", 26)
        dev_font = ImageFont.truetype("ShashankMusic/assets/font.ttf", 24)
    except:
        title_font = meta_font = small_font = dev_font = ImageFont.load_default()

    # =========================
    # RIGHT SIDE TEXT
    # =========================
    title = trim(title, title_font, 560)

    # main title
    draw.text((620, 220), title, fill="white", font=title_font)

    # artist / views
    draw.text((620, 315), f"Artist: {channel}", fill=(210, 210, 210), font=meta_font)
    draw.text((620, 365), f"Views: {views} views", fill=(170, 170, 170), font=meta_font)

    # =========================
    # PROGRESS BAR
    # =========================
    bar_x, bar_y = 620, 470
    bar_w = 560

    # bar line
    draw.rounded_rectangle(
        (bar_x, bar_y, bar_x + bar_w, bar_y + 8),
        10,
        fill=(235, 235, 235)
    )

    # progress dot
    progress_x = bar_x + int(bar_w * 0.48)
    draw.ellipse(
        (progress_x - 10, bar_y - 8, progress_x + 10, bar_y + 12),
        fill="white"
    )

    # time text
    draw.text((620, 515), "01:20", fill=(180, 180, 180), font=meta_font)
    draw.text((1110, 515), duration, fill=(180, 180, 180), font=meta_font)

    # =========================
    # DEV TAG BOTTOM RIGHT
    # =========================
    dev_text = f"ᴅᴇᴠ :• @{player_username}"

    # glow text
    glow_layer = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.text((1030, 660), dev_text, fill=(255, 255, 255, 120), font=dev_font)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(6))
    bg.paste(glow_layer, (0, 0), glow_layer)

    # main dev text
    draw.text((1030, 660), dev_text, fill=(230, 230, 230), font=dev_font)

    # =========================
    # CLEANUP
    # =========================
    try:
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path


# =========================
# MAIN FIX
# =========================
async def get_thumb(videoid: str, user_id=None):
    username = getattr(app, "username", "rustam")
    return await gen_thumb(videoid, player_username=username)
