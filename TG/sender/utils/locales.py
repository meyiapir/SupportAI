# Load the translations
import gettext

from sender.core.config import settings

def translate(lang):
    translation = gettext.translation('messages', settings.LOCALES_DIR, languages=[lang])
    translation.install()

    return translation.gettext
