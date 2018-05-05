# -*- coding: utf-8 -*-

import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

import main_ui
import set_ui
from utils.utils import get_config, save_config
from utils.qiniu_api import get_buckets, get_bucket_domains, get_bucket_files

main_dialog = None
mui = None
ak = None
sk = None
cur_marker = ""


# -------- 设置状态栏显示信息 --------------
def set_status_bar(info):
    mui.status.setText(info)


# ------ start 设置AccessKey和SecretKey对话框 -------------
def save_key_set_dialog(sui, set_dialog):
    global ak, sk

    edit_ak = sui.lineEdit_ak.text()
    edit_sk = sui.lineEdit_sk.text()
    if edit_ak == "" or edit_sk == "":
        QtWidgets.QMessageBox.warning(main_dialog, '警告', "AccessKey和SecretKey都不能为空哦！")
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


# ------ end 设置AccessKey和SecretKey对话框 -------------


def init_bucket(bucket):
    global cur_marker

    # 获取仓库域名列表
    set_status_bar("正在获取仓库[%s]域名列表..." % bucket)
    ret, domains = get_bucket_domains(ak, sk, bucket)
    if ret is False:
        info = "获取仓库域名列表失败了，并确保网络畅通！"
        set_status_bar(info)
        QtWidgets.QMessageBox.warning(main_dialog, '警告', info)
        return
    set_status_bar("获取仓库[%s]域名列表成功！" % bucket)
    for i in range(0, len(domains)):
        mui.comboBox.addItem(domains[i])

    # 获取仓库文件列表
    set_status_bar("正在获取仓库[%s]文件列表..." % bucket)
    ret, files = get_bucket_files(ak, sk, bucket, cur_marker, 60, mui.lineEdit.text())
    if ret is False:
        info = "获取仓库文件列表失败了，并确保网络畅通！"
        set_status_bar(info)
        QtWidgets.QMessageBox.warning(main_dialog, '警告', info)
        return
    set_status_bar("获取仓库[%s]文件列表成功！" % bucket)
    cur_marker = files['marker']

    # 目录
    for dir in files['commonPrefixes']:
        print("DIR:" + dir)

    # 文件
    for f in files['items']:
        print("FILE:" + f['key'])


def init():
    global ak, sk

    # 检查AccessKey和SecretKey
    ak, sk = get_config()
    if ak is None:
        show_set_dialog()

    # 获取仓库列表
    set_status_bar("正在获取仓库列表...")
    ret, buckets = get_buckets(ak, sk)
    if ret is False:
        # 隐藏主界面控件
        mui.tabWidget.hide()
        mui.tableView.hide()
        mui.comboBox.hide()
        mui.lineEdit.hide()
        mui.label_domain.hide()

        info = "获取仓库列表失败了，请检查AccessKey和SecretKey，并确保网络畅通！"
        set_status_bar(info)
        QtWidgets.QMessageBox.warning(main_dialog, '警告', info)
        return
    set_status_bar("获取仓库列表成功！")

    # TODO 没有仓库, 需要新建一个仓库
    if len(buckets) == 0:
        pass
    else:
        for i in range(0, len(buckets)):
            mui.tabWidget.addTab(QtWidgets.QWidget(), buckets[i])

    # 初始化第一个仓库
    init_bucket(buckets[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog(flags=QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    main_dialog = Dialog
    Dialog.setWindowIcon(QIcon("favicon.ico"))
    ui = main_ui.Ui_Dialog()
    mui = ui
    ui.setupUi(Dialog)
    Dialog.show()
    init()
    sys.exit(app.exec_())
