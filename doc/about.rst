===============
About SQLEnergy
===============

SQLEnergy is a Python wrapper for querying SQL databases that record energy
usage.

The Python application allows for control over which tables to select, their
formatting, thresholding values, and what type of energy source the table represents.
With this information a TimeSeries object is created, effectively a matrix where
the rows represent the time axis, and the columns represent the various
net energy consumptions for each unique source type.
