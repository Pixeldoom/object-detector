# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 933)
        MainWindow.setStyleSheet(u"QLabel {\n"
"    background-color: white;\n"
"    border: 2px solid #ddd;\n"
"    padding: 10px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1601, 601))
        self.imagesLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.imagesLayout.setObjectName(u"imagesLayout")
        self.imagesLayout.setContentsMargins(10, 100, 10, 100)
        self.exampleImageLabel = QLabel(self.horizontalLayoutWidget)
        self.exampleImageLabel.setObjectName(u"exampleImageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exampleImageLabel.sizePolicy().hasHeightForWidth())
        self.exampleImageLabel.setSizePolicy(sizePolicy)

        self.imagesLayout.addWidget(self.exampleImageLabel)

        self.searchImageLabel = QLabel(self.horizontalLayoutWidget)
        self.searchImageLabel.setObjectName(u"searchImageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searchImageLabel.sizePolicy().hasHeightForWidth())
        self.searchImageLabel.setSizePolicy(sizePolicy1)
        self.searchImageLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.searchImageLabel.setScaledContents(True)
        self.searchImageLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.imagesLayout.addWidget(self.searchImageLabel)

        self.resultImageLabel = QLabel(self.horizontalLayoutWidget)
        self.resultImageLabel.setObjectName(u"resultImageLabel")
        sizePolicy1.setHeightForWidth(self.resultImageLabel.sizePolicy().hasHeightForWidth())
        self.resultImageLabel.setSizePolicy(sizePolicy1)
        self.resultImageLabel.setTextFormat(Qt.TextFormat.PlainText)

        self.imagesLayout.addWidget(self.resultImageLabel)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 605, 1581, 321))
        self.buttonsLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.mainButtonsLayout = QVBoxLayout()
        self.mainButtonsLayout.setSpacing(10)
        self.mainButtonsLayout.setObjectName(u"mainButtonsLayout")
        self.mainButtonsLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.mainButtonsLayout.setContentsMargins(10, 10, 10, 10)
        self.selectExampleImageButton = QPushButton(self.horizontalLayoutWidget_2)
        self.selectExampleImageButton.setObjectName(u"selectExampleImageButton")
        self.selectExampleImageButton.setEnabled(True)
        sizePolicy.setHeightForWidth(self.selectExampleImageButton.sizePolicy().hasHeightForWidth())
        self.selectExampleImageButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(13)
        self.selectExampleImageButton.setFont(font)

        self.mainButtonsLayout.addWidget(self.selectExampleImageButton)

        self.selectSearchImageButton = QPushButton(self.horizontalLayoutWidget_2)
        self.selectSearchImageButton.setObjectName(u"selectSearchImageButton")
        sizePolicy.setHeightForWidth(self.selectSearchImageButton.sizePolicy().hasHeightForWidth())
        self.selectSearchImageButton.setSizePolicy(sizePolicy)
        self.selectSearchImageButton.setFont(font)

        self.mainButtonsLayout.addWidget(self.selectSearchImageButton)

        self.runButton = QPushButton(self.horizontalLayoutWidget_2)
        self.runButton.setObjectName(u"runButton")
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setSizeIncrement(QSize(0, 0))
        self.runButton.setFont(font)

        self.mainButtonsLayout.addWidget(self.runButton)


        self.buttonsLayout.addLayout(self.mainButtonsLayout)

        self.verticalSpacer = QSpacerItem(500, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttonsLayout.addItem(self.verticalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalSpacer = QSpacerItem(40, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)

        self.saveResultTableButton = QPushButton(self.horizontalLayoutWidget_2)
        self.saveResultTableButton.setObjectName(u"saveResultTableButton")
        sizePolicy.setHeightForWidth(self.saveResultTableButton.sizePolicy().hasHeightForWidth())
        self.saveResultTableButton.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(False)
        font1.setKerning(True)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.saveResultTableButton.setFont(font1)
        self.saveResultTableButton.setFlat(False)

        self.verticalLayout.addWidget(self.saveResultTableButton)

        self.saveResultImageButton = QPushButton(self.horizontalLayoutWidget_2)
        self.saveResultImageButton.setObjectName(u"saveResultImageButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.saveResultImageButton.sizePolicy().hasHeightForWidth())
        self.saveResultImageButton.setSizePolicy(sizePolicy2)
        self.saveResultImageButton.setFont(font)

        self.verticalLayout.addWidget(self.saveResultImageButton)


        self.buttonsLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.saveResultTableButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.exampleImageLabel.setText("")
        self.searchImageLabel.setText("")
        self.resultImageLabel.setText("")
        self.selectExampleImageButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043e\u0431\u0440\u0430\u0437\u0435\u0446 \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430", None))
        self.selectSearchImageButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u043f\u043e\u0438\u0441\u043a \u043e\u0431\u044a\u0435\u043a\u0442\u0430", None))
        self.saveResultTableButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443 \u0441 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430\u043c\u0438", None))
        self.saveResultImageButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u043d\u043e\u0435 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
    # retranslateUi

