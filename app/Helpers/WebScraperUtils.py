'''
Created on Dec 16, 2015

@author: Derek Dik
'''

def formatString( string ):
    result = ''
    for char in string:
        if char == '\n':
            if result[ -1 ] != '\n':
                result = result + char
        else:
            result = result + char
    return result 

def monthAndYear(month, year):
    if year[-1] == '.':
        print("Correcting year format: Removing period")
        year = year[:-1]
    if len(year) != 4 or not year.isdigit():
        return ""
        print("Correcting year format: Year is not correct.")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May" or month == "June" or month == "July" or month == "August" or month == "September" or month == "October" or month == "November" or month == "December":
        return month + " " + year
    else:
        return year
        print("Correcting year format: No month available")