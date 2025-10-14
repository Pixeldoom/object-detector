import cv2
import csv
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow
from view.mainWindow import Ui_MainWindow
from export.csvExporter import CSVExporter
from utility.image import Image as ImageUtility
from utility.fileSystem import FileSystem as FileSystemUtility


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._selectedExampleImagePath = None
        self._selectedSearchImagePath = None
        self._resultImage = None
        self._matchLocation = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.selectExampleImageButton.clicked.connect(self.onSelectExamplaeImageButtonClicked)
        self.ui.selectSearchImageButton.clicked.connect(self.onSelectSearchImageButtonClicked)
        self.ui.runButton.clicked.connect(self.onRunButtonClicked)
        self.ui.saveResultTableButton.clicked.connect(self.onSaveResultTableButtonClicked)
        self.ui.saveResultImageButton.clicked.connect(self.onSaveResultImageButtonClicked)

    def onSelectExamplaeImageButtonClicked(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Выберите изображение образца для поиска",
            filter=f"Изображения ({' '.join(f'*.{ext}' for ext in ImageUtility.allowedTypes)});;Все файлы (*)"
        )

        if not filePath:
            return

        filePath = FileSystemUtility.toUnixPath(filePath)

        try:
            if not ImageUtility.checkIsImage(filePath):
                raise Exception("Файл не найден или он не является изображением")
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', err.__str__())
            return

        self._selectedExampleImagePath = filePath

        self.ui.exampleImageLabel.setPixmap(
            QtGui.QPixmap(filePath).scaled(
                self.ui.exampleImageLabel.width(),
                self.ui.exampleImageLabel.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def onSelectSearchImageButtonClicked(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Выберите изображение, на котором будет выполняться поиск образца",
            filter=f"Изображения ({' '.join(f'*.{ext}' for ext in ImageUtility.allowedTypes)});;Все файлы (*)"
        )

        if not filePath:
            return

        filePath = FileSystemUtility.toUnixPath(filePath)

        try:
            if not ImageUtility.checkIsImage(filePath):
                raise Exception("Файл не найден или он не является изображением")
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', err.__str__())
            return

        self._selectedSearchImagePath = filePath

        self.ui.searchImageLabel.setPixmap(
            QtGui.QPixmap(filePath).scaled(
                self.ui.searchImageLabel.width(),
                self.ui.searchImageLabel.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def onRunButtonClicked(self):
        if not self._selectedExampleImagePath or not self._selectedSearchImagePath:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите оба изображения.")
            return

        try:
            template = ImageUtility.readUnicode(self._selectedExampleImagePath)
            image = ImageUtility.readUnicode(self._selectedSearchImagePath)

            if template is None or image is None:
                raise Exception("Не удалось загрузить одно из изображений.")

            templateHeight, templateWidth = template.shape[:2]
            imageHeight, imageWidth = image.shape[:2]


            if templateHeight > imageHeight or templateWidth > imageWidth:
                raise Exception("Изображение-образец больше, чем изображение для поиска.")

            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            _, maxVal, _, maxLoc = cv2.minMaxLoc(result)

            threshold = 0.4
            if maxVal < threshold:
                QtWidgets.QMessageBox.information(self, "Результат", "Образец не найден на изображении.")
                return

            bottomRight = (maxLoc[0] + templateWidth, maxLoc[1] + templateHeight)

            resultImage = image.copy()
            cv2.rectangle(resultImage, maxLoc, bottomRight, (0, 255, 0), 2)

            self._resultImage = resultImage
            self._matchLocation = (maxLoc, bottomRight, maxVal)

            resultImageRGB = cv2.cvtColor(resultImage, cv2.COLOR_BGR2RGB)
            h, w, ch = resultImageRGB.shape
            bytesPerLine = ch * w
            qImg = QtGui.QImage(resultImageRGB.data, w, h, bytesPerLine, QtGui.QImage.Format.Format_RGB888)

            pixmap = QtGui.QPixmap.fromImage(qImg).scaled(
                self.ui.resultImageLabel.width(),
                self.ui.resultImageLabel.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.resultImageLabel.setPixmap(pixmap)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def onSaveResultTableButtonClicked(self):
        if not hasattr(self, '_matchLocation') or self._matchLocation is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта. Сначала выполните поиск.")
            return

        topLeft, bottomRight, maxVal = self._matchLocation

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Сохранить результаты поиска",
            filter="CSV файлы (*.csv);;Все файлы (*)"
        )

        if not filePath:
            return

        if not filePath.lower().endswith('.csv'):
            filePath += '.csv'

        try:
            CSVExporter.exportMatchResult(filePath, topLeft, bottomRight, maxVal)

            QtWidgets.QMessageBox.information(self, "Успех", f"Результаты сохранены в:\n{filePath}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить CSV:\n{str(e)}")

    def onSaveResultImageButtonClicked(self):
        if self._resultImage is None or self._resultImage.size == 0:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет результата для сохранения. Сначала выполните поиск.")
            return

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Сохранить результат поиска",
            filter=f"Изображения ({' '.join(f'*.{ext}' for ext in ImageUtility.allowedTypes)});;Все файлы (*)"
        )

        if not filePath:
            return  # Отмена

        if not filePath.lower().endswith(tuple(ImageUtility.allowedTypes)):
            filePath += '.png'

        try:
            success = ImageUtility.writeUnicode(filePath, self._resultImage)
            if not success:
                raise Exception("Не удалось записать файл изображения.")
            QtWidgets.QMessageBox.information(self, "Успех", f"Изображение сохранено:\n{filePath}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении изображения:\n{str(e)}")