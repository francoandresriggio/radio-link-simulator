import math

EARTH_RADIUS = 6372.795477598

def calculate_distance(latitude, longitude):
    distances = []
    rad = math.pi / 180  # Convert degrees to radians

    for i in range(len(latitude)):
        dlat = latitude[i] - latitude[0]
        dlon = longitude[i] - longitude[0]
        a = (math.sin(rad * dlat / 2))**2 + math.cos(rad * latitude[0]) * math.cos(rad * latitude[i]) * (math.sin(rad * dlon / 2))**2
        distances.append(2 * EARTH_RADIUS * math.asin(math.sqrt(a)) * 1000)  # Convert from km to meters

    return distances

def slope_between_points(altitude, extreme_distance):
    altitude_difference = altitude[-1] - altitude[0]
    return altitude_difference / extreme_distance

def radio_link_distance(slope, distances):
    radio_distances = []
    angle = math.atan(slope)

    for i in range(len(distances)):
        radio_distances.append(distances[i] / math.cos(angle))
    
    return radio_distances

def line_height_fresnel_radius(n, lambda_sim, k, slope, radio_distances, altitude, distances):
    upper_radius = []
    straight_line = []
    apparent_altitude = []

    lambda_sim *= 0.001

    for i in range(len(distances)):
        upper_radius.append(math.sqrt((n * lambda_sim * radio_distances[i] * (radio_distances[-1] - radio_distances[i])) / (radio_distances[i] + (radio_distances[-1] - radio_distances[i]))))
        straight_line.append(slope * distances[i] + altitude[0])
        apparent_altitude.append(((distances[i] * (distances[-1] - distances[i]) * lambda_sim * n) / (2 * k * EARTH_RADIUS * 1000)) + altitude[i])
    
    return upper_radius, straight_line, apparent_altitude

def rotate_calculate_radii(radio_distances, slope, upper_radius, straight_line, samples):
    angle = math.atan(-slope)
    lower_radius = []

    for i in range(samples):
        lower_radius.append((-radio_distances[i] * math.sin(angle)) + (-upper_radius[i] * math.cos(angle)) + straight_line[0])
        upper_radius[i] = (-radio_distances[i] * math.sin(angle)) + (upper_radius[i] * math.cos(angle)) + straight_line[0]

    return lower_radius, upper_radius

def antenna_heights(straight_line, upper_radius, lower_radius, samples, percentage, apparent_altitude):
    i = 0
    while i < samples:
        if apparent_altitude[i] > lower_radius[i] + ((straight_line[i] - lower_radius[i]) * (1 - percentage / 100)):
            for j in range(samples):
                straight_line[j] += 1
                upper_radius[j] += 1
                lower_radius[j] += 1
            i = 0
        i += 1
    
    return straight_line, upper_radius, lower_radius

def calculate_power(eirp, gain, distance, lambda_sim):
    path_loss = 20 * math.log10(float(4 * math.pi * distance) / (lambda_sim * 0.001))
    return eirp + gain - path_loss