import urllib.request
import json
import time
import datetime
import os
import socket
import errno


# This class is used to pull market orders (either just BTC or any altcoins) and saves the orders in a json file.
class GetMarkets:


    def __init__(self,raw_dat_file):
        
        self.filename = raw_dat_file                                # File used to save the market data
  
        with open(self.filename) as f_obj:                          # Open file to save raw data in
            
            self.marketinfo = json.load(f_obj)

        self.totaliterations = 0;                                   # For printing the total number of times data has been collected  
        
        self.markets = ["BTC"]                                      # Can be adjusted to pull multiple market data



    def get_market_data(self):

        marketcounter = 0                                           # Counter for which market is being looked at
        
        if self.marketinfo == {}:

            for market in self.markets:

                self.marketinfo[market] = {'last_update': [],       # Creating blank format for saved data
                                            'data': []}


        for selected_market in self.markets:
            
            first_item = 0

            marketcounter = marketcounter + 1

            while True:

                try:
                    load_dat = urllib.request.urlopen('https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=USD-' + selected_market)     # Downloads data from Bittrex
                    
                    break

                except urllib.error.URLError:                       # If there is no connection, wait 10 seconds then try to pull data again
                   
                    print("NO INTERNET!!")

                    time.sleep(10)


            self.market_input = json.load(load_dat)                 # Loads the data from Bittrex in a dictionary format         

            for section, listoforders in self.market_input.items(): # listoforders is the list of orders

                end = False                                         # Set to true when all data is successfully added to the dictionary

                printtime = False
                
                orderplace = 0                                      # Used to know where to insert the orders into the already saved data, so they are saved in chronilogical order
                
                if section == 'result':
                    
                    if listoforders == []:
                       
                        break

                    for order in listoforders:                      # Looping through each order list

                        if end == True:
                          
                            break

                        for valuetype, value in order.items():      # Getting the values for each trade from the bittrex pulled data

                            if valuetype == 'Id':
                                id = value
                            if valuetype == 'TimeStamp':
                                timestamp = value
                            if valuetype == 'Quantity':
                                quantity = value
                            if valuetype == 'Price':
                                price = value
                            if valuetype == 'Total':
                                total = value
                            if valuetype == 'OrderType':
                                ordertype = value

                        info = [id,timestamp,quantity,price,total,ordertype]        # Formatting to the data
                        
                        
                        for marketname, orderlist in self.marketinfo.items():       # Puts the data collected above into a new/ appends the old dictionary 

                            if marketname == selected_market:

                                for section2, saveddata in orderlist.items():
                                    
                                    if section2 == "last_update":

                                        if printtime == False:
                                            
                                            saveddata.append(str(datetime.datetime.now()))

                                            orderlist[section2] = saveddata

                                            printtime = True
                                        

                                    if section2 == 'data':

                                        if first_item == 0:     

                                            if saveddata == []:

                                                first_item = 0

                                            else:

                                                first_item = saveddata[0][0]
                                                
                                        if first_item == info[0]:                   # Ends the loop when it reaches the last recorded id from the previous collection
                                            
                                            end = True

                                            break
                                        
                                        else:                                       # Insert the new order into the previously saved orders list in chronilogical order

                                            saveddata.insert(orderplace,info)                                              
                                                                                                
                                            orderplace = orderplace + 1
                                        
                                                                                                        
                    break

                               
        print("Data Collection Complete!")
        
        return self.marketinfo
     
