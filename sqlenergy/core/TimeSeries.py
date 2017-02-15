import logging
import collections
from datetime import datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

class TimeSeries():

    def __init__(self, all_types, minute_res):
        #Stats
        self.time_min = datetime.max
        self.time_max = datetime.min

        #Data structures
        self.all_types = sorted(all_types)
        self.time_value_map = {series_type: collections.defaultdict(float) for series_type in all_types}

        #Time resolution
        self.minute_res = minute_res

    def __str__(self):

        self.fill_time_series()

        #Header
        output = "Timestamp, %s\n" % ', '.join(self.all_types)

        #Create string of all information
        for time in perdelta(self.time_min, self.time_max, timedelta(minutes=self.minute_res)):

            #Timestamp
            output += "%s" % time

            #All values for each series, in order
            for series_type in self.all_types:
                output += ", %s" % self.time_value_map[series_type][time]
            output += "\n"

        return output

    def fill_time_series(self):
        """
        Make sure all timestamps between minimum and maximum time are filled
        """

        #Determine maximum/minimum recorded time stamps in all series
        for series_type in self.all_types:
            #self.time_value_map[series_type] = collections.OrderedDict(sorted(self.time_value_map[series_type].iteritems()))
            self.time_min = min(self.time_min,
                                min([k for k, v in self.time_value_map[series_type].iteritems()]))
            self.time_max = max(self.time_max,
                                max([k for k, v in self.time_value_map[series_type].iteritems()]))

        #For all series, fill the values
        for series_type in self.all_types:
            for time in perdelta(self.time_min, self.time_max, timedelta(minutes=self.minute_res)):
                if time not in self.time_value_map[series_type]:
                    self.time_value_map[series_type][time] = 0.0

    def stream_handler(self, series_type, stream, min_val=0, max_val=100, time_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        From an input stream, convert the data into time-series format
        """

        prev_val = None

        #Go through all values in stream
        for row in stream:

            #Format to date time object and floor time to closest minute_res
            dt = datetime.strptime(row[0], time_format)
            dt = datetime(dt.year, dt.month, dt.day, dt.hour,
                          self.minute_res*(dt.minute // self.minute_res))

            #Only process values that are not None
            if row[1] != None:

                #If first iteration
                if prev_val == None:
                    prev_val = float(row[1])
                    continue
                #Remove cumulative
                val = float(row[1]) - prev_val

                #Thresholding
                if not(val>min_val and val<max_val):
                    val = 0

                prev_val = float(row[1])
                self.time_value_map[series_type][dt] += val
            else:
                self.time_value_map[series_type][dt] += 0

