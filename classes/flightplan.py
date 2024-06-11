from classes.legs import Leg, Climb, Cruise, Descend
from classes.waypoints import Waypoint
from classes.aircraft import Aircraft


class FlightPlan:
    def __init__(self, plan: list[Leg], aircraft: Aircraft) -> None:
        self.plan: list[Leg] = plan
        self.aircraft: Aircraft = aircraft

        self.total_time = 0
        self.total_distance = 0
        self.total_fuel = 0

        is_valid, error_msg = self.check_plan()
        assert is_valid, error_msg

    def check_plan(self) -> tuple[bool, str | None]:
        """
        Checks to make sure the flight plan is valid. A flight plan is invalid if:
        1. It consists of less than one leg.

        :return: is_valid: True if the plan is valid, false otherwise
        :return: error_msg: returns a string describing the error if the flight plan is invalid, returns None otherwise
        """
        is_valid = True
        error_msg = None

        if len(self.plan) < 2:
            is_valid = False
            error_msg = "The flight plan must have at least two legs."

        return is_valid, error_msg

    def evaluate(self) -> None:
        """
        Updates the magnetic deviation and fuel usage in each leg and computes:
            1. TH: true heading
            2. WCA: wind correction angle
            3. MH: magnetic heading
            4. CH: compass heading
            5. GS: ground speed
            5. time: total, leg and remaining flight time (min)
            6. distance: total, leg and remaining distance (nm)
            7. fuel: total, leg and remaining fuel (gal)

        :return: None
        """
        for leg in self.plan:
            leg.evaluate(mag_dev=self.aircraft.compute_mag_dev(leg.true_course),
                         fuel_rate=self.aircraft.performance_profile['fuel_rate_gph'])

            self.total_time += leg.time_min
            self.total_distance += leg.distance_nm
            self.total_fuel += leg.fuel_gal

            if isinstance(leg, Climb):
                time, distance, fuel = self.aircraft.compute_climb(from_altitude=leg.start_altitude,
                                                                   to_altitude=leg.end_altitude,
                                                                   temperature=leg.temperature)
                leg.climb_time_min = time
                leg.climb_distance_nm = distance
                leg.climb_fuel_gal = fuel

            elif isinstance(leg, Descend):
                time, distance, fuel = self.aircraft.compute_descent(from_altitude=leg.start_altitude,
                                                                     to_altitude=leg.end_altitude,
                                                                     temperature=leg.temperature)
                leg.descend_time_min = time
                leg.descend_distance_nm = distance
                leg.descend_fuel_gal = fuel

        remaining_time_min = 0
        remaining_distance_nm = 0
        remaining_fuel_gal = 0

        # updating remaining time, distance, and fuel
        for i in reversed(range(len(self.plan))):
            self.plan[i].remaining_time_min = remaining_time_min
            self.plan[i].remaining_distance_nm = remaining_distance_nm
            self.plan[i].remaining_fuel_gal = remaining_fuel_gal

            remaining_time_min += self.plan[i].time_min
            remaining_distance_nm += self.plan[i].distance_nm
            remaining_fuel_gal += self.plan[i].fuel_gal

    def summarize(self) -> None:
        """
        Prints a summary of the flight plan.

        :return: None
        """
        assert self.total_time > 0, ("The total time must be greater than 0. Please make sure the flight plan is properly "
                                     "populated and FlightPlan.evaluate() has been called.")

        for i, leg in enumerate(self.plan):
            heading = f'{i+1}) -- {leg.from_waypoint.name} -> {leg.to_waypoint.name} '
            print(heading + '-' * (80 - len(heading)))

            print(f'\t TC: {leg.TC:.1f}, TH: {leg.TH:.1f}, MH: {leg.MH:.1f}, CH: {leg.CH:.1f}')

            if isinstance(leg, Climb) or isinstance(leg, Descend):
                print(f'\t Start Altitude: {leg.start_altitude} ft,  End Altitude: {leg.end_altitude} ft')
            else:
                print(f'\t Altitude: {leg.start_altitude} ft')

            print(f'\t Time: {leg.time_min:.1f} min,  Distance: {leg.distance_nm:.1f} nm,  Fuel: {leg.fuel_gal:.1f} gal')

            if isinstance(leg, Climb):
                print(f'\t Climb Time: {leg.climb_time_min:.1f} min,  Climb Distance: {leg.climb_distance_nm:.1f} nm,  Climb Fuel: {leg.climb_fuel_gal:.1f} gal')
            elif isinstance(leg, Descend):
                print(f'\t Descent Time: {leg.descend_time_min:.1f} min,  Descent Distance: {leg.descend_distance_nm:.1f} nm,  Descent Fuel: {leg.descend_fuel_gal:.1f} gal')

            print(f'\t Rem Time: {leg.remaining_time_min:.1f} min,  Rem Distance: {leg.remaining_distance_nm:.1f} nm,  Rem Fuel: {leg.remaining_fuel_gal:.1f} gal')
