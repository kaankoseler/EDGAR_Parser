# -*- coding: utf-8 -*-
"""
Created on Thur Apr 12 21:17:18 2018

@author: Kaan Koseler
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sys
import pandas as pd
import re

def main():
    # process command line args
    args = sys.argv[1:]
    if len(args) != 1:
        print('Invalid Input. Enter a single ticker or CIK.')
        sys.exit()
    
    # search EDGAR based on user input
    user_input = args[0]
    print('Parsing 13F for ' + user_input + '...')
    searchPage_soup = searchForFund(user_input)  
    
    # grab the .txt soup and determine its headers
    txt_soup = getTextSoup(searchPage_soup)
    headers = getHeaders(txt_soup)
    
    # get the rows and write as tab-delimited .txt with Pandas
    rows = getRows(txt_soup, headers)
    df = pd.DataFrame(data=rows, columns=headers)
    file_name = user_input + '_13F.txt'
    df.to_csv(user_input + '_13F.txt', sep='\t', index=False)            
    
    print('Successfully parsed! File is named ' + file_name + ' and is '
          'located in the current directory.')

def getHeaders(txt):
    """
    Get the longest list of headers from the text file
    
    :param object txt: Soup of the .txt 13F report
    :return: the list of headers
    :rtype: list
    """
    master_headers = []
    table_array = txt.find_all('infoTable')
    
    # error check that report has information
    if (table_array is None):
        print('This report is empty! Something is wrong.')
        sys.exit()
    
    # iterate through the report to determine maximum number of headers    
    for table in table_array:
        headers = []
        for line in table.findChildren():
            if (line.name is not None and line.string is not None):
                headers.append(line.name)
        if (len(headers) > len(master_headers)):
            master_headers = headers
            
    return master_headers

def getPage(url):
    """
    Get the web page given the url
    
    :param string url: the url 
    :return: the page
    :rtype: object
    """    
    url_client = urlopen(url)
    page = url_client.read()
    url_client.close()
    
    return page

def getRows(txt_soup, headers):
    """
    Get all the rows from the 13F text
    
    :param object txt_soup: Soup of the .txt 13F report
    :param list headers: Longest header list
    :return: A 2D list of each row, where each row is itself a list of values
    :rtype: list
    """
    rows_list = []
    
    # iterate through the text file, building a list for each row
    for row in txt_soup.find_all('infoTable'):
        temp_list = []
        for column in headers:
            if (row.find(column) is None):
                # if there's no value for this column, label it 'N/A'
                temp_list.append('N/A')
            else:
                # otherwise just use the value in the column
                temp_list.append(row.find(column).string)
                
        rows_list.append(temp_list)
        
    return rows_list

def getTextSoup(search_soup):
    """
    Get soup of the 13F text file
    
    :param object search_soup: The soup of the search page 
    :return: the soup of the 13F text file
    :rtype: object
    """
    # get the URL for the most recent 13F document page
    first_13F_url = 'http://www.sec.gov' + search_soup.find('a', {'id' : 
                                         'documentsbutton'})['href']
    filingsPage_soup = soup(getPage(first_13F_url), 'html.parser')
    
    # get the .txt file url
    txt_13F_url = ('http://www.sec.gov' + filingsPage_soup.find
               ('a', text=re.compile(r".*\.txt$"))['href'])
    
    # get the .txt file xml soup
    txt_soup = soup(getPage(txt_13F_url), 'xml')
    
    return txt_soup

def searchForFund(user_input):
    """
    Search EDGAR to see if fund exists/has 13F docs on file
    
    :param str user_input: The CIK or ticker entered by user
    :return: the search page parsed by BeautifulSoup
    :rtype: object
    """
    searchPage_url = ('http://www.sec.gov/cgi-bin/browse-edgar?action='
                      'getcompany&CIK=' + user_input + 
                      '&type=13F&dateb=&owner=exclude&count=40')
    
    page_soup = soup(getPage(searchPage_url), 'html.parser')
    
    # check to make sure user hasn't entered invalid ticker/CIK
    if (page_soup.findAll(string='No matching CIK.')
        or page_soup.findAll(string='No matching Ticker Symbol.')):
        print('Invalid Input. No such ticker or CIK found on EDGAR.')
        sys.exit()
    
    # check to make sure this company has at least one 13F on file    
    if (not page_soup.find('a', {'id': 'documentsbutton'})):
        print('This company has no 13F documents on EDGAR!')
        sys.exit()
    
    return page_soup
             
if __name__ == "__main__":
    main()    