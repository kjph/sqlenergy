import collections
from datetime import datetime, timedelta

class RenewableTimeSeries():

    def __init__(self):
        self.time_value_map = collections.defaultdict(float)

    def __str__(self):

        output = "Timestamp, Renewable-Value\n"

        for timestamp, value in self.time_value_map.iteritems():
            output += "%s, %s\n" % (timestamp, value)

        return output


    def stream_handler(self, stream, minute_res=15):

        for row in stream:
            dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            dt = datetime(dt.year, dt.month, dt.day, dt.hour, minute_res*(dt.minute // minute_res))
            if row[1]:
                self.time_value_map[dt] += float(row[1])
