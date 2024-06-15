from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime,date
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import uuid
from functools import wraps
from datetime import datetime
from nav_sangna import *
from itinerary_algo import *
import mysql.connector

import base64

app = Flask(__name__)

app.secret_key = 'super_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'travel_buddy'
 
mysql = MySQL(app)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
#Configure session to use filesystem (instead of signed cookies)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PREFERRED_URL_SCHEME"] = 'https'
app.config["DEBUG"] = False
Session(app)

# @app.route('/')
# def index():
#     return render_template('selector.html')
global creating_days


@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM `recommendations` WHERE rec_id LIMIT 3;''')
    recommendations = cursor.fetchall()
    cursor.execute('''SELECT `depart_airport` FROM `flights`;''')
    depart_details=[row[0] for row in cursor.fetchall()]
    print(depart_details)
    customer_exists = session.get('customer_exists')
    if customer_exists:
        print("customer:")
        print(customer_exists)
        return render_template('/Travelbuddycustomer/index.html',user=customer_exists, recommendations = recommendations,depart_details=depart_details)
    else: 
        return render_template('/Travelbuddycustomer/index.html', recommendations = recommendations)

@app.route('/clogin', methods=['GET','POST'])
def clogin():
    username= request.form.get("email")
    print(username)
    customer_exists = session.get('customer_exists')
    if customer_exists in session:
        print("inside login customer exist zata")
        return render_template("/Travelbuddycustomer/home.html", users=customer_exists, recommendations=existing_user1) #CHECK THIS FILE NAME LATERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
    else:
        username= request.form.get("email")
        password= request.form.get("psw")
        print(password)
        print(username)
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM customer WHERE email=%s and pass=%s; ''',[username,password])
        customer_exists=cursor.fetchone()
        cursor.execute('''SELECT * FROM `recommendations` WHERE rec_id LIMIT 3;''')
        recommendations=cursor.fetchall()
        cursor.execute('''SELECT `depart_airport` FROM `flights`;''')
        depart_details=cursor.fetchall()
        if not customer_exists:
            return render_template("error.html",error="Incorrect Email Or Password")
        session['logged_in'] = True
        session['customer_exists'] = customer_exists
        session['recommendations'] = recommendations
        session['depart_details'] = depart_details

        return render_template('/Travelbuddycustomer/index.html', users=customer_exists, recommendations=recommendations,depart_details=depart_details)
        # return redirect(url_for('home'))
    return render_template('/Travelbuddycustomer/login.html')

@app.route('/login')
def login():
    customer_exists = session.get('customer_exists')
    recommendations = session.get('recommendations')
    depart_details = session.get('depart_details')
    if customer_exists:
        return render_template('/Travelbuddycustomer/index.html',user=customer_exists, recommendations = recommendations,depart_details=depart_details)
    else:
        return render_template('/Travelbuddycustomer/login.html')

@app.route('/about')
def about():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/about.html',user=customer_exists)
    else:
        return render_template('/Travelbuddycustomer/about.html')

@app.route('/service')
def service():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/service.html',user=customer_exists)
    else:
        return render_template('/Travelbuddycustomer/service.html')

@app.route('/contact')
def contact():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/contact.html',user=customer_exists)
    else:
        return render_template('/Travelbuddycustomer/contact.html')


@app.route('/hotelbook')
def hotelbook():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/hotelbook.html')
    else:
        return render_template('/Travelbuddycustomer/login.html')


@app.route('/itinerary')
def itinerary():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/booking.html',user=customer_exists)
    else:
        return render_template('/Travelbuddycustomer/login.html')

@app.route('/register')
def register():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        recommendations = session.get('recommendations')
        return render_template('/Travelbuddycustomer/index.html',user=customer_exists, recommendations = recommendations)
    else:
        return render_template('/Travelbuddycustomer/signup.html')

#IDWAL EDITED THIS 
@app.route('/emergency')
def emergency():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/emergency.html')
    else:
        return render_template('/Travelbuddycustomer/login.html')

@app.route('/docstore')
def docstore():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/docstore.html')
    else:
        return render_template('/Travelbuddycustomer/login.html')

@app.route('/packbook')
def packbook():
    customer_exists = session.get('customer_exists')
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM `recommendations`''')
    recommendations=cursor.fetchall()
    return render_template('/Travelbuddycustomer/package_booking.html',user=customer_exists,recommendations=recommendations) 

@app.route('/display')
def display():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/display_itenary.html',user=customer_exists)
    else:
        return render_template('/Travelbuddycustomer/login.html')
    
@app.route('/payment')
def payment():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/payment.html')
    else:
        return render_template('/Travelbuddycustomer/login.html')

@app.route('/car')
def car():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        return render_template('/Travelbuddycustomer/car_rental.html')
    else:
        return render_template('/Travelbuddycustomer/login.html')

# @app.route('/contact')
# def contact():
#     return render_template('/Travelbuddycustomer/contact.html')
#TILL ABOVE IDWAL EDITED

@app.route('/confirming', methods=['POST'])
def confirming():
    fname= request.form.get("firstName")
    lname= request.form.get("lastName")
    gender= request.form.get("gender")
    email= request.form.get("email")
    phone= request.form.get("phone")
    password1=request.form.get("psw")
    password2=request.form.get("confirmPsw")

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM customer WHERE email=%s and pass=%s; ''',[email,password1])
    existing_user=cursor.fetchone()
    if existing_user:
        print("alert galpa zai higa ok for now user exist zata zalear tege info insert zavpa na ok")
    else:
        cursor.execute('''INSERT INTO `customer` (`fname`, `lname`, `gender`, `email`, `phone`, `pass`, `cpass`) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(fname,lname,gender,email,phone,password1,password2))
        mysql.connection.commit()

    return render_template('/Travelbuddycustomer/login.html')

@app.route('/package')
def package():
    customer_exists = session.get('customer_exists')
    if customer_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `recommendations` WHERE rec_id;''')
        recommendations = cursor.fetchall()
        return render_template('/Travelbuddycustomer/package.html',user=customer_exists, recommendations = recommendations)
    else:
        return render_template('/Travelbuddycustomer/package.html', recommendations = recommendations)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/admin')
def admin():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `customer`;''')
        customer_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/admin_index.html',users = admin_exists)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/ad_login', methods=['GET','POST'])
def ad_login():
    username= request.form.get("email")
    password= request.form.get("pass")
    print(password)
    print(username)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM admin WHERE email=%s and pass=%s; ''',[username,password])
    admin_exists=cursor.fetchone()
    # cursor.execute('''SELECT * FROM `recommendations` WHERE rec_id LIMIT 3;''')
    # existing_user1=cursor.fetchall()
    if not admin_exists:
        return render_template("error.html",error="Incorrect Email Or Password")
    session['logged_in'] = True
    session['admin_data'] = admin_exists
    # session['cust_data'] = existing_user1

    return render_template('/Travelbuddyadmin/template/admin_index.html',users = admin_exists )

@app.route('/admin_index')
def admin_index():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `customer`;''')
        customer_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/admin_index.html',users = admin_exists)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/customer_details')
def customer_details():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `customer`;''')
        customer_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/customer_details.html',users = admin_exists, customer_details = customer_details )
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/bookings')
def bookings():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `booking` INNER JOIN itinerary ON itinerary.itinerary_id = booking.itinerary_id INNER JOIN token ON token.token_id = itinerary.token_id INNER JOIN customer ON customer.cust_id = token.cust_id;''')
        booking_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/bookings.html',users = admin_exists, bookings = booking_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/vendor_details')
def vendor_details():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `vendor`;''')
        vendor_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/vendor_details.html',users = admin_exists, vendor = vendor_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/flight')
def flight():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `flights`;''')
        flight_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/pricing/flights.html', users = admin_exists, flight = flight_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/train')
def train():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `trains`;''')
        train_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/pricing/trains.html',users = admin_exists, train = train_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/bus')
def bus():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `bus`;''')
        bus_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/pricing/bus.html',users = admin_exists, bus = bus_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/rental_vehicle')
def rental_vehicle():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `vehicle_rental`;''')
        rental_vehicle=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/pricing/rentalvehicle.html',users = admin_exists, rental_vehicle=rental_vehicle)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/hotel')
def hotel():
    admin_exists = session.get('admin_data')
    if admin_exists:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `hotels`;''')
        hotel_details=cursor.fetchall()
        return render_template('/Travelbuddyadmin/template/pricing/hotels.html',users = admin_exists, hotel = hotel_details)
    else:
        return render_template('/Travelbuddyadmin/template/samples/login.html')

@app.route('/vendor')
def vendor():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        details = session.get('details')
        count_details = session.get('count_details')
        customer_details = session.get('customer_details')
        return render_template('/Travelbuddyvendor/template/dashboard/busdashboard.html',users = vendor_exists , details = details, count_details = count_details, customer_details=customer_details)
    else:
        return render_template('/Travelbuddyvendor/template/login/login.html')
    

@app.route('/vd_login', methods=['GET','POST'])
def vd_login():
    username= request.form.get("email")
    password= request.form.get("pass")
    print(password)
    print(username)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM vendor WHERE email=%s and pass=%s; ''',[username,password])
    vendor_exists=cursor.fetchone()
    if not vendor_exists:
        return render_template("error.html",error="Incorrect Email Or Password")
    vendor_type = vendor_exists[3]
    vendor_business = vendor_exists[6]
    vendor_id = vendor_exists[0]
    print("vendor name")
    print(vendor_type)
    if vendor_type == 'bus':
        print("going inside bus")
        cursor.execute('''SELECT * FROM `booked_bus` INNER JOIN bus ON bus.bus_id = booked_bus.bus_id WHERE bus.bus_name = %s;''',(vendor_business,))
        details=cursor.fetchall()
        cursor.execute('''SELECT COUNT(booked_bus.booked_bus_id) FROM `booked_bus` INNER JOIN bus ON bus.bus_id = booked_bus.bus_id WHERE bus.bus_name = %s;''',(vendor_business,))
        count_details=cursor.fetchall()
        cursor.execute('''SELECT * FROM `bus` WHERE bus_name = %s AND vendor_id = %s;''',(vendor_business,vendor_id,))
        management=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_bus` INNER JOIN bus ON bus.bus_id = booked_bus.booked_bus_id INNER JOIN vendor ON vendor.vendor_id = bus.vendor_id WHERE vendor.vendor_id = %s AND bus.bus_name = %s;''',(vendor_id,vendor_business,))
        booking=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_bus` INNER JOIN customer ON customer.cust_id = booked_bus.cust_id INNER JOIN bus ON bus.bus_id = booked_bus.bus_id WHERE bus.bus_name = %s;''',(vendor_business,))
        customer_details=cursor.fetchall()
    elif vendor_type == 'flight':
        cursor.execute('''SELECT * FROM booked_flights INNER JOIN flights ON flights.flight_id = booked_flights.flight_id WHERE flights.flight_name = %s;''',(vendor_business,))
        details=cursor.fetchall()
        cursor.execute('''SELECT COUNT(booked_flights.booked_flight_id) FROM booked_flights INNER JOIN flights ON flights.flight_id = booked_flights.flight_id WHERE flights.flight_name = %s;''',(vendor_business,))
        count_details=cursor.fetchall()
        cursor.execute('''SELECT * FROM `flights` WHERE flight_name = %s AND vendor_id = %s;''',(vendor_business,vendor_id,))
        management=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_flights` INNER JOIN flights ON flights.flight_id = booked_flights.flight_id INNER JOIN vendor ON vendor.vendor_id = flights.vendor_id WHERE vendor.vendor_id = %s AND flights.flight_name = %s;''',(vendor_id,vendor_business,))
        booking=cursor.fetchall()
        cursor.execute('''SELECT * FROM booked_flights INNER JOIN customer ON customer.cust_id = booked_flights.cust_id INNER JOIN flights ON flights.flight_id = booked_flights.flight_id WHERE flights.flight_name = %s;''',(vendor_business,))
        customer_details=cursor.fetchall()
    elif vendor_type == 'train':
        cursor.execute('''SELECT * FROM `booked_train` INNER JOIN trains ON trains.train_id = booked_train.train_id WHERE booked_train.train_name = %s;''',(vendor_business,))
        details=cursor.fetchall()
        cursor.execute('''SELECT COUNT(booked_train.booked_train_id) FROM `booked_train` INNER JOIN trains ON trains.train_id = booked_train.train_id WHERE trains.train_name = %s;''',(vendor_business,))
        count_details=cursor.fetchall()
        cursor.execute('''SELECT * FROM `trains` WHERE train_name = %s AND vendor_id = %s;''',(vendor_business,vendor_id,))
        management=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_train` INNER JOIN trains ON trains.train_id = booked_train.train_id INNER JOIN vendor ON vendor.vendor_id = trains.vendor_id WHERE vendor.vendor_id = %s AND trains.train_name = %s;''',(vendor_id,vendor_business,))
        booking=cursor.fetchall()
        cursor.execute('''SELECT * FROM booked_train INNER JOIN customer ON customer.cust_id = booked_train.cust_id INNER JOIN trains ON trains.train_id = booked_train.train_id WHERE booked_train.train_name = %s;''',(vendor_business,))
        customer_details=cursor.fetchall()
    elif vendor_type == 'rental':
        cursor.execute('''SELECT * FROM `booked_vehicle_rentals` INNER JOIN vehicle_rental ON vehicle_rental.vehicle_rental_id = booked_vehicle_rentals.vehicle_rental_id WHERE vehicle_rental.vehicle_rental_name = %s;''',(vendor_business,))
        details=cursor.fetchall()
        cursor.execute('''SELECT COUNT(booked_vehicle_rentals.booked_vehicle_id) FROM `booked_vehicle_rentals` INNER JOIN vehicle_rental ON vehicle_rental.vehicle_rental_id = booked_vehicle_rentals.vehicle_rental_id WHERE vehicle_rental.vehicle_rental_name = %s;''',(vendor_business,))
        count_details=cursor.fetchall()
        cursor.execute('''SELECT * FROM `vehicle_rental` WHERE vehicle_rental_name = %s AND vendor_id = %s;''',(vendor_business,vendor_id,))
        management=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_vehicle_rentals` INNER JOIN vehicle_rental ON vehicle_rental.vehicle_rental_id = booked_vehicle_rentals.vehicle_rental_id INNER JOIN vendor ON vendor.vendor_id = vehicle_rental.vendor_id WHERE vendor.vendor_id = %s AND vehicle_rental.vehicle_rental_name = %s;''',(vendor_id,vendor_business,))
        booking=cursor.fetchall()
        cursor.execute('''SELECT * FROM booked_vehicle_rentals INNER JOIN customer ON customer.cust_id = booked_vehicle_rentals.cust_id INNER JOIN vehicle_rental ON vehicle_rental.vehicle_rental_id = booked_vehicle_rentals.vehicle_rental_id WHERE vehicle_rental.vehicle_rental_name = %s;''',(vendor_business,))
        customer_details=cursor.fetchall()
    elif vendor_type == 'hotel':
        cursor.execute('''SELECT * FROM booked_hotel INNER JOIN hotels ON hotels.hotel_id = booked_hotel.hotel_id WHERE hotels.hotels_name = %s;''',(vendor_business,))
        details=cursor.fetchall()
        cursor.execute('''SELECT COUNT(booked_hotel.booked_hotel_id) FROM booked_hotel INNER JOIN hotels ON hotels.hotel_id = booked_hotel.hotel_id WHERE hotels.hotels_name = %s;''',(vendor_business,))
        count_details=cursor.fetchall()
        cursor.execute('''SELECT * FROM `hotels` WHERE hotels_name = %s AND vendor_id = %s;''',(vendor_business,vendor_id,))
        management=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_hotel` INNER JOIN hotels ON hotels.hotel_id = booked_hotel.hotel_id INNER JOIN vendor ON vendor.vendor_id = hotels.vendor_id WHERE vendor.vendor_id = %s AND hotels.hotels_name = %s;''',(vendor_id,vendor_business,))
        booking=cursor.fetchall()
        cursor.execute('''SELECT * FROM `booked_hotel` INNER JOIN customer ON customer.cust_id = booked_hotel.cust_id INNER JOIN hotels ON hotels.hotel_id = booked_hotel.hotel_id WHERE hotels.hotels_name = %s;''',(vendor_business,))
        customer_details=cursor.fetchall()

    if not vendor_exists:
        return render_template("error.html",error="Incorrect Email Or Password")
    session['logged_in'] = True
    session['vendor_data'] = vendor_exists
    session['details'] = details
    session['count_details'] = count_details
    session['management'] = management
    session['booking'] = booking
    session['customer_details'] = customer_details
    # session['cust_data'] = existing_user1

    return render_template('/Travelbuddyvendor/template/dashboard/busdashboard.html',users = vendor_exists , details = details, count_details = count_details, management=management,customer_details=customer_details)

    
@app.route('/busdashboard')
def busdashboard():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        details = session.get('details')
        count_details = session.get('count_details')
        customer_details = session.get('customer_details')
        return render_template('/Travelbuddyvendor/template/dashboard/busdashboard.html',users = vendor_exists , details = details, count_details = count_details, customer_details=customer_details)
    else:
        return render_template('/Travelbuddyvendor/template/login/login.html')

@app.route('/busbooking')
def busbooking():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        details = session.get('details')
        count_details = session.get('count_details')
        booking = session.get('booking')
        customer_details = session.get('customer_details')
        return render_template('/Travelbuddyvendor/template/bookings/busbooking.html', users = vendor_exists, details = details, count_details = count_details, booking=booking,customer_details=customer_details)
    else:
        return render_template('/Travelbuddyvendor/template/login/login.html')

@app.route('/customerdetalis')
def customerdetalis():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        customer_details = session.get('customer_details')
        return render_template('/Travelbuddyvendor/template/customerdetalis.html', users = vendor_exists,customer_details=customer_details)
    else:
        return render_template('/Travelbuddyvendor/template/login/login.html')
    
@app.route('/busmanagement')
def busmanagement():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        management = session.get('management')
        return render_template('/Travelbuddyvendor/template/management/busmanagement.html', users = vendor_exists, management= management)
    else:
        return render_template('/Travelbuddyvendor/template/login/login.html')

@app.route('/buspricing')
def buspricing():
    vendor_exists = session.get('vendor_data')
    if vendor_exists:
        return render_template('/Travelbuddyvendor/template/pricing/buspricing.html', users = vendor_exists)

@app.route('/busschedule')
def busschedule():
    return render_template('/Travelbuddyvendor/template/schedules/busschedule.html')

# @app.route('/itinerarycreate')
# def itinerarycreate():
#     user_data = session.get('user_data')
#     return render_template('itinerarycreate.html')

# @app.route('/signup')
# def signup():
#     customer_exists = session.get('customer_exists')
#     recommendations = session.get('existing_user1')
#     print(customer_exists)
#     if customer_exists:
#         print("user exist zata")
#         return render_template("/Travelbuddycustomer/home.html", users=customer_exists, recommendations=recommendations)
#     else:
#         print("user exist zaina")
#         return render_template('/Travelbuddycustomer/signup.html')

# @app.route('/profile_edit')
# def profile_edit():
#     return render_template('/Travelbuddycustomer/profile_edit.html')

# @app.route('/edit_itinerary')
# def edit_itinerary():
#     cursor = mysql.connection.cursor()
#     cursor.execute('''SELECT `token_id` FROM token ORDER BY token_id DESC LIMIT 1;''')
#     latest_token_id = cursor.fetchone()[0]
#     print("Latest token_id:", latest_token_id)
#     cursor.execute('''SELECT * FROM `itinerary` WHERE token_id=%s;''',[latest_token_id])
#     itinerary=cursor.fetchall()

#     # parsed_data = [(item[0], eval(item[1]), item[2]) for item in itinerary]
#     # for item in itinerary:
#     #     print(item)
#     # sorted_itinerary = sorted(itinerary, key=lambda x: (x[0], x[1], x[2], x[4]))

#     # sorted_data = sorted(itinerary, key=lambda x: (eval(x[1])[0], eval(x[1])[1], eval(x[1])[2], eval(x[1])[4]))

# # Print the sorted data
#     # for item in itinerary:
#     #     print(item)
    
#     for activity in itinerary:
#         cursor.execute('''SELECT * FROM `sightseeing` WHERE `name`=%s;''',[activity[2]])
#         fetching1=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `shopping` WHERE `name`=%s;''',[activity[2]])
#         fetching2=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `nightlife` WHERE `name`=%s;''',[activity[2]])
#         fetching3=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `museum` WHERE `name`=%s;''',[activity[2]])
#         fetching4=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `historic` WHERE `name`=%s;''',[activity[2]])
#         fetching5=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `hiking` WHERE `name`=%s;''',[activity[2]])
#         fetching6=cursor.fetchall()
#         cursor.execute('''SELECT * FROM `beach_activities` WHERE `name`=%s;''',[activity[2]])
#         fetching7=cursor.fetchall()
        
#         if fetching1:
#             cursor.execute('''SELECT * FROM `sightseeing` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching2:
#             cursor.execute('''SELECT * FROM `shopping` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching3:
#             cursor.execute('''SELECT * FROM `nightlife` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching4:
#             cursor.execute('''SELECT * FROM `museum` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching5:
#             cursor.execute('''SELECT * FROM `historic` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching6:
#             cursor.execute('''SELECT * FROM `hiking` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()
#         elif fetching7:
#             cursor.execute('''SELECT * FROM `beach_activities` WHERE `name` <> %s ORDER BY RAND() LIMIT 5;''',[activity[2]])
#             extraction=cursor.fetchall()

#     return render_template('/edit_itinerary.html',itinerary = itinerary, extraction=extraction)

# @app.route('/con_submit')
# def con_submit():
#     # user_data = session.get('user_data')
#     # if user_data:
#         # cursor = mysql.connection.cursor()
#         # cursor.execute('''INSERT INTO itinerary (`itinerary`,`token_id`) VALUES(%s,%i)''',(creating_days))
#         # cursor.execute('''INSERT INTO itinerary (`itinerary`,`token_id`) VALUES(%s,%i)''',(creating_days))
#         # mysql.connection.commit()
#     return render_template('/Travelbuddycustomer/payments/docs/payments/payment.html')

# @app.route('/recommend_page')
# def recommend_page():
#     cursor = mysql.connection.cursor()
#     cursor.execute('''SELECT * FROM recommendations;''')
#     existing_user1=cursor.fetchall()
#     return render_template('/Travelbuddycustomer/reccomendation.html', existing_user1=existing_user1)

# @app.route('/payment_submit')
# def payment_submit():
#     # write conditions here and than thank you page
#     return render_template('/Travelbuddycustomer/payments/docs/thankyou/thanku.html')

# @app.route('/login', methods=['POST'])
# def login():
#     # Check user credentials and log in
#     customer_exists = session.get('customer_exists')
#     if customer_exists in session:
#         print("inside login customer exist zata")
#         return render_template("/Travelbuddycustomer/home.html", users=customer_exists, recommendations=existing_user1) #CHECK THIS FILE NAME LATERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
#     else:
#         username= request.form.get("emailcheck")
#         password=request.form.get("passwordcheck")
#         cursor = mysql.connection.cursor()
#         cursor.execute('''SELECT * FROM customer WHERE email=%s and pass=%s; ''',[username,password])
#         customer_exists=cursor.fetchone()
#         cursor.execute('''SELECT * FROM `recommendations` WHERE rec_id LIMIT 3;''')
#         existing_user1=cursor.fetchall()
#         if not customer_exists:
#             return render_template("error.html",error="Incorrect Email Or Password")
#         session['logged_in'] = True
#         session['cust_data'] = customer_exists
#         session['cust_data'] = existing_user1

#         return render_template('/Travelbuddycustomer/home.html', users=customer_exists, recommendations=existing_user1)
#         # return redirect(url_for('home'))

# @app.route('/csignup', methods=['POST'])
# def csignup():
#     customer_exists = session.get('customer_exists')
#     existing_user1 = session.get('existing_user1')
#     if customer_exists in session:
#         print("user exist zata in csignup")
#         return render_template("/Travelbuddycustomer/home.html", users=customer_exists, recommendations=existing_user1) 
#     else:
#         fname= request.form.get("fname")
#         lname= request.form.get("lname")
#         gender= request.form.get("gender")
#         email= request.form.get("email")
#         phone= request.form.get("phone")
#         password1=request.form.get("password")
#         password2=request.form.get("cpassword")
#         cursor = mysql.connection.cursor()
#         cursor.execute('''SELECT * FROM customer WHERE email=%s and pass=%s; ''',[email,password1])
#         existing_user=cursor.fetchone()
        

#         if existing_user:
#             return render_template("error.html",error="This email has laready been used for another account. Please use another email.")


#         elif password1 != password2:
#             return render_template("error.html",error="Passwords do not match")


#         else:
#             #CHECK THIS THING LATER BECAUSE GENDER IS NOT ADDED IN THE SIGN IN FORM------------------------------------------------------
#             # hashed_password=generate_password_hash(password2, method='pbkdf2:sha256', salt_length=8)
#             cursor = mysql.connection.cursor()
#             cursor.execute('''INSERT INTO `customer` (`fname`, `lname`, `gender`, `email`, `phone`, `pass`, `cpass`) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(fname,lname,gender,email,phone,password1,password2))
#             mysql.connection.commit()
#             cursor.execute('''SELECT * FROM customer WHERE email=%s and pass=%s; ''',[email,password1])
#             returned_user=cursor.fetchone()
#             session["cust_id"] = returned_user[0]
#             flash('Registered!')
#             cursor.close()
#             return redirect("/signup")

# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")

# # ADMIN SIDE 
# @app.route('/admin')
# def admin():
#     user_data = session.get('user_data')
#     if user_data  in session:
#         return redirect(url_for('admin_index'))
#     return render_template('/Travelbuddyadmin/template/samples/login.html')

# @app.route('/ad_login', methods=['POST'])
# def ad_login():
#     # Check user credentials and log in
#     # if request.method == "GET":
#     #     return render_template("register.html") #CHECK THIS FILE NAME LATERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
#     user_data = session.get('user_data')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/admin_index.html', users=user_data)
#     else:
#         username= request.form.get("email")
#         password=request.form.get("pass")
#         cursor = mysql.connection.cursor()
#         cursor.execute('''SELECT * FROM `admin` WHERE email=%s and pass=%s ''',[username,password])
#         existing_user=cursor.fetchone()
#         # -------------------------------------------------------------------------------------------------------------
#         cursor.execute('''SELECT * FROM `customer`''')
#         existing_user1=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `booking` INNER JOIN itinerary ON itinerary.itinerary_id = booking.itinerary_id;''')
#         existing_user2=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `flights`;''')
#         existing_user3=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `trains`;''')
#         existing_user4=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `bus`;''')
#         existing_user5=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `car_rental`;''')
#         existing_user6=cursor.fetchall()

#         cursor.execute('''SELECT * FROM `hotels`;''')
#         existing_user7=cursor.fetchall()
        
#         cursor.execute('''SELECT * FROM `vendor`;''')
#         existing_user8=cursor.fetchall()
#         #-----------------------------------------------------------------------------------------------
#         if not existing_user:
#             return render_template("error.html",error="Incorrect Email Or Password")
#         session['logged_in'] = True
#         session['user_data'] = existing_user
#         session['customer_details'] = existing_user1
#         session['bookings'] = existing_user2
#         session['flight'] = existing_user3
#         session['train'] = existing_user4
#         session['bus'] = existing_user5
#         session['rental_vehicle'] = existing_user6
#         session['hotel'] = existing_user7
#         session['vendor'] = existing_user8
#         return render_template('/Travelbuddyadmin/template/admin_index.html', users=existing_user)
#         # return redirect(url_for('home'))

# @app.route('/admin_index')
# def admin_index():
#     user_data = session.get('user_data')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/admin_index.html', users=user_data)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/customer_details')
# def customer_details():
#     user_data = session.get('user_data')
#     customer_details = session.get('customer_details')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/customer_details.html', users=user_data ,customer_details=customer_details)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/bookings')
# def bookings():
#     user_data = session.get('user_data')
#     bookings = session.get('bookings')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/bookings.html', users=user_data, bookings=bookings)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")
   
# @app.route('/vendor_details')
# def vendor_details():
#     user_data = session.get('user_data')
#     vendor = session.get('vendor')
#     if user_data:
#     # VENDOR TABLE NOT THERE-------------------------------
#         return render_template('/Travelbuddyadmin/template/vendor_details.html', users=user_data, vendor=vendor)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/flight')
# def flight():
#     user_data = session.get('user_data')
#     flight = session.get('flight')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/pricing/flights.html', users=user_data, flight=flight)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/train')
# def train():
#     user_data = session.get('user_data')
#     train = session.get('train')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/pricing/trains.html', users=user_data, train=train)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/bus')
# def bus():
#     user_data = session.get('user_data')
#     bus = session.get('bus')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/pricing/bus.html', users=user_data, bus=bus)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/rental_vehicle')
# def rental_vehicle():
#     user_data = session.get('user_data')
#     rental_vehicle = session.get('rental_vehicle')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/pricing/rentalvehicle.html', users=user_data, rental_vehicle=rental_vehicle)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# @app.route('/hotel')
# def hotel():
#     user_data = session.get('user_data')
#     hotel = session.get('hotel')
#     if user_data:
#         return render_template('/Travelbuddyadmin/template/pricing/hotels.html', users=user_data, hotel=hotel)
#     else:
#         return render_template("error.html", error="Admin not logged in <a href='/admin'>Click Here To Login</a>.")

# # VENDOR SIDE
# @app.route('/vendor')
# def vendor():
#     # user_data = session.get('user_data')
#     # if user_data:
#         # return render_template('/Travelbuddyvendor/template/login/bus_login.html', users=user_data)
#     return render_template('/Travelbuddyvendor/template/login/bus_login.html')








#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
# DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART
# DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART
# DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART
# DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART
# DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART - DON'T EDIT OR DELETE THE BELOW PART
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************
# --------------------------------------------------------------------------

@app.route('/submit', methods=['POST'])
def submit():
    global form_data
    org = request.form['source']
    dest = request.form['destination']
    start = request.form['arrival_date']
    end = request.form['departure_date']
    age_range = request.form['ageGroup']
    travel_type = request.form['travel_type']
    trip_type = request.form['trip_type']
    nots = request.form['numTravelers']
    budget = request.form['budget']
    
    print(start)
    print(end)
    print(budget)
    cal_budget = int_budget(budget) 
    days = calculate_days(start,end)
    print(days)
    percentage = percentage_calculator(cal_budget)
    print(percentage)
    transportation = transportation_avaliable(org, dest,percentage,cal_budget,int(nots))
    print(transportation)
    print(transportation[1][10])
    transportation_cost_per_person = transportation[1][10]
    transportation_cost = transportation_cost_per_person*int(nots)

    # FOR NOW LOCATION ID = 10
    loc_id = 10
    hotel = hotel_available(loc_id,int(percentage),days)
    print(hotel)
    print("hehehehe",hotel[1][6])
    hotel_price_per_day = hotel[1][6]
    hotel_cost = days*hotel_price_per_day
    print('hotel cost days: ',hotel_cost)

    # cal_budget = cal_budget-(int(transportation[0]) + int(hotel[0])) #THIS LINE WILL WORK LATER.. SINCE IDK THE RIGHT ARRAY INDEX FOR PRICE
    print(cal_budget)

    total_cost = "{:.2f}".format(hotel_cost + transportation_cost)

    act = get_user_data(age_range,travel_type,trip_type,days,budget)
    print(act)
    print(act[0][5])
    # act_up = []
    # act_up.append(act[0][5])
    # activities = act_up
    # print(act_up)
    # input_string = []
    input_string = str(act[0][5])
    activities = extract_act(input_string)
    print(activities)
    # UNCOMMENT THE ABOVE 4 TIME AND ONCES THAT EXTRACTION AGLO IS WORKING----------------------------------------------AND COMMENT THE BELOW LINE---------
    # activities = ["Sightseeing","BeachActivities", "Nightlife", "Shopping"]
    arrive = transportation[1][6]
    print(arrive)
    location = int(hotel[1][7])
    print("location")
    print(location)
    creating_days = creating_data(activities,days,trip_type,location,arrive)
    # act_data = activities_data(sample)
    # percentage = percentage_calculator(float(budget))
    # transportation = transportation_avaliable(org, dest,percentage,int(budget),int(nots))
    # hotel = hotel_available(dest,int(percentage),days)
    # budget = int(budget)-(int(transportation[0]) + int(hotel[0]))#-------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------

    
    # total_per_day = per_day_expense(trip_type,int(nots),days,int(budget))
    # if type(total_per_day) == int:
        # budget = int(budget)-int(total_per_day)
    # cust_data = session.get('cust_data')
    # print(cust_data)  
    # if cust_data:
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('''INSERT INTO `token` ( `cust_id`) VALUES (%s )''',(cust_data[0],))

    #     cursor.execute('''SELECT * FROM `token` ORDER BY token_id DESC LIMIT 1;''')
    #     existing_cust=cursor.fetchall()
    #     print(existing_cust)
    #     cursor.execute('''INSERT INTO itinerary (`itinerary`,`token_id`) VALUES(%s,%s)''',(creating_days,existing_cust[0],))
    #     mysql.connection.commit()

    # -------------------------------------------------------------------------------------------------------------------------------------
    # car = car_rental_available(dest,budget,days) #if you are commenting the previous two lines and add this line in the if statement

    # gptPrompt(start,end,travel_type,nots,trip_type,budget)
    # -------------------------------------------------------------------------------------------------------------------------------------

    if creating_days:
        customer_exists = session.get('customer_exists')
        if not customer_exists:
            return render_template('/Travelbuddycustomer/login.html')
        cust_id=str(customer_exists[0]) #CHANGE THIS BY CUST ID SESSION -----------------------------------------------------------------
        print('customer iddddddddd ',cust_id) 
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO `token` (`token_id`, `cust_id`) VALUES (NULL, %s);''',(cust_id))
        cursor.execute('''SELECT * FROM `token` ORDER BY token_id DESC LIMIT 1;''')
        existing_user2=cursor.fetchall()
        print(existing_user2)
        print(existing_user2[0][0])
        token = str(existing_user2[0][0])

        activities = []
        for item in creating_days:
            if isinstance(item, str):
                current_day = item
            elif isinstance(item, list) and item:
                for activity in item:
                    activities.append((current_day,) + activity)

        # Insert activities into the database
        # for activity in activities:
        #     try:
        #         cursor.execute('''INSERT INTO `itinerary` (`itinerary_id`, `days`, `itinerary`, `itinerary_loc`, `description`, `taluka`, `token_id`) VALUES (NULL, %s, %s);''', (str(activity), token))
                                
        #         conn.commit()
                 
        #         # VALUES (NULL, 'bfasd', 'dfsd', 'dfas', 'dsfa', 'dsfa', '18');
        #     except Exception as e:
        #         conn.rollback()
        #         print("Error:", e)
        
        # mysql.connection.commit()

        for item in creating_days:
            cursor = mysql.connection.cursor()
            if isinstance(item, str) and item.startswith('Day'):
                current_day = item
                print("daysssssssssssssssssssss")
            else:
                for activity in item:
                    print(activity)
                    cursor.execute("INSERT INTO itinerary (itinerary_id, days, itinerary, itinerary_loc, description, taluka, token_id,image) VALUES (NULL,  %s, %s, %s, %s, %s, %s, %s)", (current_day, activity[0], activity[1], activity[2], activity[3], token, activity[4]))
                    print("zale re zale")

        # cursor.execute("INSERT INTO itinerary (itinerary_id, days, itinerary, itinerary_loc, description, taluka, token_id) VALUES (NULL,  %s, %s, %s, %s, %s, %s)", (current_day, activity[0], activity[1], activity[2], activity[3], token))
        mysql.connection.commit()


    return render_template('/Travelbuddycustomer/display_itenary.html', org=org, dest=dest,start=start,end=end, budget=budget,days=days,transportation=transportation, hotel=hotel, creating_days=creating_days,total_cost=total_cost) ## --TO PRINT DATA BACK TO HTML
    return render_template('generated.html', org=org, dest=dest,start=start,end=end, budget=budget,days=days,transportation=transportation, hotel=hotel, creating_days=creating_days) ## --TO PRINT DATA BACK TO HTML
    # return f"Submitted Data: Org - {org}\n, dest - {dest}\n days = {days} {percentage} {transportation} {hotel} {budget} {car}\n"

    # return f"Submitted Data: Org - {org}\n, dest - {dest}\n days = {days} {act} {creating_days}\n"
    # else:
    #     return f"Please Increase your budget"

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
