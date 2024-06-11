import numpy as np


def compute_wca(true_course: float, true_airspeed: float, wind_direction: float, wind_speed: float) -> float:
    """
    Compute the wind correction angle.

    :param true_course: the course that the aircraft must fly on a sectional map in degrees.
    :param true_airspeed: the true airspeed of the aircraft during the maneuver in kts.
    :param wind_direction: the wind direction relative to true north in degrees.
    :param wind_speed: the wind speed in kts.
    :return: wind correction angle in degrees.
    """
    acute_wind_angle = (wind_direction - true_course) % 360

    wca = np.arctan2(wind_speed*np.sin(np.deg2rad(acute_wind_angle)), true_airspeed)

    return np.rad2deg(wca)


def compute_gs(true_course: float, true_airspeed: float, wind_direction: float, wind_speed: float) -> float:
    """
    Computes the ground speed in kts.

    :param true_course: the course that the aircraft must fly on a sectional map in degrees.
    :param true_airspeed: the true airspeed of the aircraft during the maneuver in kts.
    :param wind_direction: the wind direction relative to true north in degrees.
    :param wind_speed: the wind speed in kts.
    :return: the computed ground speed in kts.
    """
    tc_rad = np.deg2rad(true_course)
    wd_rad = np.deg2rad(wind_direction)
    wca_rad = np.deg2rad(compute_wca(true_course, true_airspeed, wind_direction, wind_speed))

    ground_speed = np.sqrt(true_airspeed ** 2 + wind_speed ** 2 -
                           2 * true_airspeed * wind_speed * np.cos(tc_rad - wd_rad + wca_rad))

    return ground_speed


if __name__ == '__main__':
    true_course = 90
    wca = compute_wca(true_course=true_course, true_airspeed=120, wind_direction=289, wind_speed=21)
    gs = compute_gs(true_course=true_course, true_airspeed=120, wind_direction=289, wind_speed=21)
    print(f'To head {true_course}, fly: {true_course + wca}')
    print(f'Ground speed: {gs}')