import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QFormLayout, 
                             QGroupBox)
from ruble import RubleCurrency
from dollar import DollarCurrency
from euro import EuroCurrency

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_currencies()
        self.setup_currency_rates()
        self.connect_signals()
        
    def init_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.setGeometry(300, 300, 500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        currency_group = QGroupBox("Конвертер валют")
        form_layout = QFormLayout()
        currency_group.setLayout(form_layout)
        
        self.ruble_input = QLineEdit()
        self.ruble_input.setPlaceholderText("0.00")
        
        self.dollar_input = QLineEdit()
        self.dollar_input.setPlaceholderText("0.00")
        
        self.euro_input = QLineEdit()
        self.euro_input.setPlaceholderText("0.00")
        
        form_layout.addRow('Рубли (RUB):', self.ruble_input)
        form_layout.addRow('Доллары (USD):', self.dollar_input)
        form_layout.addRow('Евро (EUR):', self.euro_input)
        
        main_layout.addWidget(currency_group)
        
        rates_group = QGroupBox("Текущие курсы")
        rates_layout = QVBoxLayout()
        rates_group.setLayout(rates_layout)
        
        self.rates_label = QLabel()
        rates_layout.addWidget(self.rates_label)
        
        main_layout.addWidget(rates_group)
        
        self.statusBar().showMessage('Введите значение в любую валюту.')
        
    def init_currencies(self):
        self.ruble_currency = RubleCurrency()
        self.dollar_currency = DollarCurrency()
        self.euro_currency = EuroCurrency()
        
    def setup_currency_rates(self):
        """Установка курсов валют"""
        self.usd_to_rub = 90.0 
        self.eur_to_rub = 100.0
        self.eur_to_usd = self.eur_to_rub / self.usd_to_rub
        
        rates_info = f"Курсы: 1 USD = {self.usd_to_rub} RUB | 1 EUR = {self.eur_to_rub} RUB | 1 EUR = {self.eur_to_usd:.2f} USD"
        self.rates_label.setText(rates_info)
    
    def connect_signals(self):
        """Подключение всех сигналов"""
        self.ruble_input.textChanged.connect(self.on_ruble_changed)
        self.dollar_input.textChanged.connect(self.on_dollar_changed)
        self.euro_input.textChanged.connect(self.on_euro_changed)
        
        self.ruble_currency.value_changed.connect(self.convert_from_ruble)
        self.dollar_currency.value_changed.connect(self.convert_from_dollar)
        self.euro_currency.value_changed.connect(self.convert_from_euro)
    
    def on_ruble_changed(self, text):
        """Обработчик изменения поля рублей"""
        if not text:
            return
            
        try:
            value = float(text)
            self.ruble_currency.set_value(value)
            self.statusBar().showMessage(f'Введено рублей: {value:.2f} RUB')
        except ValueError:
            pass
    
    def on_dollar_changed(self, text):
        """Обработчик изменения поля долларов"""
        if not text:
            return
            
        try:
            value = float(text)
            self.dollar_currency.set_value(value)
            self.statusBar().showMessage(f'Введено долларов: {value:.2f} USD')
        except ValueError:
            pass
    
    def on_euro_changed(self, text):
        """Обработчик изменения поля евро"""
        if not text:
            return
            
        try:
            value = float(text)
            self.euro_currency.set_value(value)
            self.statusBar().showMessage(f'Введено евро: {value:.2f} EUR')
        except ValueError:
            pass
    
    def convert_from_ruble(self, rubles):
        """Конвертирует из рублей в другие валюты"""
        # Временно отключаем сигналы для полей, которые будем обновлять
        self.dollar_input.blockSignals(True)
        self.euro_input.blockSignals(True)
        
        # Конвертация в доллары
        dollars = rubles / self.usd_to_rub
        self.dollar_input.setText(f"{dollars:.2f}")
        
        # Конвертация в евро
        euros = rubles / self.eur_to_rub
        self.euro_input.setText(f"{euros:.2f}")
        
        # Включаем сигналы обратно
        self.dollar_input.blockSignals(False)
        self.euro_input.blockSignals(False)
            
    def convert_from_dollar(self, dollars):
        """Конвертирует из долларов в другие валюты"""
        # Временно отключаем сигналы для полей, которые будем обновлять
        self.ruble_input.blockSignals(True)
        self.euro_input.blockSignals(True)
        
        # Конвертация в рубли
        rubles = dollars * self.usd_to_rub
        self.ruble_input.setText(f"{rubles:.2f}")
        
        # Конвертация в евро
        euros = dollars * self.usd_to_rub / self.eur_to_rub
        self.euro_input.setText(f"{euros:.2f}")
        
        # Включаем сигналы обратно
        self.ruble_input.blockSignals(False)
        self.euro_input.blockSignals(False)
            
    def convert_from_euro(self, euros):
        """Конвертирует из евро в другие валюты"""
        # Временно отключаем сигналы для полей, которые будем обновлять
        self.ruble_input.blockSignals(True)
        self.dollar_input.blockSignals(True)
        
        # Конвертация в рубли
        rubles = euros * self.eur_to_rub
        self.ruble_input.setText(f"{rubles:.2f}")
        
        # Конвертация в доллары
        dollars = euros * self.eur_to_usd
        self.dollar_input.setText(f"{dollars:.2f}")
        
        # Включаем сигналы обратно
        self.ruble_input.blockSignals(False)
        self.dollar_input.blockSignals(False)
        
def main():
    app = QApplication(sys.argv)
    
    converter = CurrencyConverter()
    converter.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()