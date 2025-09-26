import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мое простое приложение")
        self.resize(400, 300)

        # Метка с текстом
        self.label = QLabel("Привет! Это начальная надпись.", self)
        self.label.setStyleSheet("color: black; font-size: 16px;")
        self.label.setAlignment(Qt.AlignCenter)

        # Кнопка 1: меняет текст
        self.btn_text = QPushButton("Изменить надпись", self)
        self.btn_text.clicked.connect(self.change_text)

        # Кнопка 2: ставит PNG как фон
        self.btn_shape = QPushButton("Поставить PNG фоном", self)
        self.btn_shape.clicked.connect(self.change_background)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_text)
        hbox.addWidget(self.btn_shape)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.background = None
        self.alpha = 0.6

    def change_text(self):
        self.label.setText("Надпись изменилась!")

    def change_background(self):
        pix = QPixmap("cat.png")
        if not pix.isNull():
            self.background = pix
            self.update()
        else:
            self.label.setText("PNG не найден!")

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background:
            painter.setOpacity(self.alpha) 
            painter.drawPixmap(self.rect(), self.background)
            painter.setOpacity(1.0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
