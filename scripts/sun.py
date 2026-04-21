import math
from datetime import datetime, timedelta

def get_sun_times(lat, lon, date_obj, tz_offset_hours):
    # 1. Basic inputs
    day_of_year = date_obj.timetuple().tm_yday

    # 2. Calculate Solar Declination (the angle of the sun relative to the equator)
    # This is an approximation of the Earth's tilt
    declination = math.radians(23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 81))))

    # 3. Calculate the Zenith Angle
    # We use 90.833 degrees instead of 90 to account for atmospheric refraction
    # (why we see the sun before it actually rises)
    zenith_rad = math.radians(90.833)
    lat_rad = math.radians(lat)

    # 4. Calculate the Hour Angle (H)
    # This formula finds the angle between the sun and the meridian
    try:
        cos_h = (math.cos(zenith_rad) - (math.sin(lat_rad) * math.sin(declination))) / \
                (math.cos(lat_rad) * math.cos(declination))

        if cos_h > 1: return None, None # Sun never rises (Arctic Summer)
        if cos_h < -1: return None, None # Sun never sets (Arctic Winter)

        hour_angle = math.acos(cos_h)
    except ValueError:
        return None, None

    # 5. Calculate Solar Noon (Simplified: assumes longitude correction)
    # In a real scenario, you'd calculate the Equation of Time,
    # but for a simple script, we align it to the date.
    # We'll use 12:00 as the base and apply the longitude correction.

    # Longitude correction: Each 15 degrees is 1 hour.
    # We adjust the 12:00 noon based on how far you are from the Prime Meridian.
    seconds_correction = (lon / 15.0) * 3600
    solar_noon_base = datetime(date_obj.year, date_obj.month, date_obj.day, 12, 0, 0)

    # 6. Calculate Sunrise/Sunset offset from noon in hours
    offset_hours = math.degrees(hour_angle) / 15.0

    # 7. Apply all offsets to find actual local time
    # We subtract the longitude correction and apply the timezone offset
    sunrise = solar_noon_base - timedelta(hours=offset_hours) - timedelta(seconds=seconds_correction) + timedelta(hours=tz_offset_hours)
    sunset = solar_noon_base + timedelta(hours=offset_hours) - timedelta(seconds=seconds_correction) + timedelta(hours=tz_offset_hours)

    return sunrise, sunset

# --- CONFIGURATION ---
MY_LAT = 39.4029    # Replace with your Latitude
MY_LON = -107.2157   # Replace with your Longitude
MY_TZ = -6          # Your UTC Offset (e.g., -5 for EST)
# ---------------------

today = datetime.now()
rise, set_ = get_sun_times(MY_LAT, MY_LON, today, MY_TZ)

if rise:
    print(f"Date: {today.strftime('%Y-%m-%d')}")
    print(f"Sunrise: {rise.strftime('%H:%M:%S')}")
    print(f"Sunset:  {set_.strftime('%H:%M:%S')}")
else:
    print("The sun does not rise/set at this location on this date.")
