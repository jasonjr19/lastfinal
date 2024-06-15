import mysql.connector
from datetime import datetime
import random

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='travel_buddy'
)
# --------------------------------------------------------------------------------------------------------------------------------------------------
# Price split for ticket booking 
def percentage_calculator(budget):
    print(budget)
    # bud = int(budget)
    x = (budget/100)*50
    x2 = (x/100)*50
    # print(x2)
    return x2
# --------------------------------------------------------------------------------------------------------------------------------------------------
# transportation which includes flights,train,bus
def get_flights(source, destination):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `flights` WHERE `Depart_Airport`=%s AND arrive_Airport=%s ORDER BY RAND() LIMIT 1;", (source, destination))
    flights = cursor.fetchall()
    cursor.close()
    return flights

def get_train(source, destination):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM train WHERE source=%s AND destination=%s ORDER BY RAND() LIMIT 1", (source, destination))
    trains = cursor.fetchall()
    cursor.close()
    return trains

def get_bus(source, destination):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE source=%s AND destination=%s ORDER BY RAND() LIMIT 1", (source, destination))
    buses = cursor.fetchall()
    cursor.close()
    return buses


# --------------------------------------------------------------------------------------------------------------------------------------------------
# here we get the details of hotel room avaliable
def get_hotel(loc_id,percentage,days):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `hotels` WHERE price <= %s ORDER BY RAND() LIMIT 1;", (percentage*days,))
    #SELECT * FROM hotel WHERE location=%s AND price <= %s;
    hotels = cursor.fetchall()
    cursor.close()
    return hotels

# --------------------------------------------------------------------------------------------------------------------------------------------------
# here we get the details of car rental available  
def get_car_rental(dest,percentage,days):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM car_rental WHERE pickup_location= %s AND price_per_day <= %s ORDER BY RAND() LIMIT 1;", (dest,percentage*days))
    cars = cursor.fetchall()
    cursor.close()
    return cars

def get_userpro(age_range,travel_type,trip_type,days,budget):
    print(age_range)
    print(travel_type)
    print(trip_type)
    print(days)
    print(budget)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `userdata1` WHERE `age_range`=%s AND `travel_type`= %s AND `trip_type` = %s AND `days`=%s AND budget = %s ORDER BY RAND() LIMIT 1;", (age_range,travel_type,trip_type,days,budget))
    activity = cursor.fetchall()
    cursor.close()
    return activity

#if that data is not present inthe above function than the below function will be used for backup
def get_userpro_not(age_range,travel_type,trip_type):
    print(age_range)
    print('going inside not user',travel_type)
    print(trip_type)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `userdata1` WHERE `age_range`=%s AND `travel_type`= %s AND `trip_type` = %s ORDER BY RAND() LIMIT 1;", (age_range,travel_type,trip_type))
    activity = cursor.fetchall()
    print(activity)
    cursor.close()
    return activity
# --------------------------------------------------------------------------------------------------------------------------------------------------
# finds which transportation is best for the user based on his/her budget
def transportation_avaliable(source, destination,percentage,budget,no_of_travlers):
    flight_avaliable = get_flights(source, destination)

    # first check for flight than train and last bus
    for flight in flight_avaliable:
        if flight[8]*no_of_travlers <= percentage:
            print("Avaliable Flight: ")
            print(f"Flight Number: {flight[1]}, Source: {flight[3]}, Destination: {flight[5]}, Departure Time: {flight[6]}, Arrival Time: {flight[7]}, Price: {flight[8]}")
            budget =(flight[8]*no_of_travlers)
            # print(budget)
            return budget,flight
        else:
            train_avaliable = get_train(source, destination)
            for train in train_avaliable:
                if train[6]*no_of_travlers<=percentage:
                    print("Avaliable Train: ")
                    print(f"Train Number: {train[1]}, Source: {train[2]}, Destination: {train[3]}, Departure Time: {train[4]}, Arrival Time: {train[5]}, Price: {train[6]}")
                    budget = (train[6]*no_of_travlers)
                    # print(budget) 
                    return budget,train
                else:
                    bus_avaliable = get_bus(source, destination)
                    for bus in bus_avaliable:
                        if bus[6]*no_of_travlers<=percentage:
                            print("Avaliable Bus: ")
                            print(f"Bus Number: {bus[1]}, Source: {bus[2]}, Destination: {bus[3]}, Departure Time: {bus[4]}, Arrival Time: {bus[5]}, Price: {bus[6]}")
                            budget = (bus[6]*no_of_travlers)
                            # print(budget)
                            return budget,bus 
                        else:
                            print("Sorry, Your budget is too low. Please Increase your budget")

def hotel_available(loc_id,percentage,days):
    percentage=percentage/days
    hotel = get_hotel(loc_id,percentage,days)
    for room_avaliable in hotel:
        if room_avaliable[4] >= 1:
            print("Avaliable Room: ")
            print(f"Train Number: {room_avaliable[1]}, Source: {room_avaliable[2]}, Destination: {room_avaliable[3]}, Departure Time: {room_avaliable[4]}, Arrival Time: {room_avaliable[5]}")
            # budget = percentage*days
            budget = room_avaliable[5]*days
            return budget,room_avaliable
        
def car_rental_available(dest,budget,days):
    car = get_car_rental(dest,budget,days)
    for car_available in car:
        print("Avaliable Room: ")
        print(f"Train Number: {car_available[1]}, Source: {car_available[2]}, Destination: {car_available[3]}, Departure Time: {car_available[4]}, Arrival Time: {car_available[5]}")
        price =  car_available[6]*days
        if price <= budget:
            return price,car_available
        else:
            return print("car not available")

def calculate_days(start_date_str,end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    difference = (end_date - start_date).days + 1

    print("Number of days between the two dates:", difference)
    return difference

def per_day_expense(trip_type,no_of_travlers,days,budget):
    if trip_type == "chilled":
        chilled_trip = 1500 # chilled person per day expense --------------------------------------------------------
        per_day = chilled_trip*no_of_travlers*days
    elif trip_type == "touristy":
        touristy_trip = 1500 # touristy person per day expense ------------------------------------------------------
        per_day = touristy_trip*no_of_travlers*days
    elif trip_type == "packed":
        packed_trip = 1500 # packed person per day expense ----------------------------------------------------------
        per_day = packed_trip*no_of_travlers*days
    else:
        print("Trip Type (Chilled, Touristy, Packed) Not Selected")

    if budget >= per_day:
        return per_day
    else:
        return f"Please Increase Your Budget"

def gptPrompt(start_date,end_date,travel_type,nots,trip_type,budget):
    prompt = "I am travellng from mumbai to goa on {start_date} till {end_date}. it is a {travel_type} trip of {nots} people. It is a {trip_type} package. Can you create a detailed itinerary based on the days I'm in Goa? My budget is Rs: {budget}. please dont include flight and hotel expenses"
    return prompt 

def get_user_data(age_range,travel_type,trip_type,days,budget):
    act = get_userpro(age_range,travel_type,trip_type,days,budget)
    if not act:
        act = get_userpro_not(age_range,travel_type,trip_type)
    print(act)
    return act

def activities_data():
    rand = random.randint(1,12)
    # get_act = getting_activities(rand,activities)
    return rand

def int_budget(budget):
    print(budget)
    if  budget == 'Less than 10000':
        bud = 10000
        return float(bud)
    elif budget == '10000 - 20000':
        bud = 20000
        return float(bud)
    elif budget == '20000 - 40000':
        bud = 40000
        return float(bud)
    elif budget == '40000 - 60000':
        bud = 60000
        return float(bud)
    elif budget == '60000 - 80000':
        bud = 80000
        return float(bud)
    elif budget == '80000 - 100000':
        bud = 100000
        return float(bud)
    elif budget == 'More than ₹100,000':
        bud = 100000000
        return float(bud)
    
def extract_act(input_string):
    act_list = [act.strip() for act in input_string.split(',')]
    return act_list

def extract_time(arrive):
    
    time_str = arrive
    # time_str = str(time_delta)
    hours, minutes, seconds = str(time_str).split(":")
    print(hours,minutes,seconds)
    return hours,minutes,seconds

def saving_to_database():
    return 
