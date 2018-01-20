"""
    Andrew Goodman
    January 18, 2018

    The class WeatherDataReader provides three operations:

    1) dry_bulb_temp_ave_stddev(date, scale):

    This function takes as arguments a date to examine and the
    user's temperature scale of choice (C or F), and computes
    the mean and standard deviation of the temperature
    values recorded between sunrise and sunset

    2) wind_chill_by_time(date, threshold = 40):

    This function takes as arguments a date to examine and
    an upper temperature threshold, and returns the
    wind chill rounded to the nearest integer for the times
    when the temperature is less than the value of threshold
    (defaults to 40 degrees on the Fahrenheit scale)

    3) find_most_similar_date():

    This function reads the two datasets and finds the day
    in which the conditions in Canadian, TX, were most
    similar to Atlanta's Hartsfield-Jackson Airport
"""
import csv, statistics
from decimal import Decimal, ROUND_HALF_EVEN
from datetime import datetime


class WeatherDataReader():
    def __init__(self, f1, f2):
        self.dataset1 = self._read_data_file(f1)
        self.dataset2 = self._read_data_file(f2)
    
    def dry_bulb_temp_ave_stddev(self, date, scale):
        """
        This method takes a date as its argument
        and returns a data structure with the average and
        standard deviation of the temperature (dry-bulb)
        between the hours of sunrise and sunset

        :param date: date value formatted as month/day/year
        :param scale: temperature scale to use, "c" or "f"

        :returns: a tuple containing average temperature and
        standard deviation
        """
        # Check for empty date
        if (not date):
            return -1
        # Check for malformed date format
        if (len(date.split("/")[2]) > 2):
            print("Date value is incorrect: {0}".format(date))
            return -2

        # Determine temperature scale
        if (scale.lower() == "c"):
            temp_col = "HOURLYDRYBULBTEMPC"
        elif (scale.lower() == "f"):
            temp_col = "HOURLYDRYBULBTEMPF"

        # List will hold the temperature values within
        # the appropriate time range from sunrise to
        # sunset
        temps = []

        # Date found flag will change to "True" if
        # the submitted date is found
        date_found = False

        for row in self.dataset1:
            # Try to find the provided date in the file
            if (str(date) == row["DATE"].split(' ')[0]):
                date_found = True

                # Convert time value to an int
                time_of_day = int(row["DATE"].split(' ')[1].replace(":", ""))

                # Determine if the time is in the range from
                # sunrise to sunset
                if (time_of_day >= int(row["DAILYSunrise"]) and time_of_day <= int(row["DAILYSunset"])):

                    # Ensure a temperature value exists
                    # before appending it to the list temps[]
                    if (row[temp_col] != ""):
                        temps.append(Decimal(row[temp_col]))
            
        # Notify user if date not found in data
        # and return error
        if (date_found is False):
            print("Could not find date {0} in data".format(date))
            return -3
        
        return ("Temperature Mean: {0}\n".format(statistics.mean(temps)), \
            "Temperature Standard Deviation: {0}".format(statistics.stdev(temps)))

    def wind_chill_by_time(self, date, threshold):
        """
        This method takes a date as its argument and returns the
        wind chill rounded to the nearest integer for the times
        when the temperature is less than the value of the argument
        threshold (defaults to 40 degrees on the Fahrenheit scale)

        :param date: date value formatted as month/day/year
        :param threshold: the temperature value to use for the threshold

        :returns: a dictionary containing the time of day and
        the wind chill when the temperature is below the argument
        threshold
        """
        # Check for empty date
        if (not date):
            return -1
        # Check for malformed date format
        if (len(date.split("/")[2]) > 2):
            print("Date value is incorrect: {0}".format(date))
            return -2
        # Check for a threshold value of 0 or less
        if (threshold <= 0):
            print("Threshold value must be greater than 0: {0}".format(threshold))
            return -3

        # Dictionary to hold the "time" : "wind chill" pairs
        wind_chill = []

        # Date found flag will change to "True" if
        # the submitted date is found
        date_found = False

        for row in self.dataset1:
            # Try to find the provided date in the file
            if (str(date) == row["DATE"].split(' ')[0]):
                date_found = True

                # Ensure a temperature value exists before rounding
                if (row["HOURLYWindSpeed"] != ""):

                    # Round temperature value to nearest integer
                    dec = Decimal(row["HOURLYWindSpeed"]).quantize(Decimal(1), \
                        rounding = ROUND_HALF_EVEN)

                    # Add wind chill values that are less than the threshhold
                    if (dec < threshold):
                        wind_chill.append("{0} : {1}\n".format(row["DATE"].split(' ')[1], dec))
        
        # Notify user if date not found in data
        # and return error
        if (date_found is False):
            print("Could not find date {0} in data".format(date))
            return -4
        
        return wind_chill

    def find_most_similar_date(self, threshold):
        """
        This method reads two data sets and finds the day
        in which the conditions in Canadian, TX, were most
        similar to Atlanta's Hartsfield-Jackson Airport

        :param threshold: the temperature value to use as the difference threshold
        """
        # Check for a threshold value of 0 or less
        if (threshold <= 0):
            print("Threshold value must be greater than 0: {0}".format(threshold))
            return -1

        # Ensure the datasets contain data for the same year(s)
        self._match_dataset_dates()

        # Most similar weather data will be stored in this list
        most_similar = []

        ## Data to use in evaluation:
        ##
        ## DAILYAverageDryBulbTemp

        # Iterate over the datasets until the most similar
        # conditions are found
        for data1 in self.dataset1:
            for data2 in self.dataset2:

                # If the date for the inner loop is greater than the
                # outer loop then break
                if (datetime.strptime(data1["DATE"].split(" ")[0].strip(), "%m/%d/%y").date() <=
                    datetime.strptime(data2["DATE"].split(" ")[0].strip(), "%m/%d/%y").date()):

                    # If a date match is found then continue looking for similar conditions
                    if (data1["DATE"].split(" ")[0] == data2["DATE"].split(" ")[0]):

                        # Ensure DAILYAverageDryBulbTemp has a value
                        if (data1["DAILYAverageDryBulbTemp"] != "" and data2["DAILYAverageDryBulbTemp"] != ""):

                            # Calculate the difference between data points
                            dry_bulb_diff = self._difference_between_datapoints(
                                data1["DAILYAverageDryBulbTemp"],
                                data2["DAILYAverageDryBulbTemp"])
                            
                            # Check the difference within the threshold
                            if (dry_bulb_diff <= threshold):
                                
                                # If the list most_similar is empty or if
                                # the difference in temperature is less than
                                # the current lowest value
                                if (not most_similar or dry_bulb_diff < most_similar[3]):
                                    most_similar.append("Most similar date: {0}\n".format(data1["DATE"].split(" ")[0].strip()))
                                    most_similar.append("Canadian, TX, Average Daily Temperature: {0}\n".format(
                                        data1["DAILYAverageDryBulbTemp"]))
                                    most_similar.append("Atlanta Hartsfield International Airport, GA, Average Daily Temperature: {0}\nTemperature difference: ".format(
                                        data2["DAILYAverageDryBulbTemp"]))
                                    most_similar.append(dry_bulb_diff)
                    else:
                        continue
                else:
                    break
        return most_similar

    def _read_data_file(self, data_file):
        """
        Helper function

        Reads data from a CSV file into a dictionary

        :param data_file: the data file to read

        :returns: a dictionary data structure of the
        data read from argument data_file
        """
        try:
            with open(data_file, newline = '') as f:
                reader = csv.DictReader(f)
                data = []
                for row in reader:
                    data.append(row)
        except OSError as err:
            print("An exception occurred: {0}".format(err))
        return data

    def _match_dataset_dates(self):
        """
        Helper function

        Iterate through two datasets and remove rows
        that do not have a corresponding year values
        in their "DATE" value
        """
        years_in_dataset = []
        for data1 in self.dataset1:
            year = str(datetime.strptime(data1["DATE"].split("/")[2].split(" ")[0], \
                "%y").date()).split("-")[0]
            if (year not in years_in_dataset):
                years_in_dataset.append(year)

        year = str(datetime.strptime(self.dataset2[0]["DATE"].split("/")[2].split(" ")[0], \
                "%y").date()).split("-")[0]
        while(year not in years_in_dataset):
            year = str(datetime.strptime(self.dataset2[0]["DATE"].split("/")[2].split(" ")[0], \
                "%y").date()).split("-")[0]
            if (year not in years_in_dataset):
                try:
                    del self.dataset2[0]
                except KeyError as key_err:
                    print("KeyError: {0}".format(key_err))

    def _isolate_daily_data(self, dataset):
        """
        Helper function

        Iterate through a dataset and remove any rows where
        the "DAILY" data is empty

        :param dataset: the set of data to examine
        """
        pass
        # index = 0
        # for data in dataset:
        #     if (data["DAILYAverageDryBulbTemp"] == "" or data["DAILYAverageDryBulbTemp"].isspace()):
        #         del dataset[]
    
    def _difference_between_datapoints(self, datapoint1, datapoint2):
        """
        Helper function

        Calculate the difference between data points

        :param datapoint1: the first data point
        :param datapoint2: the second data point

        :returns: the absolute value of the difference between data points
        """
        return abs(int(datapoint1) - int(datapoint2))