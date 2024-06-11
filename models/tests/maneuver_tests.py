import unittest
from aircraft.N8273V import N8273V


aircraft = N8273V()
FUEL_TOLERANCE_GAL = 0.25
DISTANCE_TOLERANCE_NM = 1
TIME_TOLERANCE_MIN = 1


class TestManeuvers(unittest.TestCase):
    """
    Tests to ensure that the climb and descent models work correctly.
    """
    def test_climb_model(self):
        test_cases = [
            {
                "temperature": 70,
                "from_altitude": 1000,
                "to_altitude": 5500,
                "expected_time": 11.5,
                "expected_distance": 16,
                "expected_fuel": 2.5
            },
        ]

        for case in test_cases:
            with self.subTest(from_pressure=case["from_altitude"], to_pressure=case["to_altitude"], temperature=case["temperature"]):
                result_time, result_distance, result_fuel = aircraft.compute_climb(case["from_altitude"], case["to_altitude"], case["temperature"])
                self.assertAlmostEqual(result_time, case["expected_time"], delta=TIME_TOLERANCE_MIN)
                self.assertAlmostEqual(result_distance, case["expected_distance"], delta=DISTANCE_TOLERANCE_NM)
                self.assertAlmostEqual(result_fuel, case["expected_fuel"], delta=FUEL_TOLERANCE_GAL)


    def test_descent_model(self):
        test_cases = [
            {
                "temperature": 73.4,
                "from_altitude": 5500,
                "to_altitude": 1000,
                "expected_time": 11,
                "expected_distance": 23.5,
                "expected_fuel": 1.25
            },
        ]

        for case in test_cases:
            with self.subTest(from_altitude=case["from_altitude"], to_altitude=case["to_altitude"], temperature=case["temperature"]):
                result_time, result_distance, result_fuel = aircraft.compute_descent(case["from_altitude"], case["to_altitude"], case["temperature"])
                self.assertAlmostEqual(result_time, case["expected_time"], delta=TIME_TOLERANCE_MIN)
                self.assertAlmostEqual(result_distance, case["expected_distance"], delta=DISTANCE_TOLERANCE_NM)
                self.assertAlmostEqual(result_fuel, case["expected_fuel"], delta=FUEL_TOLERANCE_GAL)


if __name__ == '__main__':
    unittest.main()
