import sys
import random
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMenuBar, QMenu,QScrollArea)
from PySide6.QtGui import QPixmap, QColor, QAction
from PySide6.QtCore import Qt
import os
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMessageBox


class ClickableTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        index = self.indexAt(event.position().toPoint())
        if index.isValid():
            self.cellClicked.emit(index.row(), index.column())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SiTOperation")
        self.setGeometry(100, 100, 1100, 800)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
    
        # Create a title widget with a box around it.
        self.title_widget = QWidget()
        self.title_layout = QVBoxLayout(self.title_widget)

        self.title_label = QLabel("SiT Module Analyzer")
        self.title_label.setStyleSheet("""
            font-family: 'Courier New', monospace;
            font-size: 24px;
            padding: 5px;
            border: 2px solid #EEE;
            border-radius: 5px;
            background-color: #333;
            color: #EEE;
            margin-bottom: 20px;
            qproperty-alignment: AlignCenter;
        """)
        self.title_layout.addWidget(self.title_label)

        # Add title widget to main layout
        
        self.layout.addWidget(self.title_widget)
        with open("chips.txt", "r") as names:
                chips = names.read()
                
                chip_names = chips.strip().split("\n")
   
                
        
        
        self.chips = []
        for name in chip_names:
            file_path = f"../SiT_testing/{name}_ANLYSIS/stats_{name}.txt"
            chip = {
        "name": name,
        "stats": {}}

            with open(file_path, "r") as file:
                lines = file.readlines()
                
            for line in lines:
                # Split the line into stat_key and value
                stat_key, value = line.strip().split(": ")
                stat_key = stat_key.strip()

                # Add stat_name and value to the stats dictionary
                chip["stats"][stat_key] = value
        

            self.chips.append(chip)
        self.colors = []
        for i in range(len(chip_names)):
            # Calculate the green and red values based on the position in the list
            red = int(255 * i / (len(chip_names) - 1))
            green = 255 - red
            # Convert to hexadecimal and append to the list
            self.colors.append(f'#{red:02X}{green:02X}00')
      
  


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Create a mapping of numbers to stat names
        stat_names = list(self.chips[0]["stats"].keys())
        self.stat_mapping = {i: name for i, name in enumerate(stat_names, 1)}
        
        self.table = ClickableTableWidget()
        # Set column count to number of stats + 1 for the "Chip" column
        self.table.setColumnCount(len(stat_names) + 1)
        
        # Create header labels with numbers instead of stat names
        header_labels = ["Module"] + list(map(str, self.stat_mapping.keys()))
        self.table.setHorizontalHeaderLabels(header_labels)
        self.table.setRowCount(len(self.chips))
        
        self.update_table()
        self.table.cellClicked.connect(self.open_analysis_window)
        self.layout.addWidget(self.table)

        # Create a QLabel to act as the legend
        # Format the legend to display each key-value pair on a new line
        legend_text = "\n".join(f"{i}: {name}" for i, name in self.stat_mapping.items())
        self.legend_label = QLabel(legend_text)
        self.layout.addWidget(self.legend_label)

        self.legend_label.setAlignment(Qt.AlignCenter)
        # Set the background color to white and the text color to black
        self.legend_label.setStyleSheet("QLabel { background-color: white; color: black; border: 10px solid black;}")
        self.layout.addWidget(self.legend_label)

        #menu
        self.sort_menu = QMenu("Sort")
        self.menuBar().addMenu(self.sort_menu)

        self.sort_actions = [
            QAction("Random Sort", self.sort_menu),
            QAction("Sort by Lowest Sigma Value", self.sort_menu),
            QAction("Sort by Lowest Leakage Current", self.sort_menu),
            QAction("Sort by Highest Breakdown Voltage", self.sort_menu),
        ]

        for sort_action in self.sort_actions:
            self.sort_menu.addAction(sort_action)
            if sort_action.text() == "Random Sort":
                sort_action.triggered.connect(self.on_sort_random)
            elif sort_action.text() == "Sort by Lowest Sigma Value":
                sort_action.triggered.connect(self.on_sort_sigma)
            elif sort_action.text() == "Sort by Lowest Leakage Current":
                sort_action.triggered.connect(self.on_sort_leakage_current)
            elif sort_action.text() == "Sort by Highest Breakdown Voltage":
                sort_action.triggered.connect(self.on_sort_breakdown_voltage)

        self.analysis_window = None
       
        self.layout.addWidget(self.title_label)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #333; color: #EEE; padding: 20px; }
            QLabel { font-family: 'Courier New', monospace; font-size: 18px; }
            QTableWidget { background-color: #555; gridline-color: #777; color: #EEE; font-size: 14px; }
            QTableWidget QTableCornerButton::section { background: #555; }
            QTableWidget QHeaderView::section { background-color: #555; color: #EEE; padding: 5px; text-align: left; border: 1px solid #777; }
            QTableWidget QTableCornerButton::section { border: 1px solid #777; border-top-right-radius: 9px; border-bottom-right-radius: 9px; }
            QMenuBar { background-color: #555; color: #EEE; }
            QMenuBar::item { background-color: #555; color: #EEE; padding: 5px; margin: 2px; }
            QMenuBar::item:selected { background-color: #777; }
            QMenu { background-color: #555; color: #EEE; margin: 0px; }
            QMenu::item { background-color: #555; color: #EEE; padding: 5px 20px 5px 20px; margin: 2px; }
            QMenu::item:selected { background-color: #777; }
        """)

        # ...
        header = self.table.horizontalHeader()
       
        #self.table.setStyleSheet("QTableWidget { background-color: white; color: black; }")
        header.setSectionResizeMode(QHeaderView.Stretch)

    def update_table(self):
        for i, chip in enumerate(self.chips):
            color = QColor(self.colors[i])

            name_item = QTableWidgetItem(chip["name"])
            name_item.setBackground(color)
            self.table.setItem(i, 0, name_item)

            for j, (stat, value) in enumerate(chip["stats"].items()):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(i, j+1, item)

    def open_analysis_window(self, row, column):
        if column == 0:
            chip_name = self.table.item(row, column).text()
            chip_stats = self.chips[row]["stats"]
            if self.analysis_window is None:
                self.analysis_window = AnalysisWindow(chip_name, chip_stats, self)
                self.analysis_window.show()
            else:
                self.analysis_window.update_content(chip_name, chip_stats)

    def on_sort_random(self):
        random.shuffle(self.chips)
        self.update_table()

    def on_sort_sigma(self):
        self.chips.sort(key=lambda chip: float(chip["stats"]["Mean of sigma"]))
        self.update_table()

    def on_sort_leakage_current(self):
        self.chips.sort(key=lambda chip: float(chip["stats"]["Leakage Current[mA]"]))
        self.update_table()

    def on_sort_breakdown_voltage(self):
        self.chips.sort(key=lambda chip: -float(chip["stats"]["Breakdown Voltage/cmpl reached [V]"]))
        self.update_table()

    def clear_analysis_window(self):
        self.analysis_window = None

class ImageWindow(QMainWindow):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(image_path))
        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)


class ClickableImageLabel(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setPixmap(QPixmap(image_path))
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Open the image in a new window
            self.image_window = ImageWindow(self.image_path)
            self.image_window.show()



class AnalysisWindow(QMainWindow):
    def __init__(self, chip_name, stats, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Analysis for {chip_name}")
        # Make the window larger
        self.setGeometry(100, 100, 1800, 1200)
        self.setStyleSheet("QMainWindow { background-color: white; }")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
            
        # Create a QScrollArea to hold the images
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Create a widget and a layout for the QScrollArea
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        
        # Add images to the scroll layout
        image_paths = [f"../SiT_testing/{chip_name}_ANLYSIS/THRESHOLD_ANLYSIS_COMPARE/threshold_compare.png",f"../SiT_testing/{chip_name}_ANLYSIS/THRESHOLD_ANLYSIS_COMPARE/simga_dist_compare.png",f"../SiT_testing/{chip_name}_ANLYSIS/THRESHOLD_ANLYSIS2/BadPixels_Mod_25;1.png",f"../SiT_testing/{chip_name}_ANLYSIS/TOT_ANLYSIS_COMPARE/tot_sigma_compare.png",f"../SiT_testing/{chip_name}_ANLYSIS/TOT_ANLYSIS_COMPARE/tot_mean_compare.png",f"../SiT_testing/{chip_name}_ANLYSIS/TOT_ANLYSIS/BadPixels_Mod_25;1.png",f"../SiT_testing/{chip_name}_ANLYSIS/iv_curve.png"]
        for image_path in image_paths:
            image_label = ClickableImageLabel(image_path)
            self.scroll_layout.addWidget(image_label)
        
        # Set the scroll_widget as the widget for the scroll_area
        self.scroll_area.setWidget(self.scroll_widget)

        self.labels = []
        self.update_content(chip_name, stats)


    def update_content(self, chip_name, stats):
        self.setWindowTitle(f"Analysis for {chip_name}")
        for label in self.labels:
            label.setParent(None)
        self.labels.clear()


    def closeEvent(self, event):
        if isinstance(self.parent(), MainWindow):
            self.parent().clear_analysis_window()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
