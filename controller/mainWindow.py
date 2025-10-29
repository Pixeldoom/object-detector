import cv2
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtGui
from view.mainWindow import Ui_MainWindow
from vision.processor import VisionProcessor
from utility.image import Image as ImageUtility
from PySide6.QtWidgets import QMainWindow, QMessageBox
from utility.fileSystem import FileSystem as FileSystemUtility


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._selectedExampleImagePath = None
        self._selectedSearchImagePath = None
        self._resultImage = None
        self._matchLocation = None
        self._foundObjects = []

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
            QMessageBox.critical(self, 'Ошибка', err.__str__())
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
            QMessageBox.critical(self, 'Ошибка', err.__str__())
            return

        self._selectedSearchImagePath = filePath
        self._resultImage = None
        self._foundObjects = []

        self.ui.searchImageLabel.setPixmap(
            QtGui.QPixmap(filePath).scaled(
                self.ui.searchImageLabel.width(),
                self.ui.searchImageLabel.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def onRunButtonClicked(self):
        if not self._selectedSearchImagePath:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите изображение для анализа.")
            return

        try:
            image = ImageUtility.readUnicode(self._selectedSearchImagePath)
            if image is None:
                raise Exception("Не удалось загрузить изображение для анализа.")

            resultImage = image.copy()
            self._foundObjects = [] # Очищаем предыдущие результаты

            # --- 1. Поиск по образцу ("Фоторобот") ---
            if self._selectedExampleImagePath:
                template = ImageUtility.readUnicode(self._selectedExampleImagePath)
                if template is not None:
                    foundCorners = VisionProcessor.findObjectByFeatures(template, image)
                    if foundCorners is not None:
                        cv2.polylines(resultImage, [foundCorners], True, (255, 0, 0), 3, cv2.LINE_AA)
                        x, y, w, h = cv2.boundingRect(foundCorners)
                        self._foundObjects.append({'class': 'custom_object', 'box': (x, y, w, h)})

            # --- 2. Поиск лиц с помощью каскада Хаара ---
            faceCascadePath = FileSystemUtility.resourcePath('vision/cascades/haarcascade_frontalface_default.xml')
            faces = VisionProcessor.findObjectsByHaar(image, faceCascadePath)
            for (x, y, w, h) in faces:
                cv2.rectangle(resultImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(resultImage, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                self._foundObjects.append({'class': 'face', 'box': (x, y, w, h)})

            # --- 3. Поиск глаз внутри найденных лиц ---
            eyeCascadePath = FileSystemUtility.resourcePath('vision/cascades/haarcascade_eye.xml')
            for (fx, fy, fw, fh) in faces:
                faceRoi = image[fy:fy+fh, fx:fx+fw] # Область лица
                eyes = VisionProcessor.findObjectsByHaar(faceRoi, eyeCascadePath)
                for (ex, ey, ew, eh) in eyes:
                    # Координаты глаз относительно всего изображения
                    cv2.rectangle(resultImage, (fx + ex, fy + ey), (fx + ex + ew, fy + ey + eh), (0, 0, 255), 2)
                    self._foundObjects.append({'class': 'eye', 'box': (fx + ex, fy + ey, ew, eh)})

            if not self._foundObjects:
                QMessageBox.information(self, "Результат", "На изображении ничего не найдено.")
                return

            self._resultImage = resultImage
            self.displayImage(self._resultImage, self.ui.resultImageLabel)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка во время анализа:\n{str(e)}")

    def displayImage(self, imageCV, label):
        imageRGB = cv2.cvtColor(imageCV, cv2.COLOR_BGR2RGB)
        h, w, ch = imageRGB.shape
        bytesPerLine = ch * w
        qImg = QtGui.QImage(imageRGB.data, w, h, bytesPerLine, QtGui.QImage.Format.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg).scaled(
            label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(pixmap)


    def onSaveResultTableButtonClicked(self):
        if not self._foundObjects:
            QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта. Сначала выполните анализ.")
            return

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Сохранить результаты", filter="CSV файлы (*.csv);;Все файлы (*)"
        )
        if not filePath: return
        if not filePath.lower().endswith('.csv'): filePath += '.csv'

        try:
            import csv
            with open(filePath, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Class", "Top_Left_X", "Top_Left_Y", "Width", "Height"])
                for obj in self._foundObjects:
                    x, y, w, h = obj['box']
                    writer.writerow([obj['class'], x, y, w, h])
            QMessageBox.information(self, "Успех", f"Результаты сохранены в:\n{filePath}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить CSV:\n{str(e)}")

    def onSaveResultImageButtonClicked(self):
        if self._resultImage is None:
            QMessageBox.warning(self, "Ошибка", "Нет результата для сохранения.")
            return

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Сохранить изображение", filter=f"Изображения ({' '.join(f'*.{ext}' for ext in ImageUtility.allowedTypes)});;Все файлы (*)"
        )
        if not filePath: return
        try:
            if ImageUtility.writeUnicode(filePath, self._resultImage):
                QMessageBox.information(self, "Успех", f"Изображение сохранено:\n{filePath}")
            else:
                raise Exception("Не удалось записать файл изображения.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении:\n{str(e)}")