import collections
from datetime import datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

class TimeSeries():

    def __init__(self, all_types, minute_res):
        self.time_min = datetime.max
        self.time_max = datetime.min
        self.all_types = all_types
        self.time_value_map = {series_type: collections.defaultdict(float) for series_type in all_types}
        self.minute_res = minute_res

    def __str__(self):

        self.fill_time_series()

        output = "Timestamp, %s\n" % ', '.join(self.all_types)

        for time in perdelta(self.time_min, self.time_max, timedelta(minutes=self.minute_res)):

            output += "%s" % time

            for series_type in self.all_types:
                output += ", %s" % self.time_value_map[series_type][time]

            output += "\n"

        return output

    def fill_time_series(self):
        """
        Make sure all timestamps between minimum and maximum time are filled
        """

        for series_type in self.all_types:
            self.time_value_map[series_type] = collections.OrderedDict(sorted(self.time_value_map[series_type].iteritems()))
            self.time_min = min(self.time_min, min(k for k, v in self.time_value_map[series_type].iteritems() if v != 0))
            self.time_max = max(self.time_max, max(k for k, v in self.time_value_map[series_type].iteritems() if v != 0))

        for series_type in self.all_types:
            for time in perdelta(self.time_min, self.time_max, timedelta(minutes=self.minute_res)):
                if time not in self.time_value_map[series_type]:
                    self.time_value_map[series_type][time] = 0.0

    def stream_handler(self, series_type, stream, min_val=0, max_val=1000):

        prev_val = None

        #Go through all values in stream
        for row in stream:

            #Format to date time object and floor time to closest minute_res
            dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            dt = datetime(dt.year, dt.month, dt.day, dt.hour, self.minute_res*(dt.minute // self.minute_res))

            #Only process values that are not None
            if row[1] != None:

                #If first iteration
                if prev_val == None:
                    prev_val = float(row[1])
                    continue

                val = float(row[1]) - prev_val
                if not(val>min_val and val<max_val):
                    continue
                prev_val = float(row[1])
                self.time_value_map[series_type][dt] += val
            else:
                self.time_value_map[series_type][dt] += 0

