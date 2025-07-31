
import math
import numpy as np

# Earth's radius in km
R = 6371.0

def latlon_to_cartesian(lat_deg, lon_deg, radius=R):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    x = radius * math.cos(lat) * math.cos(lon)
    y = radius * math.cos(lat) * math.sin(lon)
    z = radius * math.sin(lat)
    return np.array([x, y, z])

def get_look_vector_and_angle(lat1, lon1, lat2, lon2):
    p1 = latlon_to_cartesian(lat1, lon1)
    p2 = latlon_to_cartesian(lat2, lon2)

    direction = p2 - p1
    unit_dir = direction / np.linalg.norm(direction)

    # Local "up" at point A is just the vector from Earth's center to p1
    local_up = p1 / np.linalg.norm(p1)

    # Angle between local up and the look direction
    angle_rad = math.acos(np.dot(unit_dir, local_up))
    angle_deg = math.degrees(angle_rad)

    return unit_dir, angle_deg

# Example: from Prague (50.0755, 14.4378) to Wellington, NZ (-41.2865, 174.7762)
direction_vector, angle_into_earth = get_look_vector_and_angle(39.0689,
                                                               108.5643
                                                               , 48.6293,
                                                               21.7197)

print("Direction vector through Earth:", direction_vector)
print("Angle into the Earth (degrees):", angle_into_earth)
