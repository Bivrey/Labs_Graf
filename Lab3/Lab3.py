import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTableView, QAction, QFileDialog,
    QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QDialog,
    QLabel, QTextEdit, QHBoxLayout, QInputDialog, QComboBox as QtComboBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

class Lab3Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3 — PyQt + SQLite")
        self.resize(1050, 700)

        self.db = None
        self.supported_tables = ["students", "groups", "courses"]

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        self.bt1 = QPushButton("bt1: SELECT * FROM sqlite_master")
        self.bt1.setEnabled(False)
        self.bt1.clicked.connect(self.on_bt1_clicked)

        self.combo_label = QLabel("Колонка (из students):")
        self.combo = QComboBox()
        self.combo.setEnabled(False)
        self.combo.currentTextChanged.connect(self.on_combo_changed)

        self.bt2 = QPushButton("bt2: SELECT * FROM students")
        self.bt2.setEnabled(False)
        self.bt2.clicked.connect(self.on_bt2_clicked)

        self.bt3 = QPushButton("bt3: SELECT * FROM student_grades")
        self.bt3.setEnabled(False)
        self.bt3.clicked.connect(self.on_bt3_clicked)

        self.bt_add_record = QPushButton("➕ Add Record")
        self.bt_add_record.setEnabled(False)
        self.bt_add_record.clicked.connect(self.add_record)

        self.bt_del_record = QPushButton("🗑️ Delete Record")
        self.bt_del_record.setEnabled(False)
        self.bt_del_record.clicked.connect(self.delete_record)

        # Раскладка
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.bt1)
        control_layout.addWidget(self.combo_label)
        control_layout.addWidget(self.combo)
        control_layout.addWidget(self.bt2)
        control_layout.addWidget(self.bt3)
        control_layout.addWidget(self.bt_add_record)
        control_layout.addWidget(self.bt_del_record)

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Меню
        menubar = self.menuBar()
        db_menu = menubar.addMenu("Database")
        self.action_set_conn = QAction("Set connection", self)
        self.action_set_conn.triggered.connect(self.set_connection)
        db_menu.addAction(self.action_set_conn)

        self.action_close_conn = QAction("Close connection", self)
        self.action_close_conn.triggered.connect(self.close_connection)
        self.action_close_conn.setEnabled(False)
        db_menu.addAction(self.action_close_conn)

        request_menu = menubar.addMenu("SQL request")
        self.action_custom_sql = QAction("Execute custom SQL...", self)
        self.action_custom_sql.setShortcut("Ctrl+E")
        self.action_custom_sql.triggered.connect(self.open_custom_sql_dialog)
        self.action_custom_sql.setEnabled(False)
        request_menu.addAction(self.action_custom_sql)

    def set_connection(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите SQLite базу данных", "", "SQLite DB (*.db *.sqlite *.sqlite3)"
        )
        if not file_path:
            return

        self.close_connection()
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(file_path)

        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть БД:\n{self.db.lastError().text()}")
            self.db = None
            return

        QMessageBox.information(self, "Успех", f"Подключено к:\n{os.path.basename(file_path)}")

        self.run_query("SELECT * FROM sqlite_master", "Tab1: sqlite_master")

        cols = self._get_columns("students")
        self.combo.clear()
        self.combo.addItems(cols)

        for btn in [self.bt1, self.combo, self.bt2, self.bt3,
                    self.bt_add_record, self.bt_del_record]:
            btn.setEnabled(True)
        self.action_close_conn.setEnabled(True)
        self.action_custom_sql.setEnabled(True)

    def _get_columns(self, table_name):
        """Возвращает список столбцов таблицы через PRAGMA."""
        if not self.db or not self.db.isOpen():
            return []
        query = self.db.exec_(f"PRAGMA table_info(`{table_name}`)")
        cols = []
        while query.next():
            cols.append(query.value(1))
        return cols

    def close_connection(self):
        if self.db:
            self.db.close()
            QSqlDatabase.removeDatabase(self.db.connectionName())
            self.db = None

        self.tabs.clear()
        self.combo.clear()
        for btn in [self.bt1, self.combo, self.bt2, self.bt3,
                    self.bt_add_record, self.bt_del_record]:
            btn.setEnabled(False)
        self.action_close_conn.setEnabled(False)
        self.action_custom_sql.setEnabled(False)

    def run_query(self, query_str, tab_title):
        if not self.db or not self.db.isOpen():
            return
        model = QSqlQueryModel()
        model.setQuery(query_str, self.db)
        if model.lastError().isValid():
            QMessageBox.warning(self, "Ошибка SQL", f"{model.lastError().text()}\n\nЗапрос:\n{query_str}")
            return
        view = QTableView()
        view.setModel(model)
        view.resizeColumnsToContents()
        view.setSortingEnabled(True)
        self.tabs.addTab(view, tab_title)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def on_bt1_clicked(self):
        self.run_query("SELECT * FROM sqlite_master", "Tab3: * (bt1)")

    def on_combo_changed(self, col_name):
        if col_name:
            self.run_query(f"SELECT `{col_name}` FROM students", f"Tab2: students.{col_name}")

    def on_bt2_clicked(self):
        self.run_query("SELECT * FROM students", "Tab4: Students (bt2)")

    def on_bt3_clicked(self):
        self.run_query("SELECT * FROM student_grades", "Tab5: Grades (bt3)")

    def add_record(self):
        table, ok = QInputDialog.getItem(
            self, "Добавить запись", "Выберите таблицу:", self.supported_tables, 0, False
        )
        if not ok:
            return

        cols = self._get_columns(table)
        if not cols:
            QMessageBox.warning(self, "Ошибка", f"Не удалось получить структуру таблицы '{table}'.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Добавить запись в '{table}'")
        layout = QVBoxLayout()

        ignores = {"id"}
        edits = {}
        for col in cols:
            if col.lower() in ignores:
                continue
            layout.addWidget(QLabel(f"{col}:"))
            edit = QTextEdit()
            edit.setMaximumHeight(40)
            layout.addWidget(edit)
            edits[col] = edit

        btn_ok = QPushButton("Добавить")
        btn_cancel = QPushButton("Отмена")
        layout.addWidget(btn_ok)
        layout.addWidget(btn_cancel)
        dialog.setLayout(layout)

        def on_ok():
            values = []
            for edit in edits.values():
                val = edit.toPlainText().strip()
                values.append(val if val != "" else None)

            cols_list = list(edits.keys())
            placeholders = ", ".join("?" for _ in cols_list)
            cols_sql = ", ".join(f"`{c}`" for c in cols_list)
            query_str = f"INSERT INTO `{table}` ({cols_sql}) VALUES ({placeholders})"

            query = QSqlQuery(self.db)
            if not query.prepare(query_str):
                QMessageBox.critical(dialog, "Ошибка", f"Подготовка:\n{query.lastError().text()}")
                return

            for val in values:
                query.addBindValue(val)

            if not query.exec_():
                QMessageBox.critical(dialog, "Ошибка", f"Выполнение:\n{query.lastError().text()}")
                return

            QMessageBox.information(dialog, "Успех", f"Добавлено в '{table}' (id = {query.lastInsertId()})")
            dialog.accept()

        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.reject)
        dialog.exec_()

    def delete_record(self):
        table, ok = QInputDialog.getItem(
            self, "Удалить запись", "Выберите таблицу:", self.supported_tables, 0, False
        )
        if not ok:
            return

        pk_name = "id"
        cols = self._get_columns(table)
        pk_col = next((c for c in cols if c.lower() == "id"), None)
        if pk_col:
            pk_name = pk_col

        record_id, ok = QInputDialog.getInt(
            self, f"Удалить из '{table}'", f"Введите {pk_name}:", 1, 1, 10000
        )
        if not ok:
            return

        check_query = QSqlQuery(self.db)
        ok = check_query.prepare(f"SELECT 1 FROM `{table}` WHERE `{pk_name}` = ?")
        if not ok:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подготовить CHECK-запрос:\n{check_query.lastError().text()}")
            return

        check_query.addBindValue(record_id)
        ok = check_query.exec_()
        if not ok or not check_query.next():
            QMessageBox.warning(self, "Не найдено", f"Запись с {pk_name} = {record_id} не найдена в '{table}'.")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить запись из '{table}' с {pk_name} = {record_id}?\n⚠️ Каскадное удаление может затронуть связанные данные.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No:
            return

        del_query = QSqlQuery(self.db)
        ok = del_query.prepare(f"DELETE FROM `{table}` WHERE `{pk_name}` = ?")
        if not ok:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подготовить DELETE:\n{del_query.lastError().text()}")
            return

        del_query.addBindValue(record_id)
        ok = del_query.exec_()
        if not ok:
            QMessageBox.critical(self, "Ошибка", f"Удаление не выполнено:\n{del_query.lastError().text()}")
            return

        QMessageBox.information(self, "Удалено", f"Запись ({pk_name} = {record_id}) удалена из '{table}'.")

    def open_custom_sql_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("SQL-запрос")
        dialog.resize(650, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите SQL-запрос:"))
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        btn_ok = QPushButton("Выполнить")
        btn_cancel = QPushButton("Отмена")
        layout.addWidget(btn_ok)
        layout.addWidget(btn_cancel)
        dialog.setLayout(layout)

        def on_ok():
            sql = text_edit.toPlainText().strip()
            if sql:
                self.run_query(sql, "TabX: Custom SQL")
            dialog.accept()
        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.reject)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Lab3Window()
    window.show()
    sys.exit(app.exec_())