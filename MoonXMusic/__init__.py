from MoonXMusic.core.bot import Moony
from MoonXMusic.core.dir import dirr
from MoonXMusic.core.userbot import Userbot
from MoonXMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
dbb()
heroku()

app = Moony()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
