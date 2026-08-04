import json
import os

try:
    from PySide2 import QtGui, QtCore, QtWidgets
    QT_VERSION = 2
except ImportError:
    try:
        from PySide import QtGui, QtCore
        QtWidgets = QtGui
        QT_VERSION = 1
    except ImportError:
        from PyQt5 import QtGui, QtCore, QtWidgets
        QT_VERSION = 5


class BearingSelectionDialog(QtWidgets.QDialog):
    def __init__(self, json_filename="bearing_data.json", parent=None):
        super(BearingSelectionDialog, self).__init__(parent)
        self.setWindowTitle(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Select Bearing - OpenMechanical"))
        self.setMinimumSize(650, 500)
        self.selected_designation = None
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, json_filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        self._setup_ui()
        self._populate_table()
    
    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        header_label = QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Select the desired bearing:"))
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(header_label)
        
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Filter:")))
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Type to filter by model or family..."))
        self.filter_input.textChanged.connect(self._filter_table)
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "Model"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "Family"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "d (mm)"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "D (mm)"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "B (mm)"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "Balls"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "Ball (mm)"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "rmin (mm)"),
            QtCore.QCoreApplication.translate("BearingSelectionDialog", "Protection"),
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.doubleClicked.connect(self._on_generate)
        layout.addWidget(self.table)
        
        info_group = QtWidgets.QGroupBox(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Selected Bearing Dimensions"))
        info_layout = QtWidgets.QGridLayout()
        
        self.label_model = QtWidgets.QLabel("-")
        self.label_d = QtWidgets.QLabel("-")
        self.label_D = QtWidgets.QLabel("-")
        self.label_B = QtWidgets.QLabel("-")
        self.label_balls = QtWidgets.QLabel("-")
        self.label_ball_dia = QtWidgets.QLabel("-")
        
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Model:")), 0, 0)
        info_layout.addWidget(self.label_model, 0, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Inner Diameter (d):")), 0, 2)
        info_layout.addWidget(self.label_d, 0, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Outer Diameter (D):")), 1, 0)
        info_layout.addWidget(self.label_D, 1, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Width (B):")), 1, 2)
        info_layout.addWidget(self.label_B, 1, 3)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Nr. of Balls:")), 2, 0)
        info_layout.addWidget(self.label_balls, 2, 1)
        info_layout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Ball Diameter:")), 2, 2)
        info_layout.addWidget(self.label_ball_dia, 2, 3)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        self.table.selectionModel().currentChanged.connect(self._on_selection_changed)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        self.btn_generate = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Generate Bearing"))
        self.btn_generate.setMinimumHeight(35)
        self.btn_generate.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white;")
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_generate.setEnabled(False)
        
        self.btn_cancel = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("BearingSelectionDialog", "Cancel"))
        self.btn_cancel.setMinimumHeight(35)
        self.btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(self.btn_generate)
        button_layout.addWidget(self.btn_cancel)
        layout.addLayout(button_layout)
    
    def _populate_table(self, filter_text=""):
        self.table.setRowCount(0)
        filter_lower = filter_text.lower()
        
        sorted_designations = sorted(self.data.keys())
        
        for designation in sorted_designations:
            bearing = self.data[designation]
            family = bearing.get("family", "")
            dims = bearing.get("dimensions", {})
            
            if filter_lower and filter_lower not in designation.lower() and filter_lower not in family.lower():
                continue
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(designation))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(family))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(dims.get("d", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(dims.get("D", ""))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(dims.get("B", ""))))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(bearing.get("balls", ""))))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(bearing.get("ball_diameter", ""))))
            self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(bearing.get("rmin", ""))))
            self.table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(bearing.get("shield", "Open"))))
            
            for col in range(9):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
    
    def _filter_table(self, text):
        self._populate_table(text)
    
    def _on_selection_changed(self, current, previous):
        row = current.row()
        if row >= 0:
            designation = self.table.item(row, 0).text()
            if designation in self.data:
                bearing = self.data[designation]
                dims = bearing.get("dimensions", {})
                
                self.label_model.setText(designation)
                self.label_d.setText(f"{dims.get('d', '-')} mm")
                self.label_D.setText(f"{dims.get('D', '-')} mm")
                self.label_B.setText(f"{dims.get('B', '-')} mm")
                self.label_balls.setText(str(bearing.get("balls", "-")))
                self.label_ball_dia.setText(f"{bearing.get('ball_diameter', '-')} mm")
                
                self.btn_generate.setEnabled(True)
        else:
            self.btn_generate.setEnabled(False)
            self.label_model.setText("-")
            self.label_d.setText("-")
            self.label_D.setText("-")
            self.label_B.setText("-")
            self.label_balls.setText("-")
            self.label_ball_dia.setText("-")
    
    def _on_generate(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_designation = self.table.item(row, 0).text()
            self.accept()
    
    def get_selected_designation(self):
        return self.selected_designation


def select_bearing(json_filename="bearing_data.json"):
    import FreeCADGui as Gui
    
    parent = Gui.getMainWindow()
    dialog = BearingSelectionDialog(json_filename, parent)
    
    try:
        result = dialog.exec_()
    except AttributeError:
        result = dialog.exec_()
    
    if result:
        return dialog.get_selected_designation()
    return None
