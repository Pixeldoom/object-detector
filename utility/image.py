import os
import cv2
import imghdr
import numpy as np
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

    @classmethod
    def readUnicode(cls, path: str):
        with open(path, "rb") as f:
            data = f.read()
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    @classmethod
    def writeUnicode(cls, path, img):
        isSuccess, buffer = cv2.imencode(os.path.splitext(path)[1], img)
        if isSuccess:
            with open(path, "wb") as f:
                f.write(buffer.tobytes())
            return True
        return False