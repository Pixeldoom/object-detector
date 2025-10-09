import os
import imghdr
from utility.fileSystem import FileSystem as FileSystemUtility


class Image:
    """
    Класс-хелпер для работы с изображениями
    """

    allowedTypes = {"png", "jpg", "jpeg", "bmp"}

    @classmethod
    def checkIsImage(cls, filePath) -> bool:
        """
        Метод для проверки того, является файл изображением или нет

        :param filePath: путь до предполагаемого файла
        :return:
        :rtype: bool
        """

        FileSystemUtility.toUnixPath(filePath)

        if not os.path.exists(filePath):
            return False

        # Определение типа файла
        imageType = imghdr.what(filePath)

        return bool(imageType in cls.allowedTypes)