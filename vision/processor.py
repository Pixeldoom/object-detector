import cv2
import numpy as np

class VisionProcessor:
    """
    Класс, инкапсулирующий различные методы компьютерного зрения.
    """

    @staticmethod
    def findObjectsByHaar(image: np.ndarray, cascadeXmlPath: str):
        """
        Находит объекты с помощью каскада Хаара (например, лица, глаза).

        :param image: Изображение для поиска (в формате OpenCV).
        :param cascadeXmlPath: Путь к XML-файлу каскада.
        :return: Список кортежей с координатами (x, y, w, h) для каждого найденного объекта.
        """
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascadeXmlPath)
        # Параметры можно настраивать для лучшей точности
        objects = cascade.detectMultiScale(
            grayImage,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return objects

    @staticmethod
    def findObjectByFeatures(template: np.ndarray, image: np.ndarray):
        """
        Находит образец на изображении с помощью сопоставления ключевых точек (ORB).
        Этот метод устойчив к повороту и масштабу.

        :param template: Изображение-образец.
        :param image: Изображение для поиска.
        :return: Координаты углов найденного объекта или None, если ничего не найдено.
        """
        # Инициализация детектора ORB
        orb = cv2.ORB_create(nfeatures=1000)

        # Находим ключевые точки и дескрипторы
        kp1, des1 = orb.detectAndCompute(template, None)
        kp2, des2 = orb.detectAndCompute(image, None)

        if des1 is None or des2 is None:
            return None

        # Сопоставляем дескрипторы с помощью Brute-Force Matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Сортируем их по расстоянию (чем меньше, тем лучше)
        matches = sorted(matches, key=lambda x: x.distance)

        # Берем лучшие 15 совпадений (можно настроить)
        goodMatches = matches[:15]

        # Минимальное количество совпадений для поиска
        MIN_MATCH_COUNT = 10
        if len(goodMatches) < MIN_MATCH_COUNT:
            return None

        # Извлекаем координаты совпавших точек
        srcPts = np.float32([kp1[m.queryIdx].pt for m in goodMatches]).reshape(-1, 1, 2)
        dstPts = np.float32([kp2[m.trainIdx].pt for m in goodMatches]).reshape(-1, 1, 2)

        # Находим матрицу гомографии, чтобы определить положение образца
        M, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)

        if M is None:
            return None

        # Получаем углы образца
        h, w = template.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        # Преобразуем углы в соответствии с найденным положением на большом изображении
        dst = cv2.perspectiveTransform(pts, M)

        return np.int32(dst)