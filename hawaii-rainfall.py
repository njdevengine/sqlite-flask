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

# Design a query to show how many stations are available in this dataset?
cursor = engine.execute('select count(*) from Station')
for i in cursor:
    print(i[0])
    
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
cursor = engine.execute('select count(*),station from Measurement group by station order by count(*) desc')
for i in cursor:
    print(i)

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
cursor = engine.execute("select station,min(tobs) from Measurement where station='USC00519281'")
for i in cursor:
    print("Minimum Temp:")
    print(i)
    print("\n")
cursor = engine.execute("select station,max(tobs) from Measurement where station='USC00519281'")
for i in cursor:
    print("Maximum Temp:")
    print(i)
    print("\n")
cursor = engine.execute("select station,round(avg(tobs), 2) from Measurement where station='USC00519281'")
for i in cursor:
    print("Mean Temp:")
    print(i)
    print("\n")
    
# Choose the station with the highest number of temperature observations.
results = []
cursor = engine.execute('select count(tobs),station from Measurement group by station order by count(*) desc limit 1')
for i in cursor:
    print("Station with most tobs:")
    print(i)
    print("\n")
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
cursor = engine.execute('select * from Measurement where station="USC00519281" and date >"2016-08-18" order by date desc')
for i in cursor:
    results.append(i)

df2 = pd.DataFrame(results)
df2.columns = ["ID","Station","Date","Precipitation","Temp"]
df2["Date"] = pd.to_datetime(df2["Date"])

hist = df2["Temp"].hist(bins=10)
legend = mpatches.Patch(color='blue', label='temp observations')
plt.legend(handles=[legend])
plt.show()

# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
print("MIN, MEAN, MAX")
print(calc_temps('2017-05-19', '2017-05-22'))
data = calc_temps('2017-05-19', '2017-05-22')
y = data[0][1]
error = (data[0][2])-(data[0][0])

fig, ax = plt.subplots()

rects1 = ax.bar([1], y, 1,
                alpha=1, color='orange',
                yerr=error)

ax.set_ylabel('Temp (F)')
ax.set_title('Trip Avg Temp')
ax.set_xticks([0])
plt.show()

# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
cursor = engine.execute("""
select Measurement.station, Measurement.date, Measurement.prcp, Station.name,
Station.latitude, Station.latitude, Station.elevation
from Measurement
inner join Station on Measurement.station = Station.station 
where Measurement.date > "2017-05-19"
and Measurement.date < "2017-05-22"
order by Measurement.prcp desc;
""")
print("Station, Date, Precipitation, Name, Lat, Lon, Elevation")
for i in cursor:
    print(i)
    
# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`
# Set the start and end date of the trip
# Use the start and end date to create a range of dates
# Stip off the year and save a list of %m-%d strings
# Loop through the list of %m-%d strings and calculate the normals for each date
normals = []
start = "05-19"
end = "05-22"
dates = []
dates.append(start)
dates.append(end)
for i in range (20,22):
    dates.append("05-"+str(i))

for i in dates:
    normals.append(daily_normals(i))
dates

# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index

df3 = pd.DataFrame(np.array([normals[0][0], normals[1][0], normals[2][0], normals[3][0]]),
                   columns=['min', 'avg', 'max'])
df3['date']=dates
df3

# Plot the daily normals as an area plot with `stacked=False`
df3.plot(kind='area', stacked=False, alpha=0.5,
        title='Min / Avg / Max')
plt.show()
