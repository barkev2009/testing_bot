import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont

from ..main import get_all_functions, test_new_app, test_existing_app

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_number = ''
        self.actions = []

        self.setWindowTitle("Тестирование fp-gnb.fisgroup.ru")

        self.layout = QVBoxLayout()

        
        self.setup_input_field()
        self.setup_checkboxes()
        self.setup_main_button()

        widget = QWidget()
        widget.setLayout(self.layout)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)

    def setup_checkboxes(self):
        self.checkboxes = []
        self.setup_main_checkbox()

        self.functions = get_all_functions()
        for func in self.functions:
            self.checkboxes.append(self.setup_checkbox(func[0]))


    def setup_checkbox(self, function_name):
        def checkbox_trigger(state):
            self.actions = []
            for i, box in enumerate(self.checkboxes):
                if box.isChecked():
                    self.actions.append(self.functions[i])
            # print(self.actions)

        checkbox = QCheckBox(function_name)
        checkbox.stateChanged.connect(checkbox_trigger)
        self.layout.addWidget(checkbox)
        return checkbox
    
    def setup_main_checkbox(self):
        def checkbox_trigger(state):
            if state == 2:
                for checkbox in self.checkboxes:
                    checkbox.setChecked(True)
            else:
                for checkbox in self.checkboxes:
                    checkbox.setChecked(False)
        checkbox = QCheckBox('Выделить/Убрать все функции')
        checkbox.stateChanged.connect(checkbox_trigger)
        # checkbox.setFont(QFont(italic=True))
        self.layout.addWidget(checkbox)
    
    def setup_main_button(self):
        def timer():
            time.sleep(5)
            self.main_button.setDisabled(False)
        def trigger_button(state):
            if self.actions:
                if self.app_number == '':
                    test_new_app(self.actions)
                else:
                    test_existing_app(self.actions, [self.app_number])

        self.main_button = QPushButton('Запустить')
        self.main_button.clicked.connect(trigger_button)
        self.layout.addWidget(self.main_button)
    
    def setup_input_field(self):
        def trigger_input(state):
            self.app_number = state
            # print(self.app_number)
        
        h_layout = QHBoxLayout()
        input_form = QLineEdit()
        input_form.textChanged.connect(trigger_input)
        self.layout.addLayout(h_layout)
        h_layout.addWidget(QLabel('Номер заявки:'))
        h_layout.addWidget(input_form)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()