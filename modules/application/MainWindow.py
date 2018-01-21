"""
    Andrew Goodman
    January 18, 2018

    Main window of the application
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QMessageBox,
    QLabel, QLineEdit, QTextEdit, QGridLayout, QAction,
    QPushButton, QButtonGroup, QRadioButton)
from modules.application.WeatherDataReader import WeatherDataReader


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.output = QTextEdit()
        self.date = QLineEdit(self)
        self.scale = ""
        self.celsius = QRadioButton("Celsius")
        self.farenheit = QRadioButton("Farenheit")
        self.threshold = QLineEdit(self)

        # Default threshold to 40
        self.threshold.setText("40")

        # Laod the user interface
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface
        """
        # Output area
        lbl_output = QLabel("Test Output")
        self.output.setReadOnly(True)
        self.output.setWordWrapMode(1)

        # Grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # Add output widgets to the window
        # grid.addWidget(widget, row, col, rowspan, colspan)
        grid.addWidget(lbl_output, 1, 1)
        grid.addWidget(self.output, 2, 1, 5, 5)

        # Setup text box and label for date entry
        lbl_date = QLabel("Date")
        grid.addWidget(lbl_date, 7, 0, 1, 1)
        grid.addWidget(self.date, 7, 1, 1, 1)
        self.date.setPlaceholderText("M/D/YY")

        # Action -> set scale
        action_set_scale = QAction("&SetScale", self)
        action_set_scale.triggered.connect(self.set_scale)

        # Radio buttons for scale
        lbl_scale = QLabel("Temperature Scale")
        rad_group = QButtonGroup(self)
        rad_group.addButton(self.celsius)
        rad_group.addButton(self.farenheit)
        grid.addWidget(lbl_scale, 8, 0, 1, 1)
        grid.addWidget(self.celsius, 8, 1, 1, 1)
        grid.addWidget(self.farenheit, 8, 2, 1, 1)
        self.celsius.toggled.connect(self.set_scale)
        self.farenheit.toggled.connect(self.set_scale)

        # Setup text box and label for threshold
        lbl_threshold = QLabel("Threshold (in F)")
        grid.addWidget(lbl_threshold, 9, 0, 1, 1)
        grid.addWidget(self.threshold, 9, 1, 1, 1)

        # Action -> call dry_bulb_temp_ave_stddev
        action_dry_bulb_temp_ave_stddev = QAction("&CallDryBulbTempAveStdDev", self)
        action_dry_bulb_temp_ave_stddev.setStatusTip("call function dry_bulb_temp_ave_stddev")
        action_dry_bulb_temp_ave_stddev.triggered.connect(self.get_temp_stats_for_date)

        # Button -> call dry_bulb_temp_ave_stddev
        btn_call_dry_bulb_temp_ave_stddev = QPushButton("Calculate Mean and Std. Deviation Dry Bulb Temp for a Date", self)
        btn_call_dry_bulb_temp_ave_stddev.clicked.connect(self.get_temp_stats_for_date)
        grid.addWidget(btn_call_dry_bulb_temp_ave_stddev, 10, 1, 1, 1)

        # Action -> call wind_chill_by_time
        action_wind_chill_by_time = QAction("&CallWindChillByTime", self)
        action_wind_chill_by_time.setStatusTip("call function wind_chill_by_time")
        action_wind_chill_by_time.triggered.connect(self.get_wind_chill_by_time)

        # Button -> call wind_chill_by_time
        btn_call_wind_chill_by_time = QPushButton("Get the Wind Chill by Time for a Date", self)
        btn_call_wind_chill_by_time.clicked.connect(self.get_wind_chill_by_time)
        grid.addWidget(btn_call_wind_chill_by_time, 11, 1, 1, 1)

        # Action -> call find_most_similar_date
        action_find_most_similar_date = QAction("&CallFindMostSimilarDate", self)
        action_find_most_similar_date.setStatusTip("call function find_most_similar_date")
        action_find_most_similar_date.triggered.connect(self.get_most_similar_weather_by_date)

        # Button -> call find_most_similar_date
        btn_call_find_most_similar_date = QPushButton("Find the Most Similar Date Between Datasets")
        btn_call_find_most_similar_date.clicked.connect(self.get_most_similar_weather_by_date)
        grid.addWidget(btn_call_find_most_similar_date, 12, 1, 1, 1)

        # Action -> show instructions
        action_show_instructions = QAction("&ShowInstructions", self)
        action_show_instructions.setShortcut("Ctrl+I")
        action_show_instructions.setStatusTip("show application instructions")
        action_show_instructions.triggered.connect(self.show_app_instructions)

        # Button -> show instructions
        btn_show_instructions = QPushButton("Show Instructions", self)
        btn_show_instructions.clicked.connect(self.show_app_instructions)
        grid.addWidget(btn_show_instructions, 13, 1, 1, 1)

        # Action -> exit application
        action_exit = QAction("&Exit", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.setStatusTip("exit the application")
        action_exit.triggered.connect(self.exit_application)

        # Button -> exit application
        btn_exit = QPushButton("Exit", self)
        btn_exit.clicked.connect(self.exit_application)
        grid.addWidget(btn_exit, 14, 1, 1, 1)

        # Set the layout to the grid
        self.setLayout(grid)

        # Default the output to show application instructions
        self.show_app_instructions()

        # Set window options then show
        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle("Weather Test")
        self.show()
    
    def get_temp_stats_for_date(self):
        """
        Call WeatherDataReader function dry_bulb_temp_ave_stddev
        """
        # Show error if temperature scale not set
        if (self.celsius.isChecked() == False and self.farenheit.isChecked() == False):
            self.output.clear()
            self.write_text("Please select a temperature scale")
            return

        # Instantiate object and call the function
        wdr = WeatherDataReader("1089419.csv", "1089441.csv")
        ret = wdr.dry_bulb_temp_ave_stddev(self.date.text(), self.scale)
        
        # Handle errors
        if (not ret):
            self.output.clear()
            self.write_text("Nothing returned from the function")
            return
        elif (ret == -1):
            self.output.clear()
            self.write_text("Date value is empty. Please enter a date in the format M/D/YY")
            return
        elif (ret == -2):
            self.output.clear()
            self.write_text("Date value {0} is invalid. Please use format M/D/YY".format(self.date.text()))
            return
        elif (ret == -3):
            self.output.clear()
            self.write_text("Date value {0} not found in data".format(self.date.text()))
            return

        # Show data returned from the function
        self.output.clear()
        # self.write_text(str(ret))
        for data in ret:
            self.write_text("{0}".format(data))
    
    def get_wind_chill_by_time(self):
        """
        Call WeatherDataReader function get_wind_chill_by_time
        """
        # Show error if the threshold value is empty
        if (self.threshold.text() == ""):
            self.output.clear()
            self.write_text("Please enter a value for threshold")
            return

        # Instantiate object and call the function
        wdr = WeatherDataReader("1089419.csv", "1089441.csv")
        ret = wdr.wind_chill_by_time(self.date.text(), int(self.threshold.text()))

        # Handle errors
        if (not ret):
            self.output.clear()
            self.write_text("Nothing returned from the function")
            return
        elif (ret == -1):
            self.output.clear()
            self.write_text("Date value is empty. Please enter a date in the format M/D/YY")
            return
        elif (ret == -2):
            self.output.clear()
            self.write_text("Date value {0} is invalid. Please use format M/D/YY".format(self.date.text()))
            return
        elif (ret == -3):
            self.output.clear()
            self.write_text("Threshold value must be greater than 0, currently {0}".format(self.threshold.text()))
            return
        elif (ret == -4):
            self.output.clear()
            self.write_text("Date value {0} not found in data".format(self.date.text()))
            return

        # Show data returned from the function
        self.output.clear()
        # self.write_text(str(ret))
        for data in ret:
            self.write_text("{0}".format(data))

    def get_most_similar_weather_by_date(self):
        """
        Call WeatherDataReader function find_most_similar_date
        """
        # Show error if the threshold value is empty
        if (self.threshold.text() == ""):
            self.output.clear()
            self.write_text("Please enter a value for threshold")
            return

        # Instantiate object and call the function
        wdr = WeatherDataReader("1089419.csv", "1089441.csv")
        ret = wdr.find_most_similar_date(int(self.threshold.text()))

        # Handle errors
        if (not ret):
            self.output.clear()
            self.write_text("Nothing returned from the function")
            return
        elif (ret == -1):
            self.output.clear()
            self.write_text("Threshold value must be greater than 0, currently {0}".format(self.threshold.text()))
            return

        # Show data returned from the function
        self.output.clear()
        # self.write_text(str(ret))
        for data in ret:
            self.write_text("{0}".format(data))

    def set_scale(self):
        """
        Set the temperature scale to Celsius or Farenheit
        """
        if (self.celsius.isChecked()):
            self.scale = "c"
        elif (self.farenheit.isChecked()):
            self.scale = "f"

    def show_app_instructions(self):
        """
        Show the instructions for the application
        """
        if (self.output.toPlainText() == ""):
            self.write_text("See simple weather stats for Canadian, TX, and ATL Hartsfield International Airport, GA\n\n" + 
                "Press the button 'Calculate Mean and Std. Deviation Dry Bulb Temp for a Date' " +
                "to see the mean and standard deviation for the date entered in the Date textbox " +
                "according to your temperature scale of preference.\n\n" +
                "Press the button 'Get the Wind Chill by Time for a Date' " +
                "to see the wind chill values recorded that fall below a threshold you specify below.\n\n" +
                "Press the button 'Find the Most Similar Date Between Datasets' " +
                "to see the date with the most similar weather between the datasets.")
            return

        option = QMessageBox.question(self, "Message",
            "Showing instructions will erase current results", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if (option == QMessageBox.Yes):
            self.output.clear()
            self.write_text("See simple weather stats for Canadian, TX, and ATL Hartsfield International Airport, GA\n\n" + 
                "Press the button 'Calculate Mean and Std. Deviation Dry Bulb Temp for a Date' " +
                "to see the mean and standard deviation for the date entered in the Date textbox " +
                "according to your temperature scale of preference.\n\n" +
                "Press the button 'Get the Wind Chill by Time for a Date' " +
                "to see the wind chill values recorded that fall below a threshold you specify below.\n\n" +
                "Press the button 'Find the Most Similar Date Between Datasets' " +
                "to see the date with the most similar weather between the datasets.")
        else:
            pass
    
    def write_text(self, txt):
        """
        Write application instructions to the QTextEdit
        textarea

        :param txt: the text to write
        """
        self.output.insertPlainText(txt)
    
    def exit_application(self):
        """
        Exit the application
        """
        option = QMessageBox.question(self, "Message",
            "Are you sure you want to exit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if (option == QMessageBox.Yes):
            print("quit application")
            self.close()
        else:
            pass