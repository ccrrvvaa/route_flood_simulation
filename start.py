from flask import Flask
from flask import render_template
from flask import request
from settings import *
import googlemaps
import math
import json

app = Flask(__name__)


def get_nearest_locations(base_location, black_list):
	radius = 0.003
	xl = math.sqrt(3) * radius / 2

	locations = [
		(base_location[0] - radius, base_location[1]),
		(base_location[0] - radius / 2, base_location[1] - xl),
		(base_location[0], base_location[1] - radius),
		(base_location[0] + radius / 2, base_location[1] - xl),
		(base_location[0] + radius, base_location[1]),
		(base_location[0] + radius / 2, base_location[1] + xl),
		(base_location[0], base_location[1] + radius),
		(base_location[0] - radius / 2, base_location[1] + xl),
	]

	values_found = []
	for l in locations:
		if l in black_list:
			values_found.append(l)

	if len(values_found):
		for v in values_found:
			locations.remove(v)
	
	return locations


def get_lowest_elevation(locations):
	gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
	result = gmaps.elevation(locations)

	elevation = 10000
	result_item = None

	for r in result:
		if r['elevation'] < elevation:
			result_item = r
			elevation = r['elevation']

	return (result_item['location']['lat'], result_item['location']['lng'])


def get_simulated_route(base_location, size):
	location = base_location
	route = [base_location]
	black_list = [base_location]

	for i in range(size):
		locations = get_nearest_locations(location, black_list)
		if len(locations) == 0:
			break

		black_list += locations
		location = get_lowest_elevation(locations)
		route.append(location)

	return route


@app.route("/")
def home():
    return render_template('layout.html', key=GOOGLE_API_KEY)


@app.route('/simulate', methods=['POST'])
def simulate():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    base_location = (lat, lng)

    route = get_simulated_route(base_location, 20)

    return json.dumps(route)

if __name__ == "__main__":
    app.run()