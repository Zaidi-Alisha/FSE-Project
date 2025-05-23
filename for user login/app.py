from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import random
from flask import jsonify

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    
    # Mock data for nearby banquets
    nearby_banquets = [
        {"name": "Grand Palace", "distance": "1.2 km"},
        {"name": "Royal Orchid Banquet", "distance": "2.0 km"},
        {"name": "Sunset Banquet Hall", "distance": "2.5 km"}
    ]
    
    # Example response for simplicity
    banquet_list = '<br>'.join([f"{b['name']} - {b['distance']}" for b in nearby_banquets])
    return jsonify({"message": f"Nearby Banquets:<br>{banquet_list}"})

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['venue_booking']
users_collection = db['users']

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = users_collection.find_one({'name': name, 'password': password})
        if user:
            session['user'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Username or password not found')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        account = str(random.randint(1000000000, 9999999999))
        amount = float(request.form['amount'])

        user = {
            'name': name,
            'password': password,
            'email': email,
            'contact': contact,
            'account_number': account,
            'amount': amount
        }
        users_collection.insert_one(user)
        session['user'] = name
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/venue-list')
def venue_list():
    return "<h2>This will be the next page where you show venues or bookings etc.</h2>"

@app.route('/select-area')
def select_area():
    venue_db = client['venue_booking']
    banquets_collection = venue_db['banquets']
    areas = banquets_collection.distinct("Area")
    return render_template("select_area.html", areas=areas)

@app.route('/get-venues', methods=['POST'])
def get_venues():
    data = request.get_json()
    selected_area = data.get("area")

    venue_db = client['venue_booking']
    banquets_collection = venue_db['banquets']

    venues = banquets_collection.find({"Area": selected_area})
    venue_list = [
        {
            "name": venue["Banquet Name"],
            "capacity": venue["Capacity"]
        } for venue in venues
    ]
    return jsonify(venue_list)

@app.route('/payment', methods=['POST'])
def payment():
    area = request.form['selected_area']
    venue = request.form['selected_venue']
    time = request.form['selected_time']
    price = float(request.form['selected_price'])

    advance = round(price * 0.2, 2)  # 20% advance

    return render_template("payment.html", venue=venue, price=price, advance=advance, time=time, area=area)


if __name__ == '__main__':
    app.run(debug=True)
