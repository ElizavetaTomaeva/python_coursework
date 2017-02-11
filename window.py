from PyQt5.QtWidgets import QDialog, QMainWindow, QTextEdit, QAction, QFileDialog
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTextEdit,
                             QAction, QFileDialog, QApplication, QScrollArea, QLabel, QToolBar, QVBoxLayout,
                             QDockWidget, QComboBox, QListView, QListWidget, QGraphicsAnchorLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import repack
import sys
from os.path import exists

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.__init_signals()

    def initUI(self):
        self.setFixedSize(1350, 695)
        self.setGeometry(10, 30, 1000, 300)
        self.setWindowTitle("Comic Book Reader")

        self.background = QVBoxLayout(self)
        self.setLayout(self.background)

        self.scrollArea = QScrollArea(self)
        self.background.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(self.width(), self.height())

        self.imageArea = QLabel()
        self.scrollArea.setWidget(self.imageArea)

        self.statusBar()

        self.exit = QAction(QIcon('./images/exit.png'), 'Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')

        self.open = QAction(QIcon('./images/open.png'), 'Open', self)
        self.open.setStatusTip('Open file')

        self.backward = QAction(QIcon('./images/backward.png'), 'Backward', self)
        self.backward.setStatusTip('Previous page')

        self.forward = QAction(QIcon('./images/forward.png'), 'Forward', self)
        self.forward.setStatusTip('Next page')

        self.toolbar = self.addToolBar('Tools', )
        # self.toolbar.setGeometry(50, 100, self.height(), self.width())
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.backward)
        self.toolbar.addAction(self.forward)
        self.toolbar.addAction(self.exit)

        self.closeFile = QAction('Exit', self)
        self.open.setStatusTip('Open file')

        self.pageBox = QComboBox(self)
        self.pageBox.setGeometry(1220, 10, 100, 20)
        self.pageBox.setStatusTip("Page")
        self.pageBox.hide()

        self.show()

    def __init_signals(self):
        self.backward.triggered.connect(self.previous_page)
        self.forward.triggered.connect(self.next_page)
        self.open.triggered.connect(self.show_dialog)
        self.closeFile.triggered.connect(self.close)
        self.pageBox.currentIndexChanged.connect(self.open_page)
        self.exit.triggered.connect(self.close)

    def show_dialog(self):  # диалог открытия файла
        self.bookfile = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Comic Book Archive files (*.cbz *.cbr)")[0]
        if self.bookfile:
            count = 0
            self.pageBox.show()
            for page_num in repack.all_pages(repack.extract(self.bookfile)):  # страницы в выпадающем списке
                self.pageBox.addItem(str(count))
                count += 1
        else:
            return

    def open_page(self):  # загрузка страницы по номеру из выпадающего списка
        page = repack.all_pages(repack.extract(self.bookfile))[self.get_combo_box_index()]
        self.myPixmap = QPixmap(page).scaledToWidth(self.width())
        self.imageArea.setPixmap(self.myPixmap)

    def get_combo_box_index(self):  # индекс строки в выпадающем списке
        return self.pageBox.currentIndex()

    # def load_first_page(self):  # загрузка первой страницы при открытии папки
    #     picture = get_files.all_pages(get_files.extract(self.bookfile))[0]
    #     self.myPixmap = QPixmap(picture)
    #     self.imageArea.setPixmap(self.myPixmap)

    def previous_page(self, new_index):  # пролистывание назад
        return self.pageBox.setCurrentIndex(self.get_combo_box_index()-1)

    def next_page(self): # пролистывание вперед
        return self.pageBox.setCurrentIndex(self.get_combo_box_index()+1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())