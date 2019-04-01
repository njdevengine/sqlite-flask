%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

from sqlalchemy import create_engine, inspect, func
inspector = inspect(engine)
inspector.get_table_names()

# Get a list of column names and types
print("Measurement table \n")
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])

print("\nStation table \n")    
# Get a list of column names and types
columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])
    
# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Calculate the date 1 year ago from the last data point in the database
# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame and set the index to the date column
# Sort the dataframe by date
# Use Pandas Plotting with Matplotlib to plot the data
cursor = engine.execute('select * from Measurement order by date desc limit 1')
for i in cursor:
    print(i)
    
x = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
x

df = pd.DataFrame(x)
df.columns = ["Date", "Precipitation"]
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index("Date")
df = df.dropna()
df.sort_values(by="Date")

import matplotlib.dates as mdates
import matplotlib.patches as mpatches

x = df.index.values
y = df['Precipitation']

fig, chart = plt.subplots(figsize=(15,7))
chart.bar(x, y, width=2)
chart.xaxis_date()
chart.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

legend = mpatches.Patch(color='blue', label='Precipitation')
plt.legend(handles=[legend])
plt.show()

# Use Pandas to calculate the summary statistics for the precipitation data
df.describe()
