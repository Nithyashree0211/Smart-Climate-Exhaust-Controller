"""
utils.py
Utility functions for Smart Climate & Exhaust Controller
"""

def calculate_dew_point(temperature, humidity):
    """
    Calculate dew point using a simple approximation.

    Parameters:
        temperature (float): Temperature in °C
        humidity (float): Relative Humidity (%)

    Returns:
        float: Dew Point (°C)
    """
    return round(temperature - ((100 - humidity) / 5), 1)


def get_status(temperature):
    """
    Determine system status based on temperature.

    Returns:
        (status, fan_speed, led)
    """

    if temperature < 30:
        return ("NORMAL", 30, "GREEN")

    elif temperature < 35:
        return ("WARNING", 60, "YELLOW")

    else:
        return ("DANGER", 100, "RED")
