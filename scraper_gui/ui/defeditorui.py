# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_DefEditor(object):
    def setupUi(self, defeditor):
        defeditor.setObjectName(u"defeditor")
        defeditor.resize(900, 650)

        self.centralwidget = QtGui.QWidget(defeditor)
        self.centralwidget.setObjectName(u"centralwidget")
        defeditor.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        #self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addLayout(self.formLayout, 1)

        self.def_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.def_textEdit.setObjectName(u"def_textEdit")
        self.formLayout.addRow(u"Edit Def:", self.def_textEdit)

        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u"buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(defeditor.okay)
        self.buttonBox.rejected.connect(defeditor.exit)

        QtCore.QMetaObject.connectSlotsByName(defeditor)