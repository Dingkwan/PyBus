from PyQt6 import QtWidgets
import sys
import pandas as pd

app = QtWidgets.QApplication(sys.argv)

width = 600
height = 400

Form = QtWidgets.QWidget()
Form.setWindowTitle('pytrack')
Form.resize(width, height)



def open():

    filePath , filterType = QtWidgets.QFileDialog.getOpenFileNames()
    filePath = filePath[0]
    label.setText(filePath)
    data = pd.read_csv(filePath, header = None)

    data.columns = ["id", "datetime","longitude", "latitude"]

    data = data[["datetime","latitude", "longitude"]]

    # input.setPlainText(data.head().to_string(index = False))
    dataLabel.setText(data.head().to_string(index = False))
    print(data)



btn = QtWidgets.QPushButton(Form)
btn.move(50, 100)
btn.setText('open file')
btn.clicked.connect(open)

label = QtWidgets.QLabel(Form)
label.setGeometry(0, 0, width, 100)

dataLabel = QtWidgets.QLabel(Form)
dataLabel.setGeometry(0, 150, width, 150)
# input = QtWidgets.QPlainTextEdit(Form)

# input.setGeometry(0, 150, width, 150)

Form.show()

sys.exit(app.exec())
