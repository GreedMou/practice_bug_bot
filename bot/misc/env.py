from os import environ
from typing import Final


class TgKeys:
    TOKEN: Final = environ.get('TOKEN', 'define me!')
    DB_HOST: Final = environ.get('DB_HOST', 'define me!')
    DB_USER: Final = environ.get('DB_USER', 'define me!')
    DB_PASS: Final = environ.get('DB_PASS', 'define me!')
    DB_NAME: Final = environ.get('DB_NAME', 'define me!')
