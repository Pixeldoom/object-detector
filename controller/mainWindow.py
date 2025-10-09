from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow
from view.mainWindow import Ui_MainWindow
from utility.image import Image as ImageUtility
from utility.fileSystem import FileSystem as FileSystemUtility


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._selectedExampleImagePath = ''

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.selectExampleImageButton.clicked.connect(self.onSelectExamplaeImageButtonClicked)
        self.ui.selectSearchImageButton.clicked.connect(self.onSelectSearchImageButtonClicked)
        self.ui.runButton.clicked.connect(self.onRunButtonClicked)
        self.ui.openResultTableButton.clicked.connect(self.onOpenResultTableButtonClicked)
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
        pass

    def onRunButtonClicked(self):
        pass

    def onOpenResultTableButtonClicked(self):
        pass

    def onSaveResultImageButtonClicked(self):
        pass