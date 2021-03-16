# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:28:31 2019

@author: Omar
"""
#
#class CsvFileReader:
#    
#    def __init__(self, filePath):
#        
#        self.filePath = filePath
#        
#        def read_File(self):
#            
            
#import csv
#
#with open('D:/05_Financials/Omar_Private/2019_09_Umsatz.CSV', mode='r') as csv_file:
#    csv_reader = csv.DictReader(csv_file, delimiter=';')
#    line_count = 0
#    for row in csv_reader:
#        if line_count == 0:
#            #print(f'Column names are {", ".join(row)}')
#            line_count += 1
#                
#        print(f'\t{row["Beguenstigter/Zahlungspflichtiger"]} --> {row["Betrag"]}. \n {row["Verwendungszweck"]}')
#        line_count += 1
#    print(f'Processed {line_count} lines.')

import pandas
df = pandas.read_csv('D:/05_Financials/Omar_Private/2019_09_Umsatz.CSV', delimiter=';', encoding='latin-1', decimal=',')  
print(df)