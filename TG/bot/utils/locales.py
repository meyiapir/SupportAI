import gettext

from bot.core.config import settings


def get_flag_emoji(country_code: str) -> str:
    if country_code == 'en':
        country_code = 'us'
    elif country_code == 'uk':
        country_code = 'ua'
    """
    Retrieve the flag emoji by country code.

    Args:
    - country_code (str): The two-letter country code (ISO 3166-1 alpha-2).

    Returns:
    - str: The flag emoji corresponding to the country code, or None if not found.
    """
    # Offset between uppercase ASCII characters and Regional Indicator Symbols
    OFFSET = ord('🇦') - ord('A')

    # Convert the country code to uppercase
    country_code = country_code.upper()

    # Check if the input country code is valid (2 uppercase letters)
    if len(country_code) != 2 or not country_code.isalpha():
        print("Invalid country code.")
        return None

    # Calculate the Unicode code point for the first letter of the country code
    code_point_1 = ord(country_code[0]) + OFFSET
    # Calculate the Unicode code point for the second letter of the country code
    code_point_2 = ord(country_code[1]) + OFFSET

    # Construct the flag emoji using the Regional Indicator Symbols
    flag_emoji = chr(code_point_1) + chr(code_point_2)

    return flag_emoji


def translate(msg_id, language):
    if language not in settings.LANGUAGES:
        language = 'en'
    translation = gettext.translation(settings.I18N_DOMAIN, languages=[language], localedir=settings.LOCALES_DIR)
    return translation.gettext(msg_id)


def get_all_locales(msg_id):
    return [translate(msg_id, language) for language in settings.LANGUAGES]
