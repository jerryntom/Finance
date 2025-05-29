import sqlite3
import os
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox, QScrollArea, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont, Qt

class TransactionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout(self)
        self.titleLabel = QLabel("Transactions")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: #fff;")
        self.layout.addWidget(self.titleLabel)

        # Elegant scroll area for transactions
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("QScrollArea { border: none; }")
        self.transactionsContainer = QWidget()
        self.transactionsLayout = QVBoxLayout(self.transactionsContainer)
        self.transactionsLayout.setSpacing(10)
        self.scrollArea.setWidget(self.transactionsContainer)
        self.layout.addWidget(self.scrollArea)

        # Only Remove All button
        btnLayout = QHBoxLayout()
        self.removeAllButton = QPushButton("Remove All")
        self.removeAllButton.setStyleSheet("QPushButton { color: #fff; border: 1px solid #444; border-radius: 6px; padding: 6px 16px; } QPushButton:hover { background: #31363f; }")
        btnLayout.addWidget(self.removeAllButton)
        self.layout.addLayout(btnLayout)

        self.goBackButton = QPushButton("Go Back")
        self.goBackButton.setStyleSheet("QPushButton { color: #fff; border: 1px solid #444; border-radius: 6px; padding: 6px 16px; } QPushButton:hover { background: #31363f; }")
        self.layout.addWidget(self.goBackButton)

        self.account_id = None
        self.transactions = []

        self.removeAllButton.clicked.connect(self.removeAllTransactions)

    def setAccount(self, account_id, transactions):
        self.account_id = account_id
        # Fetch transaction_id for each transaction from DB
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        db_path = os.path.join(base_path, "finedu.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Get all transactions for this account, ordered by date desc
        cursor.execute(
            "SELECT transaction_id, transaction_date, transaction_name, transaction_amount FROM transactions WHERE finance_account_id = ? ORDER BY transaction_date DESC",
            (account_id,)
        )
        self.transactions = [
            {"transaction_id": row[0], "date": row[1], "description": row[2], "amount": row[3]} for row in cursor.fetchall()
        ]
        conn.close()
        self.refreshList()

    def refreshList(self):
        # Clear layout (widgets and spacers)
        while self.transactionsLayout.count():
            item = self.transactionsLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                del item
        # Show empty state if no transactions
        if not self.transactions:
            emptyLabel = QLabel("No transactions to display.")
            emptyLabel.setStyleSheet("color: #aaa; font-size: 15px; padding: 30px 0; text-align: center;")
            emptyLabel.setAlignment(Qt.AlignCenter)
            self.transactionsLayout.addWidget(emptyLabel)
        else:
            # Add transaction cards
            for idx, t in enumerate(self.transactions):
                card = QFrame()
                card.setFrameShape(QFrame.StyledPanel)
                # Match DashboardUI card style: dark background, border, rounded corners
                card.setStyleSheet("QFrame { background: #23272e; border-radius: 10px; border: 2px solid #444; margin-bottom: 8px; }")
                cardLayout = QHBoxLayout(card)
                cardLayout.setContentsMargins(12, 8, 12, 8)
                # Date
                dateLabel = QLabel(t['date'])
                dateLabel.setStyleSheet("color: #aaa; font-size: 12px;")
                # Description
                descLabel = QLabel(t['description'])
                descLabel.setStyleSheet("font-weight: bold; font-size: 14px; color: #fff;")
                # Amount
                amountLabel = QLabel(f"${t['amount']:.2f}")
                amountLabel.setStyleSheet(f"color: {'#4caf50' if t['amount'] >= 0 else '#e57373'}; font-size: 14px; font-weight: bold;")
                # Remove button
                removeBtn = QPushButton("✕")
                removeBtn.setFixedSize(28, 28)
                removeBtn.setStyleSheet("QPushButton { color: #fff; border: 1px solid #444; border-radius: 14px; } QPushButton:hover { background: #c62828; color: #fff; }")
                removeBtn.clicked.connect(lambda _, i=idx: self.removeTransactionAt(i))
                cardLayout.addWidget(dateLabel)
                cardLayout.addSpacing(10)
                cardLayout.addWidget(descLabel)
                cardLayout.addStretch()
                cardLayout.addWidget(amountLabel)
                cardLayout.addSpacing(10)
                cardLayout.addWidget(removeBtn)
                self.transactionsLayout.addWidget(card)
        self.transactionsLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def removeTransactionAt(self, idx):
        if self.account_id is not None and 0 <= idx < len(self.transactions):
            t = self.transactions[idx]
            transaction_id = t.get("transaction_id")
            if transaction_id is not None:
                # Remove from SQLite by transaction_id
                try:
                    base_path = sys._MEIPASS
                except Exception:
                    base_path = os.path.abspath(".")
                db_path = os.path.join(base_path, "finedu.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM transactions WHERE transaction_id = ?",
                    (transaction_id,)
                )
                # Update account balance
                cursor.execute(
                    "UPDATE finance_accounts SET finance_account_balance = finance_account_balance - ? WHERE finance_account_id = ?",
                    (t['amount'], self.account_id)
                )
                conn.commit()
                conn.close()
            del self.transactions[idx]
            self.refreshList()

    def removeAllTransactions(self):
        if self.transactions:
            confirm = QMessageBox.question(self, "Confirm", "Remove all transactions?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    base_path = sys._MEIPASS
                except Exception:
                    base_path = os.path.abspath(".")
                db_path = os.path.join(base_path, "finedu.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                # Fetch initial balance (the balance before any transactions)
                cursor.execute(
                    "SELECT finance_account_balance FROM finance_accounts WHERE finance_account_id = ?",
                    (self.account_id,)
                )
                initial_balance = cursor.fetchone()
                if initial_balance is not None:
                    # Calculate what the balance would be if all transactions are removed
                    # Sum all transaction amounts for this account
                    cursor.execute(
                        "SELECT SUM(transaction_amount) FROM transactions WHERE finance_account_id = ?",
                        (self.account_id,)
                    )
                    total_transactions = cursor.fetchone()[0] or 0.0
                    # Set balance to current balance minus all transaction amounts
                    new_balance = initial_balance[0] - total_transactions
                    # Remove all transactions
                    cursor.execute(
                        "DELETE FROM transactions WHERE finance_account_id = ?",
                        (self.account_id,)
                    )
                    # Restore balance to initial value (before any transactions)
                    cursor.execute(
                        "UPDATE finance_accounts SET finance_account_balance = ? WHERE finance_account_id = ?",
                        (new_balance, self.account_id)
                    )
                    conn.commit()
                conn.close()
                self.transactions.clear()
                self.refreshList()
        else:
            QMessageBox.information(self, "No transactions", "There are no transactions to remove.")
