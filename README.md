# route_flood_simulation
This is a simulation of the probable route that a flood would take.

This project is made with the framework Flask (python 3.x)
I'm using two services: google maps api and google elevation api.

Process:
The idea is to select or mark a point in the map and build the possible route that a flood should take based on 	
altitudes. So based on the original point, I create 8 points rounding the original point (using a radius) and I get the lower
point using Google Elevation Api. Then I use this lowest point as the origin point and I repeat the previous steps and continue
with this process in order to draw joined lines which in this case this would be the route that the flood should take.
