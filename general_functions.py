import datetime
import json

# Converts time from UTC format into a interger of minutes starting from 0
def converttime(time1):

    months = [31,28,31,30,31,30,31,31,30,31,30,31]                                           # How many days are in each month
    
    total_days = 0
    
    for month in months[:(int(time1[5:7])-1)]:
        
        total_days = month + total_days


    converted_time = int(time1[:4])*365*24*60 + total_days*24*60 + int(time1[8:10])*24*60   # Converting the time into total minutes
    
    converted_time = converted_time + int(time1[11:13])*60  + int(time1[14:16])             #

    return converted_time


# Loads data from a json file and returns a dictionary with the data
def loaddata(load_file):

    with open(load_file) as f_obj:  

        data = json.load(f_obj)
        
    return data


# Saving data to a Json file
def save_data(filename, data):  
        
        with open(filename, 'w') as f:

           json.dump(data, f)
        
