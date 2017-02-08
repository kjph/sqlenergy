import collections
from datetime import datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

class RenewableTimeSeries():

    def __init__(self, minute_res):
        self.time_value_map = collections.defaultdict(float)
        self.minute_res = minute_res

    def __str__(self):

        self.fill_time_series()

        output = "Timestamp, Renewable-Value\n"

        #ordered_dict = collections.OrderedDict()
        for timestamp, value in sorted(self.time_value_map.iteritems()):
            output += "%s, %s\n" % (timestamp, value)

        return output

    def fill_time_series(self):
        """
        Make sure all timestamps between minimum and maximum time are filled
        """

        self.time_value_map = collections.OrderedDict(sorted(self.time_value_map.iteritems()))
        self.time_min = min(k for k, v in self.time_value_map.iteritems() if v != 0)
        self.time_max = max(k for k, v in self.time_value_map.iteritems() if v != 0)

        for time in perdelta(self.time_min, self.time_max, timedelta(minutes=self.minute_res)):
            if time not in self.time_value_map:
                self.time_value_map[time] = 0.0

    def stream_handler(self, stream, min_val=0, max_val=1000):

        prev_val = None
        for row in stream:

            dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            dt = datetime(dt.year, dt.month, dt.day, dt.hour, self.minute_res*(dt.minute // self.minute_res))

            if row[1]:

                if prev_val == None:
                    prev_val = float(row[1])
                    continue

                val = float(row[1]) - prev_val
                if not(val>min_val and val<max_val):
                    continue
                prev_val = float(row[1])
                self.time_value_map[dt] += val
            else:
                self.time_value_map[dt] += 0

