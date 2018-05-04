# coding=utf-8

import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import main_ui
import set_ui


def show_set_dialog():
    set_Dialog = QtWidgets.QDialog(main_Dialog, flags=QtCore.Qt.WindowCloseButtonHint)
    sui = set_ui.Ui_Dialog()
    sui.setupUi(set_Dialog)
    set_Dialog.show()


def init():
    # 检查AccessKey和SecretKey
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog(flags=QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    main_Dialog = Dialog
    Dialog.setWindowIcon(QIcon("favicon.ico"))
    ui = main_ui.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    init()
    sys.exit(app.exec_())
