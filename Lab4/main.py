import sys
import os
from datetime import datetime
from PyQt5.QtCore import QUrl, QObject, QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    saveRequest = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._interval_sec = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer)
        self.timer.start(self._interval_sec * 1000)

        print(f"Автосохранение включено: каждые {self._interval_sec} сек.")

    @pyqtSlot()
    def _on_timer(self):
        self.saveRequest.emit()


if __name__ == '__main__':

    # Создаем экземпляр приложения
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)

    # Загружаем QML
    engine.load("mainWindow.qml")

    # Проверка успешной загрузки QML
    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    sys.exit(app.exec())
