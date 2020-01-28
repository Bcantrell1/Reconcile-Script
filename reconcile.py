import pandas as pd
import re
import csv

#Setting csv files into variables for useability. 
masterFile = 'MasterReport.csv'
mosaicFile = 'MosaicReservations.csv'
sitelinkCurrentFile = 'SitelinkCurrentTenants.csv'
sitelinkMoveFile = 'SitelinkMoveInMoveOut.csv'
marchexPhoneCallData = 'MarchexPhoneCallData.csv'

#CSV data frames for use of manipulation.
mosaicDf = pd.read_csv(mosaicFile)
sitelinkCurDf = pd.read_csv(sitelinkCurrentFile)
sitelinkMoveDf = pd.read_csv(sitelinkMoveFile)
marchexDf = pd.read_csv(marchexPhoneCallData)

#column variables
mosaicPhone = mosaicDf['tenant_phone'].tolist()
sitelinkPhone = sitelinkCurDf['Phone'].tolist()
marchexPhone = marchexDf['caller_number'].tolist()
mosaicEmails = mosaicDf['tenant_email'].tolist()
sitelinkMoveEmails = sitelinkMoveDf['sEmail'].tolist()
 
#Prints out number of rows in each csv
mosaicCount = len(mosaicDf.values) 
sitelinkCount = len(sitelinkCurDf.values) 
marchexCount = len(marchexDf.values)

#convert sitelink CSV list to strings due to having decimal places makes the type() a float
sitelinkStrings = [str(i) for i in sitelinkPhone]

#cleaning lists of all special characters to be compared for matches
mosaicClean = [re.sub(r'[^0-9]+', '', i) for i in mosaicPhone]
sitelinkClean = [re.sub(r'[^0-9]+', '', i) for i in sitelinkStrings]
marchexClean = [re.sub(r'[^0-9]+', '', i) for i in marchexPhone]

#match logic for phone numbers (outputs list of phone numbers that match between variables used).
matchesMosaicSitelink = [d for d in sitelinkClean if d in mosaicClean]
matchesMosaicMarchex = [d for d in marchexClean if d in mosaicClean]

#match logic for Emails (outputs list of phone numbers that match between variables used).
emailMatchSiteMosaic = [d for d in sitelinkMoveEmails if d in mosaicEmails]

#Outputs number of matches between mosaic reservations and sitelink current tenants  
matchSitelinkCount = len(matchesMosaicSitelink)
matchMarchexCount = len(matchesMosaicMarchex)
matchSitelinkMoveMosaicCount = len(emailMatchSiteMosaic)

#Percentage change logic
def percentage_change(current, previous):
    if previous != 0 :
        return float(current / previous)*100
    else:
        return "undefined"

#finding only move ins in sitelink move in move out file.
move_in_sitelink = sitelinkMoveDf.loc[sitelinkMoveDf['MoveIn'].isin(['1'])]

#Finding only emails within the sitelinkMoveInMoveOut.csv file and putting it into list: "moveins"
moveins = []
def sitelink_movein():  
    for row, row in move_in_sitelink.iterrows():
        moveins.append(row['sEmail'])

#Run function to gather emails.        
sitelink_movein()

#Finding all matching emails from MosaicReservations.csv to SitelinkMoveInMoveOut.csv 
actual_moveins = [d for d in moveins if d in mosaicEmails]

#Pulling only emails that match 
site_move_matches = sitelinkMoveDf.loc[sitelinkMoveDf['sEmail'].isin(actual_moveins)]

#grabbing only rows that are flagged as move ins not move outs / transfers.
sitelink_movein_only = site_move_matches.loc[site_move_matches['MoveIn'].isin(['1'])]

#List of all actual movins in sitelinkmovein file also in mosaic reservations
mosaic_sitelink_move_in  = sitelink_movein_only.values.tolist()

#Counting of sitelink moveins that are also in mosaic reservations.
number_of_MSMI = len(sitelink_movein_only)

#Data points found to be actual move ins from reservations
data_points = [line for line in mosaic_sitelink_move_in]


with open(masterFile, 'w', newline='', errors='ignore') as f:
    w = csv.writer(f)
    w.writerow(['A Alpha Mini Storage'])
    w.writerow(['Reservations', str(mosaicCount)])
    w.writerow(['Sitelink Leases', str(sitelinkCount)])
    w.writerow(['Reservations to Leases', str(matchSitelinkCount)])
    w.writerow(['Reservation to Lease Conv Rate', str(percentage_change(matchSitelinkCount, mosaicCount)) + '%'])
    w.writerow(['Marchex Phone Calls', str(marchexCount)])
    w.writerow(['Reservations from Phone Calls', str(matchMarchexCount)])
    w.writerow(['Reservation to Phone Call Conv Rate', str(percentage_change(matchMarchexCount, mosaicCount)) + '%'])
    w.writerow(['Reservation to Sitelink Move Ins', str(number_of_MSMI)])
    w.writerow(['Reservation to Site Link Move In Conv Rate', str(percentage_change(number_of_MSMI, mosaicCount)) + '%'])
    w.writerow([])
    w.writerow([])
    w.writerow(["Algortihm data points (Sitelink Move Ins in Mosaic Reservations)"])
    w.writerows(data_points)
    

#printing to console output for testing.
# print('Number of Mosaic Reservations this month: ' + str(mosaicCount))
# print('Number of sitelink leases: ' + str(sitelinkCount))
# print('Number of reservations that lead to a lease conversion: ' + str(matchSitelinkCount))
# print('The reservation to lease conversion rates is: ' + str(percentage_change(matchSitelinkCount, mosaicCount)) + '%')
# print('Number of marchex phone calls for this month: ' + str(marchexCount))
# print('Number of reservations that were made from phone calls: ' + str(matchMarchexCount))
# print('The reservation from phone call conversion rates is: ' + str(percentage_change(matchMarchexCount, mosaicCount)) + '%')
# print(mosaic_sitelink_move_in)