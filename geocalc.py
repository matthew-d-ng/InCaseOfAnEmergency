import math

class Boundary:
    def _init_(left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    # Find the distance between two places given their latitude and longitude.
    # get_distance returns the distance betwen place1 and place2.
    def get_distance(latitude, longitude, source_lat, source_long):
        # Δσ: central angle, φ1: latitude1,
        # φ2: latitude2, Δφ: difference b/w lat,
        # Δλ: difference b/w long
        #
        # Δσ = 2 * arcsin √(sin^2(Δφ/2) + cos(φ1) * cos(φ2) * sin^2(Δλ/2))
        # distance = rΔσ, where r is radius of the given sphere (earth)

        delta_lat = math.fabs(source_lat - latitude)
        delta_long = math.fabs(source_long - longitude)
        a = math.pow(math.sin(delta_lat / 2), 2)
        b = math.cos(source_lat) * math.cos(latitude)
        c = math.pow(math.sin(delta_long / 2), 2)
        central_angle = 2 * math.asin(math.sqrt(a + b * c))
        return earth_rad * central_angle
    
    # get_boundary returns an object that contains the latitude and longitude
    # values of a square boundary around a queries city.
    def get_boundary(longitude, latitude):

    def toString():
        print("Left: ", self.left, "; Right: ", self.right,
                "; Top: ", self.top, "; Bottom: ", self.bottom)