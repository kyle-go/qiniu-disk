# coding=utf-8

import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

import main_ui
import set_ui
from utils import get_config, save_config

main_dialog = None
ak = None
sk = None


def save_key_set_dialog(sui, set_dialog):
    global ak, sk

    edit_ak = sui.lineEdit_ak.text()
    edit_sk = sui.lineEdit_sk.text()
    if edit_ak == "" or edit_sk == "":
        QtWidgets.QMessageBox.information(main_dialog, '警告', "AccessKey和SecretKey都不能为空哦！")
        return

    save_config(edit_ak, edit_sk)
    ak = edit_ak
    sk = edit_sk
    # set dialog return value
    set_dialog.accept()


def show_set_dialog():
    set_dialog = QtWidgets.QDialog(main_dialog, flags=QtCore.Qt.WindowCloseButtonHint)
    sui = set_ui.Ui_Dialog()
    sui.setupUi(set_dialog)
    sui.pushButton.clicked.connect(partial(save_key_set_dialog, sui, set_dialog))
    exit_code = set_dialog.exec()
    if exit_code != QtWidgets.QDialog.Accepted:
        sys.exit(0)


def init():
    global ak, sk

    # 检查AccessKey和SecretKey
    ak, sk = get_config()
    if ak is None:
        show_set_dialog()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog(flags=QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    main_dialog = Dialog
    Dialog.setWindowIcon(QIcon("favicon.ico"))
    ui = main_ui.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    init()
    sys.exit(app.exec_())
