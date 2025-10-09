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