# -*- coding: utf-8 -*-

# ORingSelectionDialog.py
# Diálogo de seleção de o-rings a partir dos dados normalizados
# (o-ring_pol.csv / o-ring_mm.csv / material.csv / brand.csv).

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

try:
    from PySide2 import QtCore, QtWidgets
    QT_VERSION = 2
except ImportError:
    try:
        from PySide import QtGui, QtCore
        QtWidgets = QtGui
        QT_VERSION = 1
    except ImportError:
        from PyQt5 import QtGui, QtCore, QtWidgets
        QT_VERSION = 5

from ORingData import ORingData


def _fmt(value, suffix=" mm"):
    """Formata valor numérico com vírgula decimal (padrão de catálogo)."""
    if value is None:
        return "-"
    return f"{value:g}{suffix}"


class ORingSelectionDialog(QtWidgets.QDialog):
    def __init__(self, data_dir=None, parent=None):
        super(ORingSelectionDialog, self).__init__(parent)
        self.setWindowTitle(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Select O-Ring - OpenMechanical"))
        self.setMinimumSize(850, 550)
        self.selected_key = None

        self.data = ORingData(data_dir)

        self._setup_ui()
        self._populate_table()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        header_label = QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Select the desired O-Ring:"))
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(header_label)

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Filter:")))
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Type to filter by catalog, code, ref. or table..."))
        self.filter_input.textChanged.connect(self._filter_table)
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Code"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Catalog"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Standard Ref."),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Table"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "inner d (mm)"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "w (mm)"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "outer d (mm)"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Material"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Shore A Hardness"),
            QtCore.QCoreApplication.translate("ORingSelectionDialog", "Temperature"),
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.doubleClicked.connect(self._on_generate)
        layout.addWidget(self.table)

        info_group = QtWidgets.QGroupBox(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Selected O-Ring Data"))
        info_layout = QtWidgets.QGridLayout()

        self.label_key = QtWidgets.QLabel("-")
        self.label_catalogo = QtWidgets.QLabel("-")
        self.label_ref = QtWidgets.QLabel("-")
        self.label_tabela = QtWidgets.QLabel("-")
        self.label_di = QtWidgets.QLabel("-")
        self.label_w = QtWidgets.QLabel("-")
        self.label_de = QtWidgets.QLabel("-")
        self.label_material = QtWidgets.QLabel("-")
        self.label_polimero = QtWidgets.QLabel("-")

        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Key:")), 0, 0)
        info_layout.addWidget(self.label_key, 0, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Catalog:")), 0, 2)
        info_layout.addWidget(self.label_catalogo, 0, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Standard Ref.:")), 1, 0)
        info_layout.addWidget(self.label_ref, 1, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Table:")), 1, 2)
        info_layout.addWidget(self.label_tabela, 1, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Inner Diameter:")), 2, 2)
        info_layout.addWidget(self.label_di, 2, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Section (w):")), 3, 0)
        info_layout.addWidget(self.label_w, 3, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Outer Diameter:")), 3, 2)
        info_layout.addWidget(self.label_de, 3, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Material:")), 4, 0)
        info_layout.addWidget(self.label_material, 4, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Polymer:")), 4, 2)
        info_layout.addWidget(self.label_polimero, 4, 3)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        self.table.selectionModel().currentChanged.connect(self._on_selection_changed)

        button_layout = QtWidgets.QHBoxLayout()

        self.btn_generate = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Generate O-Ring"))
        self.btn_generate.setMinimumHeight(35)
        self.btn_generate.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white;")
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_generate.setEnabled(False)

        self.btn_cancel = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("ORingSelectionDialog", "Cancel"))
        self.btn_cancel.setMinimumHeight(35)
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_generate)
        button_layout.addWidget(self.btn_cancel)
        layout.addLayout(button_layout)

    def _populate_table(self, filter_text=""):
        self.table.setRowCount(0)
        filter_lower = filter_text.lower()

        for record in self.data.records:
            haystack = " ".join([
                record.codigo, record.catalogo, record.tabela,
                record.referencia, record.norma,
                record.material, record.polimero,
            ]).lower()

            if filter_lower and filter_lower not in haystack:
                continue

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(record.codigo or "-"))
            self.table.item(row, 0).setData(QtCore.Qt.UserRole, record.key)
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(record.catalogo))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(
                f"AS568-{record.referencia}" if record.norma == "AS568" else record.referencia))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(record.tabela))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{record.di_interno:g}"))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(f"{record.secao_w:g}"))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(f"{record.de_externo:g}"))
            self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(record.material or "-"))
            self.table.setItem(row, 8, QtWidgets.QTableWidgetItem(record.dureza_shore_a or "-"))
            self.table.setItem(row, 9, QtWidgets.QTableWidgetItem(record.temperatura or "-"))

            for col in range(10):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)

    def _filter_table(self, text):
        self._populate_table(text)

    def _current_record(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item is None:
            return None
        key = item.data(QtCore.Qt.UserRole)
        if not key:
            return None
        try:
            return self.data.get_record(key)
        except ValueError:
            return None

    def _on_selection_changed(self, current, previous):
        record = self._current_record()
        if record is not None:
            self.label_key.setText(record.key)
            self.label_catalogo.setText(record.catalogo)
            self.label_ref.setText(
                f"AS568-{record.referencia}" if record.norma == "AS568" else record.referencia)
            self.label_tabela.setText(record.tabela)
            self.label_di.setText(_fmt(record.di_interno))
            self.label_w.setText(_fmt(record.secao_w))
            self.label_de.setText(_fmt(record.de_externo))
            self.label_material.setText(record.material or "-")
            self.label_polimero.setText(record.polimero or "-")
            self.btn_generate.setEnabled(True)
        else:
            self.btn_generate.setEnabled(False)
            self.label_key.setText("-")
            self.label_catalogo.setText("-")
            self.label_ref.setText("-")
            self.label_tabela.setText("-")
            self.label_di.setText("-")
            self.label_w.setText("-")
            self.label_de.setText("-")
            self.label_material.setText("-")
            self.label_polimero.setText("-")

    def _on_generate(self):
        record = self._current_record()
        if record is not None:
            self.selected_key = record.key
            self.accept()

    def get_selected_key(self):
        return self.selected_key


def select_oring(data_dir=None):
    import FreeCADGui as Gui

    parent = Gui.getMainWindow()
    dialog = ORingSelectionDialog(data_dir, parent)

    try:
        result = dialog.exec_()
    except AttributeError:
        result = dialog.exec_()

    if result:
        return dialog.get_selected_key()
    return None
