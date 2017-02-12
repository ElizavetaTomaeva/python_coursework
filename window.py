from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog,
                             QApplication, QScrollArea, QLabel,
                             QVBoxLayout,QComboBox, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import unpack
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.__init_signals()

    def initUI(self):
        # self.showFullScreen()
        self.setFixedSize(1360, 695)
        # self.setGeometry(10, 30, 1000, 300)
        self.setWindowTitle("Comic Book Reader")

        self.background = QVBoxLayout(self)
        self.setLayout(self.background)

        self.scrollArea = QScrollArea(self)
        self.background.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(self.width(), self.height())

        self.imageArea = QLabel()
        self.scrollArea.setWidget(self.imageArea)
        self.scrollArea.hide()

        self.statusBar()

        self.exit = QAction(QIcon('./images/exit.png'), 'Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')

        self.open = QAction(QIcon('./images/open.png'), 'Open', self)
        self.open.setShortcut('Ctrl+O')
        self.open.setStatusTip('Open file')

        self.backward = QAction(QIcon('./images/backward.png'), 'Backward', self)
        self.backward.setStatusTip('Previous page')
        self.backward.setEnabled(False)

        self.forward = QAction(QIcon('./images/forward.png'), 'Forward', self)
        self.forward.setStatusTip('Next page')
        self.forward.setEnabled(False)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.backward)
        self.toolbar.addAction(self.forward)
        self.toolbar.addAction(self.exit)
        self.toolbar.setStyleSheet("QToolBar {border-color: none}")
        self.closeFile = QAction('Exit', self)
        self.open.setStatusTip('Open file')

        self.sizeCheck = QCheckBox(self)
        self.sizeCheck.setText('Cover')
        self.sizeCheck.setGeometry(1100, 10, 100, 20)
        self.sizeCheck.hide()

        self.pageBox = QComboBox(self)
        self.pageBox.setFocusPolicy(Qt.NoFocus)
        self.pageBox.setGeometry(1220, 10, 100, 20)
        self.pageBox.setStatusTip('Page')
        self.pageBox.hide()

        self.show()

    def __init_signals(self):
        self.backward.triggered.connect(self.previous_page)
        self.forward.triggered.connect(self.next_page)
        self.open.triggered.connect(self.show_dialog)
        self.sizeCheck.stateChanged.connect(self.change_size)
        self.closeFile.triggered.connect(self.close)
        self.pageBox.currentIndexChanged.connect(self.open_page)
        self.exit.triggered.connect(self.close)

    def show_dialog(self):  # диалог открытия файла
        self.bookfile = QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                                    "Comic Book Archive files (*.cbz *.cbr)")[0]
        if self.bookfile:
            self.scrollArea.show()
            self.backward.setEnabled(True)
            self.forward.setEnabled(True)
            self.pageBox.show()
            self.sizeCheck.show()
            self.setWindowTitle("Comic Book Reader - " + unpack.get_book_name(self.bookfile))
            if self.pageBox not in range(0):
                self.pageBox.clear()
            self.get_page_num()
        else:
            return

    def get_page_num(self):   # добавление номеров страниц в выпадающий список
        count = 0
        for page_num in unpack.all_pages(unpack.extract(self.bookfile)):
            self.pageBox.addItem(str(count))
            count += 1

    def open_page(self):  # загрузка страницы по номеру из выпадающего списка
        self.page = unpack.all_pages(unpack.extract(self.bookfile))[self.get_combo_box_index()]
        if self.get_combo_box_index() == 0:
            self.load_cover()
        else:
            self.load_fullscreen()

    def get_combo_box_index(self):  # индекс строки в выпадающем списке
        return self.pageBox.currentIndex()

    def previous_page(self):  # пролистывание назад
        return self.pageBox.setCurrentIndex(self.get_combo_box_index()-1)

    def next_page(self):  # пролистывание вперед
        return self.pageBox.setCurrentIndex(self.get_combo_box_index()+1)

    def load_fullscreen(self):  # отображение по ширине окна
        self.myPixmap = QPixmap(self.page).scaledToWidth(self.width())
        self.imageArea.setPixmap(self.myPixmap)
        self.sizeCheck.setChecked(False)

    def load_cover(self):  # отображение по высоте окна и по центру
        self.myPixmap = QPixmap(self.page).scaledToHeight(self.height())
        self.imageArea.setPixmap(self.myPixmap)
        self.imageArea.setAlignment(Qt.AlignHCenter)
        self.sizeCheck.setChecked(True)

    def change_size(self):  # изменение формата отображения
        if self.sizeCheck.isChecked():
            self.load_cover()
        else:
            self.load_fullscreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())