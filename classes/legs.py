from classes.aircraft import Aircraft
from classes.waypoints import Waypoint
from models.winds import compute_wca, compute_gs


class Leg:
    """
    Generic class for the leg of a flight plan.
    """
    def __init__(self,
                 from_waypoint: Waypoint,
                 to_waypoint: Waypoint,
                 distance: float,
                 true_course: float,
                 true_airspeed: float,
                 start_altitude: float,
                 end_altitude: float,
                 wind_direction: float,
                 wind_speed: float,
                 temperature: float,
                 mag_var: float) -> None:
        """
        :param from_waypoint: waypoint at the start of the leg
        :param to_waypoint: waypoint at the start of the leg
        :param distance: distance between waypoints in nautical miles
        :param true_course: true course in degrees
        :param true_airspeed: true airspeed in kts
        :param start_altitude: starting pressure altitude
        :param end_altitude: ending pressure altitude
        :param wind_direction: wind direction in degrees
        :param wind_speed: wind speed in kts
        :param temperature: outside temperature at waypoint (Celsius)
        :param mag_var: magentic variation in degrees
        """

        self.from_waypoint: Waypoint = from_waypoint
        self.to_waypoint: Waypoint = to_waypoint
        self.distance: float = distance
        self.true_course: float = true_course
        self.true_airspeed: float = true_airspeed
        self.start_altitude: float = start_altitude
        self.end_altitude: float = end_altitude
        self.wind_direction: float = wind_direction
        self.wind_speed: float = wind_speed
        self.temperature: float = temperature
        self.mag_var: float = mag_var
        self.mag_dev: float | None = None

        self.wca: float | None = None
        self.TC: float | None = None
        self.TH: float | None = None
        self.MH: float | None = None
        self.CH: float | None = None

        self.GS: float | None = None

        self.time_min: float | None = None
        self.remaining_time_min: float | None = None
        self.distance_nm: float | None = None
        self.remaining_distance_nm: float | None = None
        self.fuel_gal: float | None = None
        self.remaining_fuel_gal: float | None = None

    def evaluate(self, mag_dev: float, fuel_rate:float) -> None:
        """
        Computes
        :param mag_dev: magnetic deviation of aircraft in degrees.
        :param fuel_rate: aircraft fuel rate in GPH.
        :return:
        """
        self.mag_dev = mag_dev

        self.TC = self.true_course
        self.wca = compute_wca(self.true_course, self.true_airspeed, self.wind_direction, self.wind_speed)
        self.TH = self.TC + self.wca
        self.MH = self.TH + self.mag_var
        self.CH = self.MH + self.mag_dev

        self.GS = compute_gs(self.true_course, self.true_airspeed, self.wind_direction, self.wind_speed)
        self.distance_nm = self.distance
        self.time_min = self.distance_nm / self.GS * 60
        self.fuel_gal = fuel_rate / 60 * self.time_min

class Climb(Leg):
    def __init__(self,
                 from_waypoint: Waypoint,
                 to_waypoint: Waypoint,
                 distance: float,
                 true_course: float,
                 true_airspeed: float,
                 start_altitude: float,
                 end_altitude: float,
                 wind_direction: float,
                 wind_speed: float,
                 temperature: float,
                 mag_var: float) -> None:

        super().__init__(from_waypoint=from_waypoint,
                 to_waypoint=to_waypoint,
                 distance=distance,
                 true_course=true_course,
                 true_airspeed=true_airspeed,
                 start_altitude=start_altitude,
                 end_altitude=end_altitude,
                 wind_direction=wind_direction,
                 wind_speed=wind_speed,
                 temperature=temperature,
                 mag_var=mag_var)

        self.climb_time_min: float | None = None
        self.climb_distance_nm: float | None = None
        self.climb_fuel_gal: float | None = None


class Descend(Leg):
    def __init__(self,
                 from_waypoint: Waypoint,
                 to_waypoint: Waypoint,
                 distance: float,
                 true_course: float,
                 true_airspeed: float,
                 start_altitude: float,
                 end_altitude: float,
                 wind_direction: float,
                 wind_speed: float,
                 temperature: float,
                 mag_var: float) -> None:

        super().__init__(from_waypoint=from_waypoint,
                 to_waypoint=to_waypoint,
                 distance=distance,
                 true_course=true_course,
                 true_airspeed=true_airspeed,
                 start_altitude=start_altitude,
                 end_altitude=end_altitude,
                 wind_direction=wind_direction,
                 wind_speed=wind_speed,
                 temperature=temperature,
                 mag_var=mag_var)

        self.descend_time_min: float | None = None
        self.descend_distance_nm: float | None = None
        self.descend_fuel_gal: float | None = None


class Cruise(Leg):
    def __init__(self,
                 from_waypoint: Waypoint,
                 to_waypoint: Waypoint,
                 distance: float,
                 true_course: float,
                 true_airspeed: float,
                 altitude: float,
                 wind_direction: float,
                 wind_speed: float,
                 temperature: float,
                 mag_var: float) -> None:

        super().__init__(from_waypoint=from_waypoint,
                 to_waypoint=to_waypoint,
                 distance=distance,
                 true_course=true_course,
                 true_airspeed=true_airspeed,
                 start_altitude=altitude,
                 end_altitude=altitude,
                 wind_direction=wind_direction,
                 wind_speed=wind_speed,
                 temperature=temperature,
                 mag_var=mag_var)
