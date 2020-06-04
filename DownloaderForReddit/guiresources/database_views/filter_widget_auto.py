# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FilterWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilterWidget(object):
    def setupUi(self, FilterWidget):
        FilterWidget.setObjectName("FilterWidget")
        FilterWidget.resize(1700, 228)
        FilterWidget.setMaximumSize(QtCore.QSize(16777215, 228))
        FilterWidget.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(FilterWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(FilterWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(FilterWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.model_combo = QtWidgets.QComboBox(FilterWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.model_combo.sizePolicy().hasHeightForWidth())
        self.model_combo.setSizePolicy(sizePolicy)
        self.model_combo.setObjectName("model_combo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.model_combo)
        self.label = QtWidgets.QLabel(FilterWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.field_combo = QtWidgets.QComboBox(FilterWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.field_combo.sizePolicy().hasHeightForWidth())
        self.field_combo.setSizePolicy(sizePolicy)
        self.field_combo.setMinimumSize(QtCore.QSize(300, 0))
        self.field_combo.setObjectName("field_combo")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.field_combo)
        self.label_2 = QtWidgets.QLabel(FilterWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.operator_combo = QtWidgets.QComboBox(FilterWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operator_combo.sizePolicy().hasHeightForWidth())
        self.operator_combo.setSizePolicy(sizePolicy)
        self.operator_combo.setObjectName("operator_combo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.operator_combo)
        self.label_3 = QtWidgets.QLabel(FilterWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.value_layout = QtWidgets.QVBoxLayout()
        self.value_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.value_layout.setObjectName("value_layout")
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.value_layout)
        self.add_filter_button = QtWidgets.QPushButton(FilterWidget)
        self.add_filter_button.setObjectName("add_filter_button")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.add_filter_button)
        self.horizontalLayout.addLayout(self.formLayout)
        self.filter_box_list_widget = QtWidgets.QListWidget(FilterWidget)
        self.filter_box_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.filter_box_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.filter_box_list_widget.setMovement(QtWidgets.QListView.Static)
        self.filter_box_list_widget.setViewMode(QtWidgets.QListView.IconMode)
        self.filter_box_list_widget.setUniformItemSizes(False)
        self.filter_box_list_widget.setWordWrap(True)
        self.filter_box_list_widget.setObjectName("filter_box_list_widget")
        self.horizontalLayout.addWidget(self.filter_box_list_widget)

        self.retranslateUi(FilterWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterWidget)

    def retranslateUi(self, FilterWidget):
        _translate = QtCore.QCoreApplication.translate
        FilterWidget.setWindowTitle(_translate("FilterWidget", "Filter"))
        self.label_4.setText(_translate("FilterWidget", "Filter"))
        self.label_5.setText(_translate("FilterWidget", "Model:"))
        self.label.setText(_translate("FilterWidget", "Field:"))
        self.label_2.setText(_translate("FilterWidget", "Operator:"))
        self.label_3.setText(_translate("FilterWidget", "Value:"))
        self.add_filter_button.setText(_translate("FilterWidget", "Add Filter"))