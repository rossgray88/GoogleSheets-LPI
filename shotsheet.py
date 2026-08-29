from logging import warning
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import datetime 

class shotsheet: 

    '''
    ------------------------------------------
    Title: shotsheet
    Creation Date: 20/03/2021
    Author: R. Gray
    Version: v1 (20/03/2021)

    %%%%% CODE DESCRIPTION [BEGINS]

    This class reads in and parses a shotsheet either from google sheets or as an excel 
    (although as of 28/03/21 the excel functionality hasn't been added ). The idea here is to read in the shotsheet and return 
    it in a pandas dataframe so that it can be used for metadata/plotting along side the experiment data

    %%%%% CODE DESCRIPTION [ENDS]
    ------------------------------------------
    '''
    
    
    def __init__(self,filename=None):

        self.filename = filename
         
    
    def googlesheetsloader(self, id, tokenloc, sheetname):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        SAMPLE_RANGE_NAME = sheetname

        
        # Reads in the token given by token loc to authorise access to the spreadsheet
        with open(tokenloc, 'rb') as token:
                    creds = pickle.load(token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=id,range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        
        return values

    def parse_googlesheets(self, values, headerrow = 0, datarow = 2): 
        
        
        # The header row is the top section header on the shot sheet like 'laser information' 
        # these are often set to span across multiple columns. 
        # Here from the values array we grab the usually the first row, but in other cases any header 
        # row defined by the user. 
        headers = values[headerrow]

        # the sub headers are the row headings like 'date', 'filter' and 'comments'. 
        # In order to store these in a dict they have to be unique names but in the shot sheet 
        # Here we grab the next row down from the header row which would typically be these sub headings. 
        sub_headers = values[headerrow+1]


        # Seeting up an array to contain the header strings
        header_string_array = []
        
        # for the header row where the header is 'merged' over multiple columns this appears as an empty
        # header in the form ''. We want to identify the headers that have names and those that dont. 
        non_empty_header = []

        
        # Outside loop: for each header in the array. 
        # Loop (1) If the the header is '' i.e empty then append the last non_empty header to that position
        # Loop (2) If it is the first header position append the header 
        # or if not append the previous entry in the header_string_array i.e the last header that wasn't == ''


        for i,header in enumerate(headers): 
            
            # Loop (1)
            if (header == ''): 
                header_string_array.append(non_empty_header)
            else: 
                non_empty_header = header
            
            # Loop(2)
                
                # Make sure to get the first and last headers
                if (i == 0) or (headers[i] == headers[-1]):
                    header_string_array.append(header)
                
                # Make sure to get a header which only one column long 
                elif headers[i] !='': 
                    header_string_array.append(header)
                
                # Creating new header from the previous non empty (i.e '') header
                else: 
                    header_string_array.append(header_string_array[-1])
                
        #header_string_array = header_string_array[1:]
        #sub_headers = sub_headers[0:-1]

                
        # From that array of headers combine each header with its corresponding sub_header to make 
        # a unique key for the dict. This could be combined with the previous loop so that you 
        # only have to go through the list once but this seems more readible to me 
        
        unique_headers =[]
        for i,sub_header in enumerate(sub_headers): 
            sub_header_string = header_string_array[i]+' ('+sub_header+')'
            unique_headers.append(sub_header_string)
                

        # Creating dict for values using the uniquely generated headers as the key. 
        data = {}
        for i,unique_header in enumerate(unique_headers): 
            
            # Can't append to a none value so changing the value to an empty array []
            data[unique_header] = []
            for j in range(datarow,len(values)): 
                if values[j] == []: 
                    break
                else: 
                    
                    
                    
                    
                    data[unique_header].append(values[j][i])


        df_shotsheet = pd.DataFrame(data)
        
        return df_shotsheet

    def excel_reader(self): 
        pass 

class parseshotsheets: 

    # The intention here is to build up a number of parsing functions for the shot sheet. 
    # It is probably sensible to catch bad data entry at this point. 
    
    def __init__(self):
        pass
    
    
    def get_shotsheet_datetime(self,date,time):
        shotdate = date + ' ' + time

        shotdate_converted = []
        for SD in shotdate:
             
            if (SD == '') or (SD == ' '):
                SD = "01/01/22 00:00"
                raise Warning('Replaced missing date with 01/01/22 00:00 check shotsheet.')
            
            shotdate_converted.append(self.datetimestring(SD))

        return shotdate_converted

    
    
    def datetimestring(self,timestring, fmt='%d/%m/%y %H:%M'): 

        # This function converts a provided date time string from the shot sheet into a standard form and 
        # into a datetime object that can be plotted. 

        datetime_converted = datetime.datetime.strptime(timestring, fmt)

        return datetime_converted

    
    def shotenergy(self,shotenergy): 
        for i,entry in enumerate(shotenergy):
            if entry == 'n/a':
                shotenergy[i] = 0 
                raise Warning('Replaced n/a energy value in shotsheet with 0J')


    def pulseduration(self,pulseduration):
        for i,entry in enumerate(pulseduration): 
            if entry == '':
                pulse_duration[i] = 0

    

    def parse_filter_details(self,filter_details): 
    
        # Split by commas 
        filters = filter_details.split(',')
        
        # Setting up empty dict 
        parsed_filters = {}
        
        # go through each filter in the list and find where there is an '*' 
        # which implies multiples of the same filters store the number 
        # of filters in the value of the key:value pair. 
        # If there isn't a '*' store the value as 1
        
        for filter in filters: 
            if '*' in filter: 
                index = filter.index('*')
                Nfilts = int(filter[0:index])
                parsed_filters[filter[index+1::]] = Nfilts
            else: 
                Nfilts = 1
                parsed_filters[filter] = Nfilts
                
        
        return parsed_filters


