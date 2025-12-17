# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_passwd.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpinBox, QStackedWidget,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.act_quit = QAction(MainWindow)
        self.act_quit.setObjectName(u"act_quit")
        self.act_Apropos = QAction(MainWindow)
        self.act_Apropos.setObjectName(u"act_Apropos")
        self.act_quit_2 = QAction(MainWindow)
        self.act_quit_2.setObjectName(u"act_quit_2")
        self.act_help = QAction(MainWindow)
        self.act_help.setObjectName(u"act_help")
        self.act_propos = QAction(MainWindow)
        self.act_propos.setObjectName(u"act_propos")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 0, 791, 571))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.lineEdit_1 = QLineEdit(self.page)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setGeometry(QRect(160, 110, 441, 31))
        self.lineEdit_1.setEchoMode(QLineEdit.Password)
        self.btn_verify = QPushButton(self.page)
        self.btn_verify.setObjectName(u"btn_verify")
        self.btn_verify.setGeometry(QRect(110, 210, 141, 41))
        self.btn_verify.setStyleSheet(u"QPushButton {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"")
        self.btn_auto_generer = QPushButton(self.page)
        self.btn_auto_generer.setObjectName(u"btn_auto_generer")
        self.btn_auto_generer.setGeometry(QRect(530, 210, 131, 41))
        self.btn_auto_generer.setStyleSheet(u"QPushButton {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"")
        self.progressBar = QProgressBar(self.page)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(150, 320, 451, 31))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QProgressBar:hover {\n"
"    background-color: white;\n"
"}\n"
"")
        self.progressBar.setValue(24)
        self.label_tips = QLabel(self.page)
        self.label_tips.setObjectName(u"label_tips")
        self.label_tips.setGeometry(QRect(170, 400, 431, 111))
        self.label_tips.setMargin(1)
        self.btn_api = QPushButton(self.page)
        self.btn_api.setObjectName(u"btn_api")
        self.btn_api.setGeometry(QRect(270, 210, 241, 41))
        self.btn_api.setStyleSheet(u"QPushButton {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"")
        self.check_pwd_show = QCheckBox(self.page)
        self.check_pwd_show.setObjectName(u"check_pwd_show")
        self.check_pwd_show.setGeometry(QRect(140, 160, 191, 24))
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 20, 421, 41))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.btn_generer = QPushButton(self.page_2)
        self.btn_generer.setObjectName(u"btn_generer")
        self.btn_generer.setGeometry(QRect(310, 290, 111, 31))
        self.btn_generer.setStyleSheet(u"QPushButton {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"")
        self.checkBox_memonic = QCheckBox(self.page_2)
        self.checkBox_memonic.setObjectName(u"checkBox_memonic")
        self.checkBox_memonic.setGeometry(QRect(420, 190, 161, 24))
        self.btn_copy = QPushButton(self.page_2)
        self.btn_copy.setObjectName(u"btn_copy")
        self.btn_copy.setGeometry(QRect(630, 130, 88, 31))
        self.btn_copy.setStyleSheet(u"QPushButton {\n"
"    border-radius: 15px;\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"")
        icon = QIcon()
        iconThemeName = u"edit-copy"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.btn_copy.setIcon(icon)
        self.lineEdit_2 = QLineEdit(self.page_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(80, 130, 531, 31))
        self.btn_page1 = QPushButton(self.page_2)
        self.btn_page1.setObjectName(u"btn_page1")
        self.btn_page1.setGeometry(QRect(10, 10, 91, 31))
        icon1 = QIcon()
        iconThemeName = u"go-previous"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.btn_page1.setIcon(icon1)
        self.spinBox = QSpinBox(self.page_2)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(260, 196, 51, 31))
        self.spinBox.setMinimum(6)
        self.spinBox.setMaximum(24)
        self.label_lenght = QLabel(self.page_2)
        self.label_lenght.setObjectName(u"label_lenght")
        self.label_lenght.setGeometry(QRect(170, 200, 71, 20))
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(210, 40, 341, 41))
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuAide = QMenu(self.menubar)
        self.menuAide.setObjectName(u"menuAide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAide.menuAction())
        self.menuAide.addAction(self.act_quit_2)
        self.menuAide.addAction(self.act_help)
        self.menuAide.addAction(self.act_propos)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.act_quit.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.act_Apropos.setText(QCoreApplication.translate("MainWindow", u"A propos", None))
        self.act_quit_2.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.act_help.setText(QCoreApplication.translate("MainWindow", u"Aide", None))
        self.act_propos.setText(QCoreApplication.translate("MainWindow", u"\u00c0 propos", None))
        self.lineEdit_1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Entrez votre mot de passe \u00e0 analyser...", None))
        self.btn_verify.setText(QCoreApplication.translate("MainWindow", u"V\u00e9rifier la force", None))
        self.btn_auto_generer.setText(QCoreApplication.translate("MainWindow", u"G\u00e9n\u00e9rer ", None))
        self.label_tips.setText(QCoreApplication.translate("MainWindow", u"Tips", None))
        self.btn_api.setText(QCoreApplication.translate("MainWindow", u"Verification  de l'unicit\u00e9", None))
        self.check_pwd_show.setText(QCoreApplication.translate("MainWindow", u"Afficher le mot de passe", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\U0001f50d\U0001f510D\U000000e9couvrez les faiblesses et am\U000000e9liorez votre protection", None))
        self.btn_generer.setText(QCoreApplication.translate("MainWindow", u"Generer", None))
        self.checkBox_memonic.setText(QCoreApplication.translate("MainWindow", u"Mnemonic password", None))
        self.btn_copy.setText(QCoreApplication.translate("MainWindow", u"Copier", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Votre mot de passe sera g\u00e9n\u00e9r\u00e9 ici...", None))
        self.btn_page1.setText(QCoreApplication.translate("MainWindow", u"Back ", None))
        self.label_lenght.setText(QCoreApplication.translate("MainWindow", u"Longueur : ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cr\u00e9ez des mots de passe inviolables en un clic", None))
        self.menuAide.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

