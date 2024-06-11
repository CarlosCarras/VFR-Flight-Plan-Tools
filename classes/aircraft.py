import numpy as np
from models.atmosphere import atmospheric_model

class Aircraft:
    """
    Generic aircraft class.
    """
    def __init__(self, category: str, class_: str, type: str, callsign: str, performance_profile: dict) -> None:
        """
        Constructor.

        :param category: aircraft category (e.g., airplane, etc.)
        :param class_: aircraft class (e.g., SEL, MEL, etc.)
        :param type: aircraft type (e.g., PA-28-181, C172, etc.)
        :param callsign: aircraft call sign
        :param performance_profile: a dictionary containing the aircraft's performance profile
        """
        self.category: str = category
        self.class_: str = class_
        self.type: str = type
        self.callsign: str = callsign
        self.performance_profile: dict = performance_profile

        self.time_to_climb_model: np.ndarray | None = None
        self.distance_to_climb_model: np.ndarray | None = None
        self.fuel_to_climb_model: np.ndarray | None = None
        self.time_to_descend_model: np.ndarray | None = None
        self.distance_to_descend_model: np.ndarray | None = None
        self.fuel_to_descend_model: np.ndarray | None = None

    def compute_mag_dev(self, heading: float) -> float:
        """
        Compute the magnetic deviation for a given heading.
        The performance profile must have an entry called "mag_dev_lookup". The mag_dev_lookup entry must be a
        dictionary structures as a table of magentic deviations in degrees.
        e.g., "mag_dev_lookup": {0: -1, 30: 0, 60: 1, ...}

        :param heading: the magnetic heading in degrees.
        :return: the magnetic deviation correction angle in degrees.
        """
        assert "mag_dev_lookup" in self.performance_profile.keys(), \
            "Performance profile is missing the mag_dev_lookup() dictionary."
        assert isinstance(self.performance_profile["mag_dev_lookup"], dict), \
            "mag_dev_lookup must be a dictionary."

        true_headings = np.fromiter(self.performance_profile["mag_dev_lookup"].keys(), dtype=float)
        corrections = np.fromiter(self.performance_profile["mag_dev_lookup"].values(), dtype=float)

        closest_heading_index = (np.abs(true_headings - heading)).argmin()
        return corrections[closest_heading_index]

    def compute_climb(self, from_altitude: float, to_altitude: float, temperature: float):
        """
        Computes the time, distance, and fuel to climb performance based on a temperature and pressure
        altitude.

        :param from_altitude: float = outside pressure altitude (ft)
        :param to_altitude: float = desired pressure altitude (ft) [must be > pressure_alt]
        :param temperature: float = outside air temperature (F)
        :return: time: float = time to climb to the desired pressure altitude (min)
        :return: distance: float = distance to climb to the desired pressure altitude (nautical miles)
        :return: fuel: float = fuel to climb to the desired pressure altitude (gal)
        """
        assert from_altitude < to_altitude, f"from_altitude must be less than the to_altitude. Use compute_descent() otherwise."
        assert self.time_to_climb_model is not None, "Must have a time to climb model for this aircraft."
        assert self.distance_to_climb_model is not None, "Must have a distance to climb model for this aircraft."
        assert self.fuel_to_climb_model is not None, "Must have a fuel to climb model for this aircraft."

        performance = atmospheric_model(temperature=temperature, pressure_alt=to_altitude)

        time: float = np.polyval(self.time_to_climb_model, performance)
        distance: float = np.polyval(self.distance_to_climb_model, performance)
        fuel: float = np.polyval(self.fuel_to_climb_model, performance)

        reference_performance = atmospheric_model(temperature=temperature, pressure_alt=from_altitude)

        reference_time: float = np.polyval(self.time_to_climb_model, reference_performance)
        reference_distance: float = np.polyval(self.distance_to_climb_model, reference_performance)
        reference_fuel: float = np.polyval(self.fuel_to_climb_model, reference_performance)

        time -= reference_time
        distance -= reference_distance
        fuel -= reference_fuel

        return time, distance, fuel

    def compute_descent(self, from_altitude: float, to_altitude: float, temperature: float):
        """
        Computes the time, distance, and fuel to descend performance based on a temperature and pressure
        altitude.

        :param from_altitude: float = outside pressure altitude (ft)
        :param to_altitude: float = desired pressure altitude (ft) [must be > pressure_alt]
        :param temperature: float = outside air temperature (F)

        :return: time: float = time to descend to the desired pressure altitude (min)
        :return: distance: float = distance to descend to the desired pressure altitude (nautical miles)
        :return: fuel: float = fuel to descend to the desired pressure altitude (gal)
        """
        assert self.time_to_descend_model is not None, "Must have a time to descend model for this aircraft."
        assert self.distance_to_descend_model is not None, "Must have a distance to descend model for this aircraft."
        assert self.fuel_to_descend_model is not None, "Must have a fuel to descend model for this aircraft."

        performance = atmospheric_model(temperature=temperature, pressure_alt=to_altitude)
        reference_performance = atmospheric_model(temperature=temperature, pressure_alt=from_altitude)

        time: float = np.polyval(self.time_to_descend_model, performance)
        distance: float = np.polyval(self.distance_to_descend_model, performance)
        fuel: float = np.polyval(self.fuel_to_descend_model, performance)

        reference_time: float = np.polyval(self.time_to_descend_model, reference_performance)
        reference_distance: float = np.polyval(self.distance_to_descend_model, reference_performance)
        reference_fuel: float = np.polyval(self.fuel_to_descend_model, reference_performance)

        time = reference_time - time
        distance = reference_distance - distance
        fuel = reference_fuel - fuel

        return time, distance, fuel
