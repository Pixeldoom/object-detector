import csv
from pathlib import Path
from typing import Tuple

class CSVExporter:
    """
    Класс для экспорта результатов поиска образца в CSV-файл.
    """

    @staticmethod
    def exportMatchResult(
        filePath: str,
        topLeft: Tuple[int, int],
        bottomRight: Tuple[int, int],
        confidence: float
    ) -> None:
        """
        Экспортирует одно совпадение в CSV-файл.

        :param filePath: Путь для сохранения CSV (поддерживает Unicode)
        :param topLeft: (x, y) координаты верхнего левого угла
        :param bottomRight: (x, y) координаты нижнего правого угла
        :param confidence: Уверенность совпадения (0.0 – 1.0)
        :raises IOError: Если не удалось записать файл
        """
        # Убедимся, что родительская директория существует
        Path(filePath).parent.mkdir(parents=True, exist_ok=True)

        with open(filePath, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Top_Left_X", "Top_Left_Y",
                "Bottom_Right_X", "Bottom_Right_Y",
                "Confidence"
            ])
            writer.writerow([
                topLeft[0], topLeft[1],
                bottomRight[0], bottomRight[1],
                f"{confidence:.6f}"
            ])