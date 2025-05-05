from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem)

# Size contants for layout
initWidth = 800
initHeight = 600
horizontalSpacerWidth = 40    
horizontalSpacerHeight = 20
verticalSpacerWidth = 20
verticalSpacerHeight = 10
formWidgetsFrameMinimumWidth = 250
formWidgetsFrameMaximumWidth = 400
buttonMinimumHeight = 50


class MainView(QWidget):
    def setUpUI(self):
        self.setObjectName("main_view")
        
        # Vertical box layout for the main view window
        self.mainVerticalLayout = QVBoxLayout(self)
        
        # Horizontal box layout for the main view window
        self.mainHorizontalLayout = QHBoxLayout(self)
        
        # Spacer items for main view layouts
        self.verticalSpacerExpanding = QSpacerItem(verticalSpacerWidth, verticalSpacerHeight, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalSpacerFixed = QSpacerItem(verticalSpacerWidth, verticalSpacerHeight, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalSpacerExpanding = QSpacerItem(horizontalSpacerWidth, horizontalSpacerHeight, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Create widget group frame
        self.formWidgetsFrame = QFrame()
        self.formWidgetsFrame.setObjectName("form_widgets")
        self.formWidgetsFrame.setMinimumWidth(formWidgetsFrameMinimumWidth)
        self.formWidgetsFrame.setMaximumWidth(formWidgetsFrameMaximumWidth)
        
        # Layout for the main view form
        self.formLayout = QVBoxLayout(self.formWidgetsFrame)
        
        # Title label
        self.titleLabel = QLabel()
        self.titleLabel.setObjectName("title_label")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Log in button
        self.logInButton = QPushButton()
        self.logInButton.setObjectName("log_in_button")
        self.logInButton.setMinimumHeight(buttonMinimumHeight)
        self.logInButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Register button
        self.registerButton = QPushButton()
        self.registerButton.setObjectName("register_button")
        self.registerButton.setMinimumHeight(buttonMinimumHeight)
        self.registerButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Setting up layout for the main view form
        self.formLayout.addItem(self.verticalSpacerExpanding)
        self.formLayout.addWidget(self.titleLabel)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.logInButton)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.registerButton)
        self.formLayout.addItem(self.verticalSpacerExpanding)
        
        # Setting up horizontal layout for the main view window
        self.mainHorizontalLayout.addItem(self.horizontalSpacerExpanding)
        self.mainHorizontalLayout.addWidget(self.formWidgetsFrame)
        self.mainHorizontalLayout.addItem(self.horizontalSpacerExpanding)
        
        # Setting up vertical layout for the main view window
        self.mainVerticalLayout.addItem(self.verticalSpacerExpanding)
        self.mainVerticalLayout.addLayout(self.mainHorizontalLayout)
        self.mainVerticalLayout.addItem(self.verticalSpacerExpanding)
        
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        

    def retranslateUi(self):
        self.logInButton.setText(QCoreApplication.translate("mainView", "Log in", None))
        self.registerButton.setText(QCoreApplication.translate("mainView", "Create an account", None))
        self.titleLabel.setText(QCoreApplication.translate("mainView", "FinEdu by jerryntom", None))