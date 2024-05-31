from nav_sangna import *
import random
import mysql.connector
from datetime import *

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='travel_buddy'
)

def sql_data(hehe,location):
    cursor = conn.cursor()
    cursor.execute("SELECT name,address,description,location.talukas  FROM {} INNER JOIN location ON location.location_id = {}.location_id WHERE location.location_id=%s ORDER BY RAND() LIMIT 1".format(hehe, hehe) , (location,))
    data_db = cursor.fetchall()
    cursor.close()
    return data_db

def creating_data(sample,days,trip_type,location,arrive):
    length = len(sample)
    # rand = activities_data()
    data_days = []
    final = []
    
    if trip_type == 'Touristy ( 2-3 activities)':
        trip = 3
    elif trip_type == 'Packed ( 3 or more activities)':
        trip = 4
    elif trip_type == 'Chill ( 1-2 activities)':
        trip = 2
    
    print("trip print zata", trip)
    for i in range(days):
        in_data_days = []
        j=0
        while j in range(trip):
        # while j != trip:
            # print(j)
            r = random.randint(0,length-1)
            if sample[r] == 'Sightseeing':
                if sample[r] in in_data_days:
                    j=j-1
                else:
                    in_data_days.append('Sightseeing')
                    # print(j)
            elif sample[r] == 'Beach Activities':
                if sample[r] in in_data_days:
                    j=j-1
                else: 
                    in_data_days.append('Beach Activities')
                    # print(j)
            elif sample[r] == 'Shopping':
                if sample[r] in in_data_days:
                    j=j-1
                else:
                    in_data_days.append('Shopping')
                    # print(j)
            elif sample[r] == 'Hiking/Trekking':
                if "Hiking/Trekking" not in in_data_days and random.random() < 0.3:
                    in_data_days.append('Hiking/Trekking')
                else:
                    j=j-1
                # if sample[r] in in_data_days:
                #     j=j-1
                # else:
                #     in_data_days.append('Hiking')
                    # print(j)
            elif sample[r] == 'Historic':
                if sample[r] in in_data_days:
                    j=j-1
                else:
                    in_data_days.append('Historic')
                    # print(j)
            elif sample[r] == 'Museum':
                if sample[r] in in_data_days:
                    j=j-1
                else:
                    in_data_days.append('Museum')
                    # print(j)
            elif sample[r] == "Nightlife":
                if "Nightlife" not in in_data_days and random.random() < 0.3:
                    in_data_days.append('Nightlife')
                else:
                    j=j-1
            if 'Nightlife'in in_data_days:
                in_data_days.remove('Nightlife')
                in_data_days.append('Nightlife') 
            j=j+1
            # print(j)
        data_days.append(in_data_days)
    print(data_days)
    print("going inside for x loop ")

    #HOW TO FIND THE RANGE OF A 2D LIST..
    #-----------------------------------------------------------
    # max_length = max(len(sublist) for sublist in data_days)
    # min_length = min(len(sublist) for sublist in data_days)
    # list_range = max_length - min_length
    # print("Range of the data_days list:", list_range)
    #-----------------------------------------------------------
    hours,minutes,seconds = extract_time(arrive)
    for x in range(3): #change the number of buffer time(HOURS) if required 
        hours = int(hours)
        hours=hours+1
        print(hours)

    if hours >= 24:
        hours=0

    if trip == 2:
        print("trip C save zata")
        if 00 <= hours <= 8:
            print("sarko aha to")
        elif 8 <= hours <= 15:
            print("lunch son start kor")
            # print(data_days[0][1])
            del data_days[0][:1]
        elif 15 <= hours <= 24:
            print("lunch son start kor")
            # print(data_days[0][2])
            del data_days[0][:2]

    elif trip == 3:
        print("trip T save zata")
            
        if 00 <= hours <= 8:
            print("sarko aha to")
        elif 8 <= hours <= 12:
            print("lunch son start kor")
            # print(data_days[0][1])
            del data_days[0][:1]
        elif 12 <= hours <= 16:
            print("ek activity di teka")
            # print(data_days[0][2])
            del data_days[0][:2]
        elif 16 <= hours <= 24:
            print("direct dinner di teka")
            # print(data_days[0][3])
            del data_days[0][:3]

    elif trip == 4:
        print("trip P save zata")
        if 00 <= hours <= 8:
            print("sarko aha to")
        elif 8 <= hours <= 10:
            print("lunch son start kor")
            # print(data_days[0][1])
            del data_days[0][:1]
        elif 10 <= hours <= 13:
            print("ek activity di teka")
            # print(data_days[0][2])
            del data_days[0][:2]
        elif 13 <= hours <= 17:
            print("direct dinner di teka")
            # print(data_days[0][3])
            del data_days[0][:3]
        elif 17 <= hours <= 24:
            print("direct dinner di teka")
            # print(data_days[0][4])
            del data_days[0][:4]

    for x in range(len(data_days)):
        d = f"Day {x+1}"
        print(d)
        final.append(d)
        for y in data_days[x]:
            print(data_days)
            sub = y
            if 'Sightseeing' in sub:
                hehe = 'Sightseeing'
                print("if sightseeing\n")
                    # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)  
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                # while data in final:
                #     final.pop()
                    
                final.append(data)
                print(data)
            elif 'Beach Activities' in sub:
                hehe = 'Beach_activities'
                print("if Beach_activities\n")
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                final.append(data)
                print(data)
            elif 'Hiking' in sub: #IF ERROR YETA ZALEAR YE Hiking/Trekking ESKON CHANGE KOR --------------------------------------------------
                hehe = 'Hiking'
                print("if Hiking\n")
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                final.append(data)
                print(data)
            elif 'Historic' in sub:
                hehe = 'Historic'
                print("if Historic\n")
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                final.append(data)
                print(data)
            elif 'Museum' in sub:
                hehe = 'Museum'
                print("if Museum\n")
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                final.append(data)
                print(data)
            elif 'Shopping' in sub:
                hehe = 'Shopping'
                print("if Shopping\n")
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)

                final.append(data)
                print(data)
            elif 'Nightlife' in sub:
                print("if Nightlife\n")
                hehe = 'Nightlife'
                # location = 10 #THIS DATA WILL BE UPDATED.. FOR NOW TO CHECK IF THIS IS WORKING FOR NOT I AM USING LOCATION AS 10 
                data = sql_data(hehe,location)
                temp_location=location
                while not data or data in final:
                    if 0 <= temp_location < 12:
                        temp_location = temp_location+1
                        data = sql_data(hehe,temp_location)
                    elif temp_location == 12:
                        while not data or data in final:
                            if temp_location != 0:
                                temp_location = temp_location-1
                                data = sql_data(hehe,temp_location)
                final.append(data)
                print(data)
        location = random.randint(1,12)
        #IN THE ABOVE FOR LOOP WE CAN CHANGE THE ELIF TO IF SO THAT IF CAN PRINT EVERY ELEMENT IN THAT LIST 
    print(final)

    # activities = []
    # for item in final:
    #     if isinstance(item, list):
    #         activities.extend(item)

    # # Extracting specific information
    # for activity in activities:
    #     activity_id, name, location, description, *coordinates, district, region, state = activity
    #     print("Name:", name)
    #     print("Location:", location)
    #     print("Description:", description)
    #     print("District:", district)
    #     print("Region:", region)
    #     print("State:", state)
    #     print()


    # words = final.split()
    # if words == 'days':
    #     print("day yelo re")
    return final
    # return activities