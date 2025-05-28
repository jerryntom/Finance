import sqlite3
import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QScrollArea, QGridLayout,
                              QSpacerItem, QSizePolicy, QStyle)
from PySide6.QtGui import QFont, QIcon
from .AddAccountDialog import AddAccountDialog
from .AddTransactionDialog import AddTransactionDialog

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DashboardView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.db = sqlite3.connect(resource_path("finedu.db"))
        self.accounts = []
        
    def setUpUI(self):
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Header section
        self.headerFrame = QFrame()
        self.headerLayout = QHBoxLayout(self.headerFrame)
        
        self.welcomeLabel = QLabel("Welcome to Your Financial Dashboard")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.welcomeLabel.setFont(font)
        
        self.logoutButton = QPushButton("Logout")
        self.logoutButton.setFixedWidth(100)
        
        self.headerLayout.addWidget(self.welcomeLabel)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.logoutButton)
        
        # Summary section
        self.summaryFrame = QFrame()
        self.summaryFrame.setFrameShape(QFrame.StyledPanel)
        self.summaryLayout = QHBoxLayout(self.summaryFrame)
        
        self.totalBalanceFrame = self.createSummaryBox("Total Balance", "$0.00")
        self.incomeFrame = self.createSummaryBox("Monthly Income", "$0.00")
        self.expensesFrame = self.createSummaryBox("Monthly Expenses", "$0.00")
        
        self.summaryLayout.addWidget(self.totalBalanceFrame)
        self.summaryLayout.addWidget(self.incomeFrame)
        self.summaryLayout.addWidget(self.expensesFrame)
        
        # Accounts section
        self.accountsLabel = QLabel("Your Accounts")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.accountsLabel.setFont(font)
        
        # Empty state message
        self.emptyStateFrame = QFrame()
        self.emptyStateFrame.setFrameShape(QFrame.StyledPanel)
        emptyStateLayout = QVBoxLayout(self.emptyStateFrame)
        
        self.emptyStateLabel = QLabel("You don't have any accounts yet!")
        emptyStateFont = QFont()
        emptyStateFont.setPointSize(14)
        self.emptyStateLabel.setFont(emptyStateFont)
        self.emptyStateLabel.setAlignment(Qt.AlignCenter)
        
        self.emptyStateSubLabel = QLabel("Click the button below to add your first account")
        self.emptyStateSubLabel.setAlignment(Qt.AlignCenter)
        
        emptyStateLayout.addWidget(self.emptyStateLabel)
        emptyStateLayout.addWidget(self.emptyStateSubLabel)
        emptyStateLayout.setContentsMargins(20, 30, 20, 30)
        
        # Accounts scroll area
        self.accountsScrollArea = QScrollArea()
        self.accountsScrollArea.setWidgetResizable(True)
        self.accountsContainer = QWidget()
        self.accountsLayout = QVBoxLayout(self.accountsContainer)
        self.accountsScrollArea.setWidget(self.accountsContainer)
        
        # Add account button
        self.addAccountButton = QPushButton("+ Add New Account")
        self.addAccountButton.clicked.connect(self.showAddAccountDialog)
        
        # Actions section
        self.actionsFrame = QFrame()
        self.actionsLayout = QGridLayout(self.actionsFrame)
        
        self.transactionsButton = QPushButton("Transactions")
        self.budgetButton = QPushButton("Budget")
        self.reportsButton = QPushButton("Reports")
        self.settingsButton = QPushButton("Settings")
        
        self.actionsLayout.addWidget(self.transactionsButton, 0, 0)
        self.actionsLayout.addWidget(self.budgetButton, 0, 1)
        self.actionsLayout.addWidget(self.reportsButton, 1, 0)
        self.actionsLayout.addWidget(self.settingsButton, 1, 1)
        
        # Add all sections to main layout
        self.layout.addWidget(self.headerFrame)
        self.layout.addWidget(self.summaryFrame)
        self.layout.addWidget(self.accountsLabel)
        self.layout.addWidget(self.emptyStateFrame)
        self.layout.addWidget(self.accountsScrollArea)
        self.layout.addWidget(self.addAccountButton)
        self.layout.addWidget(self.actionsFrame)
        
        # Show/hide empty state based on account status
        self.loadAccountsFromDB()

    def loadAccountsFromDB(self):
        """Load accounts from SQLite for the current user and update total balance."""
        self.clearAccounts()
        total_balance = 0.0
        if not self.user_id:
            self.updateEmptyState()
            self.updateTotalBalance(0.0)
            self.updateIncomeAndExpenses()
            return
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT finance_account_id, finance_account_name, finance_account_type_id, finance_account_balance "
            "FROM finance_accounts WHERE user_id = ?", (self.user_id,)
        )
        for acc_id, name, type_id, balance in cursor.fetchall():
            account_type = self.getAccountTypeName(type_id)
            self._addAccountWidget(acc_id, name, balance, account_type)
            total_balance += float(balance)
        cursor.close()
        self.updateEmptyState()
        self.updateTotalBalance(total_balance)
        self.updateIncomeAndExpenses()

    def getAccountTypeName(self, type_id):
        # You can expand this mapping as needed
        mapping = {1: "Bank", 2: "Savings", 3: "Investment", 4: "Credit", 5: "Cash"}
        return mapping.get(type_id, "Other")

    def addFinanceAccount(self, name, balance, account_type_id):
        """Add account to DB and refresh view."""
        if not self.user_id:
            return
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO finance_accounts (finance_account_name, finance_account_type_id, finance_account_balance, user_id) "
            "VALUES (?, ?, ?, ?)",
            (name, account_type_id, float(balance), self.user_id)  # Use float for decimal values
        )
        self.db.commit()
        cursor.close()
        self.loadAccountsFromDB()
        self.updateIncomeAndExpenses()

    def getAccountTypeId(self, account_type):
        mapping = {1: "Bank", 2: "Savings", 3: "Investment", 4: "Credit", 5: "Cash"}
        return mapping.get(account_type, 1)

    def _addAccountWidget(self, acc_id, name, balance, account_type):
        accountFrame = QFrame()
        accountFrame.setFrameShape(QFrame.StyledPanel)
        accountLayout = QHBoxLayout(accountFrame)

        accountNameLabel = QLabel(name)
        accountTypeLabel = QLabel(account_type)
        accountBalanceLabel = QLabel(f"${balance:.2f}")

        font = QFont()
        font.setBold(True)
        accountBalanceLabel.setFont(font)

        # Add transaction button
        addTransactionButton = QPushButton("Add Transaction")
        addTransactionButton.setFixedSize(120, 30)
        addTransactionButton.setToolTip("Add Transaction")
        addTransactionButton.clicked.connect(lambda: self.showAddTransactionDialog(acc_id))

        # View Transactions button
        viewTransactionsButton = QPushButton("View Transactions")
        viewTransactionsButton.setFixedSize(120, 30)
        viewTransactionsButton.setToolTip("View Transactions for this Account")
        viewTransactionsButton.clicked.connect(lambda: self.parent().showTransactionView(acc_id, name) if self.parent() and hasattr(self.parent(), 'showTransactionView') else None)

        # Remove button with trash icon
        removeButton = QPushButton()
        removeButton.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        removeButton.setFixedSize(30, 30)
        removeButton.setToolTip("Remove Account")
        removeButton.clicked.connect(lambda: self.removeAccount(acc_id, accountFrame))

        accountLayout.addWidget(accountNameLabel)
        accountLayout.addWidget(accountTypeLabel)
        accountLayout.addStretch()
        accountLayout.addWidget(accountBalanceLabel)
        accountLayout.addWidget(addTransactionButton)
        accountLayout.addWidget(viewTransactionsButton)
        accountLayout.addWidget(removeButton)

        self.accountsLayout.addWidget(accountFrame)
        self.accounts.append(accountFrame)

    def removeAccount(self, acc_id, accountFrame):
        """Remove account from DB and UI."""
        cursor = self.db.cursor()
        # Remove transactions for this account
        cursor.execute(
            "DELETE FROM transactions WHERE finance_account_id = ?",
            (acc_id,)
        )
        cursor.execute(
            "DELETE FROM finance_accounts WHERE finance_account_id = ? AND user_id = ?",
            (acc_id, self.user_id)
        )
        self.db.commit()
        cursor.close()
        self.accountsLayout.removeWidget(accountFrame)
        if accountFrame in self.accounts:
            self.accounts.remove(accountFrame)
        accountFrame.deleteLater()
        self.updateEmptyState()
        self.loadAccountsFromDB()
        self.updateIncomeAndExpenses()

    def updateIncomeAndExpenses(self):
        """Update the monthly income and expenses summary fields for the current month."""
        if not self.user_id:
            self.updateIncome(0.0)
            self.updateExpenses(0.0)
            return
        import datetime
        now = datetime.datetime.now()
        month_start = now.replace(day=1).strftime('%Y-%m-%d')
        month_end = (now.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        month_end = month_end.strftime('%Y-%m-%d')
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT transaction_amount FROM transactions t JOIN finance_accounts a ON t.finance_account_id = a.finance_account_id WHERE a.user_id = ? AND transaction_date >= ? AND transaction_date <= ?",
            (self.user_id, month_start, month_end)
        )
        income = 0.0
        expenses = 0.0
        for (amount,) in cursor.fetchall():
            if amount >= 0:
                income += amount
            else:
                expenses += amount
        cursor.close()
        self.updateIncome(income)
        self.updateExpenses(abs(expenses))

    def updateIncome(self, value):
        valueLabel = self.incomeFrame.findChildren(QLabel)[1]
        valueLabel.setText(f"${value:.2f}")

    def updateExpenses(self, value):
        valueLabel = self.expensesFrame.findChildren(QLabel)[1]
        valueLabel.setText(f"${value:.2f}")
        
    def updateEmptyState(self):
        """Show or hide empty state message depending on accounts"""
        hasAccounts = len(self.accounts) > 0
        self.emptyStateFrame.setVisible(not hasAccounts)
        self.accountsScrollArea.setVisible(hasAccounts)

    def createSummaryBox(self, title, value):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        titleLabel = QLabel(title)
        titleFont = QFont()
        titleFont.setBold(True)
        titleLabel.setFont(titleFont)
        
        valueLabel = QLabel(value)
        valueFont = QFont()
        valueFont.setPointSize(18)
        valueLabel.setFont(valueFont)
        valueLabel.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(titleLabel)
        layout.addWidget(valueLabel)
        
        return frame
    
    def clearAccounts(self):
        for account in self.accounts:
            self.accountsLayout.removeWidget(account)
            account.deleteLater()
        self.accounts = []
        
        # Update empty state visibility
        self.updateEmptyState()

    def setUserId(self, user_id):
        """Set the user_id and reload accounts from DB."""
        self.user_id = user_id
        self.loadAccountsFromDB()

    def showAddAccountDialog(self):
        dialog = AddAccountDialog(self)
        if dialog.exec():
            name, type_id, type_name, balance = dialog.getData()
            if name:
                self.addFinanceAccount(name, balance, type_id)

    def showAddTransactionDialog(self, acc_id):
        dialog = AddTransactionDialog(self)
        if dialog.exec():
            name, amount, date = dialog.getData()
            if name and amount is not None:
                cursor = self.db.cursor()
                cursor.execute(
                    "INSERT INTO transactions (transaction_name, transaction_amount, finance_account_id, transaction_date) VALUES (?, ?, ?, ?)",
                    (name, float(amount), acc_id, date)
                )
                # Update the account balance
                cursor.execute(
                    "UPDATE finance_accounts SET finance_account_balance = finance_account_balance + ? WHERE finance_account_id = ?",
                    (float(amount), acc_id)
                )
                self.db.commit()
                cursor.close()
                self.loadAccountsFromDB()
                self.updateIncomeAndExpenses()

    def updateTotalBalance(self, value):
        """Update the total balance summary box value label."""
        # Assumes the second widget in totalBalanceFrame is the value label
        valueLabel = self.totalBalanceFrame.findChildren(QLabel)[1]
        valueLabel.setText(f"${value:.2f}")