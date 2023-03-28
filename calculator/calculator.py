import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.operand, self.operator = 0, ""
        self.setWindowTitle("Calculator")
        self.font1 = QFont()
        self.font1.setPointSize(16)
        self.font2 = QFont()
        self.font2.setPointSize(32)
        vBoxMain = QVBoxLayout()

        self.labelLog = QLabel()
        self.labelLog.setFont(self.font1)
        hBox0 = QHBoxLayout()
        hBox0.addStretch()
        hBox0.addWidget(self.labelLog)
        vBoxMain.addLayout(hBox0)

        self.labelIO = QLabel("0")
        self.labelIO.setFont(self.font2)
        hBox1 = QHBoxLayout()
        hBox1.addStretch()
        hBox1.addWidget(self.labelIO)
        vBoxMain.addLayout(hBox1)

        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.createButton("C", self.clearOnClicked))
        hBox2.addWidget(self.createButton("+/-", self.operatorOnClicked))
        hBox2.addWidget(self.createButton("%", self.operatorOnClicked))
        hBox2.addWidget(self.createButton("/", self.operatorOnClicked))
        vBoxMain.addLayout(hBox2)

        hBox3 = QHBoxLayout()
        hBox3.addWidget(self.createButton("7", self.operandOnClicked))
        hBox3.addWidget(self.createButton("8", self.operandOnClicked))
        hBox3.addWidget(self.createButton("9", self.operandOnClicked))
        hBox3.addWidget(self.createButton("X", self.operatorOnClicked))
        vBoxMain.addLayout(hBox3)

        hBox4 = QHBoxLayout()
        hBox4.addWidget(self.createButton("4", self.operandOnClicked))
        hBox4.addWidget(self.createButton("5", self.operandOnClicked))
        hBox4.addWidget(self.createButton("6", self.operandOnClicked))
        hBox4.addWidget(self.createButton("-", self.operatorOnClicked))
        vBoxMain.addLayout(hBox4)

        hBox5 = QHBoxLayout()
        hBox5.addWidget(self.createButton("1", self.operandOnClicked))
        hBox5.addWidget(self.createButton("2", self.operandOnClicked))
        hBox5.addWidget(self.createButton("3", self.operandOnClicked))
        hBox5.addWidget(self.createButton("+", self.operatorOnClicked))
        vBoxMain.addLayout(hBox5)

        hBox6 = QHBoxLayout()
        hBox6.addWidget(self.createButton("0", self.operandOnClicked))
        hBox6.addWidget(self.createButton(".", self.operandOnClicked))
        hBox6.addWidget(self.createButton("=", self.operatorOnClicked))
        vBoxMain.addLayout(hBox6)

        self.setLayout(vBoxMain)
        self.show()

    def createButton(self, text, onClicked):
        button = QPushButton(text)
        button.setFont(self.font1)
        if text == "0":
            button.setMinimumWidth(166)
        button.setMinimumHeight(64)
        button.clicked.connect(lambda: onClicked() if text == "C" else onClicked(text))
        return button

    def clearOnClicked(self):
        self.operand = 0
        self.operator = ""
        self.labelIO.setText("0")
        self.labelLog.setText("")

    def operandOnClicked(self, buttonText):
        ioText = self.labelIO.text()
        if buttonText != ".":
            if ioText == "0":
                ioText = ""
            ioText += buttonText
        elif "." not in ioText:
            ioText += "."
        self.labelIO.setText(ioText)

    def operatorOnClicked(self, buttonText):
        ioText = self.labelIO.text()
        if buttonText in ["+", "-", "X", "/", "="]:
            if self.operator == "":
                self.operand = float(ioText)
            elif self.operator == "+":
                self.operand += float(ioText)
            elif self.operator == "-":
                self.operand -= float(ioText)
            elif self.operator == "X":
                self.operand *= float(ioText)
            elif self.operator == "/":
                try:
                    self.operand /= float(ioText)
                except ZeroDivisionError:
                    self.operand = 0
            if buttonText != "=":
                self.operator = buttonText
                self.labelIO.setText("0")
                self.labelLog.setText(f"{self.castValue(self.operand)} {self.operator}")
            else:
                self.operator = ""
                self.labelIO.setText(self.castValue(self.operand))
                self.labelLog.setText("")
        elif buttonText == "+/-":
            self.labelIO.setText(self.castValue(float(ioText) * -1))
        elif buttonText == "%":
            self.labelIO.setText(self.castValue(float(ioText) / 100))

    @staticmethod
    def castValue(value):
        return str(int(value)) if value % 1 == 0 else str(value)


app = QApplication(sys.argv)
calculator = Calculator()
sys.exit(app.exec_())
