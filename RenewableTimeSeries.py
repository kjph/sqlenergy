import collections
from datetime import datetime, timedelta

class RenewableTimeSeries():

    def __init__(self):
        self.time_value_map = collections.defaultdict(float)

    def __str__(self):

        output = "Timestamp, Renewable-Value\n"

        #ordered_dict = collections.OrderedDict()
        for timestamp, value in sorted(self.time_value_map.iteritems()):
            output += "%s, %s\n" % (timestamp, value)

        return output


    def stream_handler(self, stream, minute_res=15, min_val=0, max_val=1000):

        prev_val = None
        for row in stream:

            if row[1]:

                if prev_val == None:
                    prev_val = float(row[1])
                    continue

                val = float(row[1]) - prev_val
                if not(val>min_val and val<max_val):
                    continue
                prev_val = float(row[1])

                dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                dt = datetime(dt.year, dt.month, dt.day, dt.hour, minute_res*(dt.minute // minute_res))

                self.time_value_map[dt] += val


