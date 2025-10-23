from PyQt5.QtCore import QObject, pyqtSignal

class EuroCurrency(QObject):
    value_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self._value = 0.0
    
    def set_value(self, value):
        self._value = value
        self.value_changed.emit(value)