import os
import sys
import random
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMenuBar, QMenu,QScrollArea,QMessageBox,QHeaderView)
<<<<<<< HEAD
from PySide6.QtGui import QPixmap, QColor, QAction
=======
from PySide6.QtGui import QPixmap, QColor, QAction, QIcon
>>>>>>> d7a54c3 (Added export excel tablet button, fixed drawing of iv curve)
from PySide6.QtCore import Qt

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
    
        # Get path to the text file in a cross-platform way
        file_dir = os.getcwd()  # This will get the current working directory
        file_name = "chips.txt"
        file_path = os.path.join(file_dir, file_name)

        # Open the file
        with open(file_path, "r") as names:
            chips = names.read() 
            chip_names = chips.strip().split("\n")         
        
        
        self.chips = []
        base_path = os.path.join('..', 'SiT_testing')
        
        for name in chip_names:
            file_name = f"stats_{name}.txt"
            sub_directory = f"{name}_ANLYSIS"
            file_path = os.path.join(base_path, sub_directory, file_name)
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
<<<<<<< HEAD
=======
        
        # In the __init__ method:
        self.export_button = QPushButton('Export to Excel')
        self.export_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_button)

>>>>>>> d7a54c3 (Added export excel tablet button, fixed drawing of iv curve)

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
            QAction("Sort by least badpixels Threshold", self.sort_menu),
            QAction("Sort by least badpixels ToT", self.sort_menu),
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
            elif sort_action.text() == "Sort by least badpixels Threshold":
                sort_action.triggered.connect(self.on_sort_badpixels_threshold)
            elif sort_action.text() == "Sort by least badpixels ToT":
                sort_action.triggered.connect(self.on_sort_badpixels_tot)
        
        self.combined_module_analysis_menu = QMenu("Combined Module Analysis")
        self.menuBar().addMenu(self.combined_module_analysis_menu)

        self.combined_iv_curves_action = QAction("Combined IV Curves", self.combined_module_analysis_menu)
        self.combined_module_analysis_menu.addAction(self.combined_iv_curves_action)
        self.combined_iv_curves_action.triggered.connect(self.on_combined_iv_curves)

        self.badpixels_comparison_action = QAction("Bad Pixels Comparison", self.combined_module_analysis_menu)
        self.combined_module_analysis_menu.addAction(self.badpixels_comparison_action)
        self.badpixels_comparison_action.triggered.connect(self.on_badpixels_comparison)


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
    def on_sort_badpixels_threshold(self):
        self.chips.sort(key=lambda chip: -float(chip["stats"]["Bad pixels threshold"]))
        self.update_table()
    def on_sort_badpixels_tot(self):
        self.chips.sort(key=lambda chip: -float(chip["stats"]["Bad pixels Tot"]))
        self.update_table()

    def clear_analysis_window(self):
        self.analysis_window = None

    def on_combined_iv_curves(self):
        # Display the combined IV curves picture
        self.image_window = ImageWindowcombined("../SiT_testing/all_modules_anlysis/iv_combined.png")
        self.image_window.show()

    def on_badpixels_comparison(self):
        # Display the bad pixels comparison picture
        self.image_window = ImageWindowcombined("../SiT_testing/all_modules_anlysis/sensor_badpixels_values.png")
        self.image_window.show()
<<<<<<< HEAD
=======
    def export_to_excel(self):
        # Create a dictionary to hold the data
        data = {}

        # Get the data from the table
        for i in range(self.table.columnCount()):
            column_data = []
            header = self.table.horizontalHeaderItem(i).text()
            for j in range(self.table.rowCount()):
                item = self.table.item(j, i)
                column_data.append(item.text() if item else None)
            data[header] = column_data

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Write the DataFrame to an Excel file
        df.to_excel('modules_table.xlsx', index=False)

>>>>>>> d7a54c3 (Added export excel tablet button, fixed drawing of iv curve)

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
    def __init__(self, image_path, scale_factor=0.5, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(pixmap.width()*scale_factor, pixmap.height()*scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Open the image in a new window
            self.image_window = ImageWindow(self.image_path)
            self.image_window.show()

class ImageWindowcombined(QMainWindow):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.resize(1200, 1000)

        # Load the original pixmap
        self.original_pixmap = QPixmap(self.image_path)

        # Set up the QLabel to display the image
        self.image_label = QLabel()
        self.setCentralWidget(self.image_label)

        # Initial update of the displayed image
        self.update_image()

    def resizeEvent(self, event):
        self.update_image()

    def update_image(self):
        # Scale the original pixmap to fit within the current window size, maintaining aspect ratio
        scaled_pixmap = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)


<<<<<<< HEAD
=======


>>>>>>> d7a54c3 (Added export excel tablet button, fixed drawing of iv curve)
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


        base_path = os.path.join('..', 'SiT_testing')
        file_names = [
            os.path.join(f"{chip_name}_ANLYSIS", "THRESHOLD_ANLYSIS_COMPARE", "threshold_compare.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "THRESHOLD_ANLYSIS_COMPARE", "simga_dist_compare.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "THRESHOLD_ANLYSIS2", "BadPixels_Mod_25;1.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "TOT_ANLYSIS_COMPARE", "tot_sigma_compare.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "TOT_ANLYSIS_COMPARE", "tot_mean_compare.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "TOT_ANLYSIS", "BadPixels_Mod_25;1.png"),
            os.path.join(f"{chip_name}_ANLYSIS", "iv_curve.png")
        ]

        image_paths = [os.path.join(base_path, file_name) for file_name in file_names]

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
