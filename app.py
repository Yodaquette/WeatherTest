"""
    Andrew Goodman
    January 18, 2018

    The main entry point for the Weather Test app
"""
import sys
from PyQt5.QtWidgets import QApplication
from modules.application.MainWindow import MainWindow
from modules.application.WeatherDataReader import WeatherDataReader

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())


# wdr = WeatherDataReader("1089419.csv", "1089441.csv")
# print(wdr.dry_bulb_temp_ave_stddev("5/15/17", "F"))
# print(wdr.wind_chill_by_time("5/15/17"))
# print(wdr.find_most_similar_date())