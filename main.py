import os
from market_data import *
from general_functions import *


if __name__ == "__main__":

    savefile = "raw_data.json"

    print("Program started")

    timeleft = 60   												       # Time between total iterations (seconds)

    marketdata = GetMarkets(savefile)        					           # Creating an object to represent the all the raw market data

    while True:
        
        marketinfo = marketdata.get_market_data()      					   # Pulling the data from bittrex

        save_data(savefile, marketinfo)                                    # Saving data to json file

        marketdata.totaliterations = marketdata.totaliterations + 1		   # Counting the number of iterations completed
		
        print("Data collection: ", marketdata.totaliterations, "\n")
        
        for key,value in marketinfo.items():

            if key == "BTC":

       	     for key2,value2 in value.items():

       		     if key2 == "last_update":

       			     last_update = converttime(value2[-1])
       			     

        while timeleft != 0:

            current_time = converttime(str(datetime.datetime.now()))      # Converting time to total minutes

            if (current_time - last_update >=2):						  # Checks to see if it has not been updated in the last two minutes, if so updates now (backup)
                
                break

            else:
                
                time.sleep(10)

         
        	


