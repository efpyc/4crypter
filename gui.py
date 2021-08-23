# -*- coding:utf-8 -*-

import sys, os
from crypter import Fcrypter
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

defdir = os.getcwd()
crypt_key = {'key': ''}

def getOpenFilesAndDirs(parent=None, caption='', directory='', filter='', initialFilter='', options=None):
    """
    This function not coded by me.
    Source: https://stackoverflow.com/questions/64336575/select-a-file-or-a-folder-in-qfiledialog-pyqt5
    """
    def updateText():
        # update the contents of the line edit widget with the selected files
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        lineEdit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    # by default, if a directory is opened in file listing mode,
    # QFileDialog.accept() shows the contents of that directory, but we
    # need to be able to "open" directories as we can do with files, so we
    # just override accept() with the default QDialog implementation which
    # will just return exec_()
    dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    # there are many item views in a non-native dialog, but the ones displaying
    # the actual contents are created inside a QStackedWidget; they are a
    # QTreeView and a QListView, and the tree is only used when the
    # viewMode is set to QFileDialog.Details, which is not this case
    stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stackedWidget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(QtWidgets.QLineEdit)
    # clear the line edit contents whenever the current directory changes
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui()

    def ui(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("4crypter")
        self.window.setGeometry(750, 500, 420, 250)
        self.hbox = QtWidgets.QHBoxLayout()
        self.h_box = QtWidgets.QHBoxLayout()
        self.hh = QtWidgets.QHBoxLayout()
        self.keytext = QtWidgets.QLabel('Key (max size 32)')
        self.hbox.addWidget(self.keytext)
        self.keyinput = QtWidgets.QLineEdit()
        self.hbox.addWidget(self.keyinput)
        self.setbutton = QtWidgets.QPushButton('Set!')
        self.processbutton = QtWidgets.QPushButton('Encrypt/Decrypt')
        self.selectbutton = QtWidgets.QPushButton('Select file(s)/folder(s)')
        self.hbox.addWidget(self.setbutton)
        self.cryptgroup = QtWidgets.QButtonGroup(self)
        self.askgroup = QtWidgets.QButtonGroup(self)
        self.enc, self.dec = QtWidgets.QRadioButton('Encrypt'), QtWidgets.QRadioButton('Decrypt')
        self.aes, self.fernet = QtWidgets.QRadioButton('AES-256-CBC'), QtWidgets.QRadioButton('MultiFernet')
        self.askgroup.addButton(self.enc)
        self.askgroup.addButton(self.dec)
        self.cryptgroup.addButton(self.aes)
        self.cryptgroup.addButton(self.fernet)
        self.aes.setChecked(True)
        self.enc.setChecked(True)
        self.vbox = QtWidgets.QVBoxLayout()
        self.h_box.addWidget(self.enc)
        self.h_box.addWidget(self.dec)
        self.hh.addWidget(self.aes)
        self.hh.addWidget(self.fernet)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.h_box)
        self.vbox.addLayout(self.hh)
        self.vbox.addStretch()
        self.vbox.addWidget(self.selectbutton)
        self.vbox.addWidget(self.processbutton)
        self.window.setLayout(self.vbox)

        self.setbutton.clicked.connect(self.setkey)
        self.processbutton.clicked.connect(lambda : self.process(self.enc.isChecked(), self.dec.isChecked(), self.aes.isChecked()))
        self.selectbutton.clicked.connect(self.select)

        self.window.show()
    def setkey(self):
        key = self.keyinput.text()
        if not len(key) > 32 and key != "":
            crypt_key['key'] = key
            self.show_popup("Key Info", "Key is setted!", QMessageBox.Information)
            print(key, "|", crypt_key['key'])
        elif len(key) > 32:
            self.show_popup("Key Error", f"Max key length is 32, your key length is {len(key)}", QMessageBox.Critical)
        elif key == "":
            self.show_popup("Key Error", "Please set a key", QMessageBox.Critical)
    def show_popup(self, title, text, icon, buttons=None, defaultbutton=None, details=None, informative=None):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        if not buttons == None:
            msg.setStandardButtons(buttons)
            if not defaultbutton == None:
                msg.setDefaultButton(defaultbutton)
        if not details == None:
            msg.setDetailedText(details)
        if not informative == None:
            msg.setInformativeText(informative)
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()

    def select(self):
        filesfolders = getOpenFilesAndDirs(self, "Select file(s)/folder(s)", defdir)
        files = []
        folders = []
        for x in filesfolders:
            if os.path.isfile(x):
                files.append(x)
            else:
                folders.append(x)
        files.sort()
        folders.sort()
        self.data = {"files": files, "folders": folders}
        self.show_popup("Crypt Info", "Selected file(s)/folder(s)!", QMessageBox.Information, buttons=QMessageBox.Ignore|QMessageBox.Ok, defaultbutton=QMessageBox.Ok)

    def popup_button(self, button):
        self.popupbutton = str(button.text()).lower().lstrip("&")
        print(self.popupbutton)

    def process(self, enc, dec, aes):
        if self.keyinput.text() == "":
            self.show_popup("Key Error", "Please set a key.", QMessageBox.Critical)
        else:
            crypter = Fcrypter(key=crypt_key['key'])
            files, folders = self.data['files'], self.data['folders']
            file_num = len(files)
            folder_num = 0
            total = file_num
            all_paths = ""
            if file_num > 0:
                for x in files:
                    all_paths += x + "\n"
            if len(folders) > 0:
                for folder in folders:
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            all_paths += os.path.join(root, file) + "\n"
                        total += len(files)
                        folder_num += len(dirs)
            if enc:
                "Encrypt process"
                self.popuptext = f"{total} file(s) will be encrypted."
                self.show_popup("Cryption Info", self.popuptext, QMessageBox.Information,
                                buttons=QMessageBox.No | QMessageBox.Yes, defaultbutton=QMessageBox.No,
                                details=all_paths, informative="Do you accept?")
                if self.popupbutton == 'yes':
                    _all = all_paths.split('\n')
                    for x in _all:
                        if os.path.isfile(x):
                            crypter.encryptFile(x, aes=aes)
                        else:
                            crypter.encryptFolder(x, aes=aes)
                    self.show_popup("Cryption Info", "Encryption was successfully!", QMessageBox.Information)
                else:
                    self.show_popup("Cryption Info", "Encryption is canceled!", QMessageBox.Information)
            elif dec:
                "Decrypt process"
                self.popuptext = f"{total} file(s) will be decrypted."
                self.show_popup("Decrypt Info", self.popuptext, QMessageBox.Information,
                                buttons=QMessageBox.No | QMessageBox.Yes, defaultbutton=QMessageBox.No,
                                details=all_paths, informative="Do you accept?")
                if self.popupbutton == 'yes':
                    _all = all_paths.split('\n')
                    for x in _all:
                        if os.path.isfile(x):
                            crypter.decryptFile(x, aes=aes)
                        else:
                            crypter.decryptFolder(x, aes=aes)
                    self.show_popup("Cryption Info", "Decryption was successfully!", QMessageBox.Information)
                else:
                    self.show_popup("Decrypt Info", "Decryption is canceled!", QMessageBox.Information)
            else:
                self.show_popup(title="Process Error", text="Please select an option (Encrypt or Decrypt)",
                                icon=QMessageBox.Warning)

app = QtWidgets.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())