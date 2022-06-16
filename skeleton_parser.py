
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def addQuotations(string):
    string = string.replace('"', '""')
    hasLetter = any(c.isalpha() for c in string)
    if (hasLetter):
        string = '"' + string + '"'
    return string

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, duplicateUserID):
    # Step 1 - open the dat file. If it does not exist, create.
    t1 = open("Item.dat", "a+")
    t2 = open("Bid.dat", "a+")
    t3 = open("User.dat", "a+")
    t4 = open("Category.dat", "a+")

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design

            Tables:
            Item(PK: ItemID, FK: SellerID, Name, Currently, Buy_Price, First_Bid, Number_Of_Bids, Started, Ends, Description)
            Bid(FK: ItemID, FK: BuyerID, FK: SellerID, Amount, Time)
            User(PK: UserID, Rating, Location, Country)
            Category(FK: ItemID, CategoryName)

            """
            # Step 2 - Parse the data and input in files

            # Item table:
            # handle NULL cases
            # plan to handle duplicates with uniq

            # Item info
            t1.write(item["ItemID"] + columnSeparator)
            t1.write(addQuotations(item["Seller"]["UserID"]) + columnSeparator)
            t1.write(addQuotations(item["Name"]) + columnSeparator)
            t1.write(transformDollar(item["Currently"]) + columnSeparator)

            if "Buy_Price" in item:
                t1.write(transformDollar(item["Buy_Price"]) + columnSeparator)
            else:
                t1.write("NULL" + columnSeparator)

            t1.write(transformDollar(item["First_Bid"]) + columnSeparator)
            t1.write(item["Number_of_Bids"] + columnSeparator)
            t1.write(transformDttm(item["Started"]) + columnSeparator)
            t1.write(transformDttm(item["Ends"]) + columnSeparator)

            if item["Description"] != None:
                t1.write(addQuotations(item["Description"]) + "\n")
            else:
                t1.write("NULL" + "\n")

            # Bid table:
            # no need to handle NULL cases
            # plan to handle duplicates with uniq

            # Bid info
            num = int(item["Number_of_Bids"])
            for i in range(num):
                t2.write(addQuotations(item["ItemID"]) + columnSeparator)
                t2.write(addQuotations(item["Bids"][i]["Bid"]["Bidder"]["UserID"]) + columnSeparator)
                t2.write(addQuotations(item["Seller"]["UserID"]) + columnSeparator)
                t2.write(transformDollar(item["Bids"][i]["Bid"]["Amount"]) + columnSeparator)
                t2.write(transformDttm(item["Bids"][i]["Bid"]["Time"]) + "\n")


            # User table:
            # no need to handle NULL cases
            # plan to handle duplicates with uniq

            # Seller info
            sellerID = addQuotations(item["Seller"]["UserID"])
            if(sellerID in duplicateUserID):
                pass
            else:
                duplicateUserID.add(sellerID)
                t3.write(sellerID + columnSeparator)
                t3.write(item["Seller"]["Rating"] + columnSeparator)
                t3.write(addQuotations(item["Location"]) + columnSeparator)
                t3.write(addQuotations(item["Country"]) + "\n")

            # Bidder info
            num = int(item["Number_of_Bids"])
            for i in range(num):
                buyerID = addQuotations(item["Bids"][i]["Bid"]["Bidder"]["UserID"])
                if(buyerID in duplicateUserID):
                    pass
                else:
                    duplicateUserID.add(buyerID)
                    t3.write(buyerID + columnSeparator)
                    t3.write(item["Bids"][i]["Bid"]["Bidder"]["Rating"] + columnSeparator)

                    if "Location" in item["Bids"][i]["Bid"]["Bidder"]:
                        t3.write(addQuotations(item["Bids"][i]["Bid"]["Bidder"]["Location"]) + columnSeparator)
                    else:
                        t3.write("NULL" + columnSeparator)

                    if "Country" in item["Bids"][i]["Bid"]["Bidder"]:
                        t3.write(addQuotations(item["Bids"][i]["Bid"]["Bidder"]["Country"]) + "\n")
                    else:
                        t3.write("NULL" + "\n")
                

            # Category table:
            # no need to handle NULL cases
            # plan to handle duplicates with uniq

            # Category info
            duplicateCategory = set()
            num = int(len(item["Category"]))
            for i in range(num):
                if(item["Category"][i] in duplicateCategory):
                    pass
                else:
                    duplicateCategory.add(item["Category"][i])
                    t4.write(item["ItemID"] + columnSeparator)
                    t4.write(addQuotations(item["Category"][i]) + "\n")


        
            pass

    # Step 3 - Close the files.
    t1.close()
    t2.close()
    t3.close()
    t4.close()
    return duplicateUserID

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    duplicateUserID = set()
    for f in argv[1:]:
        if isJson(f):
            if f[16] == "*":
                for i in range(0, 40):
                    duplicateUserID = parseJson(f[:16] + str(i) + ".json", duplicateUserID)
            else:
                duplicateUserID = parseJson(f, duplicateUserID)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
