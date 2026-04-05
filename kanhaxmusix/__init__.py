# -----------------------------------------------
# 🔸 kanhaxmuisx Project
# 🔹 Developed & Maintained by: KRISHNA (https://github.com/krishnaji020210)
# 📅 Copyright © 2025 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by KRISHNA
# -----------------------------------------------

from kanhaxmusix.core.bot import Shashank
from kanhaxmusix.core.dir import dirr
# from kanhaxmusix.core.git import git
from kanhaxmusix.core.userbot import Userbot
from kanhaxmusix.misc import dbb, heroku

from .logging import LOGGER

dirr()
#git()
dbb()
heroku()

app = kanha()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

