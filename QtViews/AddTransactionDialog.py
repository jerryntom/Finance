import os
import sys
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox)
from PySide6.QtCore import Qt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Transaction")
        self.setModal(True)
        self.setMinimumWidth(350)
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)

        # Transaction Name
        nameLabel = QLabel("Transaction Name:")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMaxLength(50)
        layout.addWidget(nameLabel)
        layout.addWidget(self.nameEdit)

        # Transaction Amount
        amountLabel = QLabel("Amount:")
        self.amountSpin = QDoubleSpinBox()
        self.amountSpin.setRange(-99999999, 99999999)
        self.amountSpin.setDecimals(2)
        self.amountSpin.setValue(0.00)
        layout.addWidget(amountLabel)
        layout.addWidget(self.amountSpin)

        # Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.errorLabel)

        # Buttons
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add")
        self.cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        self.addButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def getData(self):
        name = self.nameEdit.text().strip()
        amount = self.amountSpin.value()
        return name, amount

    def accept(self):
        name = self.nameEdit.text().strip()
        amount = self.amountSpin.value()
        if not name:
            self.nameEdit.setToolTip("Transaction name cannot be empty.")
            self.errorLabel.setText("Transaction name cannot be empty.")
            return
        else:
            self.nameEdit.setToolTip("")
            self.amountSpin.setToolTip("")
            self.errorLabel.setText("")
        super().accept()
