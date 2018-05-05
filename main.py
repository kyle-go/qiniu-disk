# -*- coding: utf-8 -*-

import os
import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

import set_ui
from utils.utils import get_config, save_config
from utils.qiniu_api import get_buckets, get_bucket_domains, get_bucket_files

web_view = None
ak = None
sk = None
cur_marker = ""
cur_prefix = ""
channel = None
handler = None


def get_abspath():
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:  # We are the main py2exe script, not a module
        root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    return root_dir


# ------ start 设置AccessKey和SecretKey对话框 -------------
def save_key_set_dialog(sui, set_dialog):
    global ak, sk

    edit_ak = sui.lineEdit_ak.text()
    edit_sk = sui.lineEdit_sk.text()
    if edit_ak == "" or edit_sk == "":
        QtWidgets.QMessageBox.warning(web_view, '警告', "AccessKey和SecretKey都不能为空哦！")
        return

    save_config(edit_ak, edit_sk)
    ak = edit_ak
    sk = edit_sk
    # set dialog return value
    set_dialog.accept()


def show_set_dialog():
    set_dialog = QtWidgets.QDialog(web_view, flags=QtCore.Qt.WindowCloseButtonHint)
    sui = set_ui.Ui_Dialog()
    sui.setupUi(set_dialog)
    sui.pushButton.clicked.connect(partial(save_key_set_dialog, sui, set_dialog))
    exit_code = set_dialog.exec()
    if exit_code != QtWidgets.QDialog.Accepted:
        sys.exit(0)


# ------ end 设置AccessKey和SecretKey对话框 -------------


def init():
    global ak, sk, channel, handler

    # js -> python
    channel = QWebChannel()
    handler = CallHandler()
    channel.registerObject('handler', handler)
    web_view.page().setWebChannel(channel)
    # js -> python

    # 检查AccessKey和SecretKey
    ak, sk = get_config()
    if ak is None:
        show_set_dialog()

    # 获取仓库列表
    ret, buckets = get_buckets(ak, sk)
    if ret is False:
        info = "获取仓库列表失败了，请检查AccessKey和SecretKey，并确保网络畅通！"
        QtWidgets.QMessageBox.warning(web_view, '警告', info)
        return

    # TODO 没有仓库, 需要新建一个仓库
    if len(buckets) == 0:
        pass
    else:
        pass
        # for i in range(0, len(buckets)):
        #     mui.tabWidget.addTab(QtWidgets.QWidget(), buckets[i])

    # 初始化第一个仓库
    # init_bucket(buckets[0])

    # 监听切换Tab事件
    # mui.tabWidget.currentChanged.connect(partial(change_tab, mui.tabWidget))


# js -> python
class CallHandler(QObject):
    result = pyqtSignal(int)

    @pyqtSlot(str, result=int)
    def test(self, s):
        print('call received:' + s)
        return 9992


# python -> js
def complete_name():
    web_view.page().runJavaScript('completeAndReturnName();', lambda v: print(v))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("favicon.ico"))
    web = QWebEngineView()
    web.setWindowTitle("七牛个人网盘 v1.0")
    web.load(QUrl.fromLocalFile(get_abspath() + "\\index.html"))
    web.show()
    web_view = web
    init()
    sys.exit(app.exec())
