from configparser import ConfigParser
from typing import Dict


def config(
    filename: str = "database.ini", section: str = "postgresql"
) -> Dict[str, str]:
    """Читает конфигурационные параметры базы данных из файла.
    Функция парсит указанный файл конфигурации и извлекает параметры
    для подключения к базе данных из заданной секции."""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found in the {filename} file.")

    return db
