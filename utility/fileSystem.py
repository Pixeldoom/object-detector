import sys
import os


class FileSystem:
    """
    Класс-утилита для работы с файловой системой
    """

    @classmethod
    def toUnixPath(cls, path: str):
        """
        Преобразует путь к файлу в Unix-формат (заменяет обратные слеши на прямые).

        :param path: Исходный путь (строка)
        :return: Путь в Unix-формате
        """
        return path.replace("\\", "/")

    @classmethod
    def resourcePath(cls, relativePath: str):
        """
        Получает абсолютный путь к ресурсу, работает как для исходного кода,
        так и для собранного в .exe приложения.
        """
        try:
            # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")

        return os.path.join(basePath, relativePath)