import mysql.connector
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QScrollArea, QGridLayout,
                              QSpacerItem, QSizePolicy, QStyle)
from PySide6.QtGui import QFont, QIcon

class DashboardView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="finedu"
        )
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
        self.addAccountButton.clicked.connect(lambda: self.addAccount("New Account", 0.00, "Checking"))
        
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
        """Load accounts from MySQL for the current user."""
        self.clearAccounts()
        if not self.user_id:
            self.updateEmptyState()
            return
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT finance_account_id, finance_account_name, finance_account_type_id, finance_account_balance "
            "FROM finance_accounts WHERE user_id = %s", (self.user_id,)
        )
        for acc_id, name, type_id, balance in cursor.fetchall():
            account_type = self.getAccountTypeName(type_id)
            self._addAccountWidget(acc_id, name, balance, account_type)
        cursor.close()
        self.updateEmptyState()

    def getAccountTypeName(self, type_id):
        # You can expand this mapping as needed
        mapping = {1: "Checking", 2: "Savings", 3: "Investment", 4: "Credit"}
        return mapping.get(type_id, "Other")

    def addAccount(self, name, balance, account_type):
        """Add account to DB and refresh view."""
        if not self.user_id:
            return
        type_id = self.getAccountTypeId(account_type)
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO finance_accounts (finance_account_name, finance_account_type_id, finance_account_balance, user_id) "
            "VALUES (%s, %s, %s, %s)",
            (name, type_id, int(balance), self.user_id)
        )
        self.db.commit()
        cursor.close()
        self.loadAccountsFromDB()

    def getAccountTypeId(self, account_type):
        mapping = {"Checking": 1, "Savings": 2, "Investment": 3, "Credit": 4}
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
        accountLayout.addWidget(removeButton)

        self.accountsLayout.addWidget(accountFrame)
        self.accounts.append(accountFrame)

    def removeAccount(self, acc_id, accountFrame):
        """Remove account from DB and UI."""
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM finance_accounts WHERE finance_account_id = %s AND user_id = %s",
            (acc_id, self.user_id)
        )
        self.db.commit()
        cursor.close()
        self.accountsLayout.removeWidget(accountFrame)
        if accountFrame in self.accounts:
            self.accounts.remove(accountFrame)
        accountFrame.deleteLater()
        self.updateEmptyState()

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