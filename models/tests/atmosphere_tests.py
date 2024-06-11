import unittest
from models.atmosphere import atmospheric_model


TOLERANCE = 0.33


class TestAtmosphericModel(unittest.TestCase):
    """
    Tests to ensure that the atmosphere model reports values that make sense.
    """
    def test_atmospheric_model(self):
        test_cases = [
            {"temperature": 40, "pressure_alt": 1000, "expected": 0},
            {"temperature": 100, "pressure_alt": 4000, "expected": 15},
            {"temperature": -20, "pressure_alt": 8000, "expected": 9.1},
            {"temperature": 0, "pressure_alt": 6000, "expected": 6.8},
            {"temperature": 40, "pressure_alt": 5000, "expected": 9.8},
            {"temperature": 70, "pressure_alt": 5500, "expected": 15},
            {"temperature": 75, "pressure_alt": 3500, "expected": 10.5},
        ]

        for case in test_cases:
            with self.subTest(temperature=case["temperature"], pressure_alt=case["pressure_alt"]):
                result = atmospheric_model(case["temperature"], case["pressure_alt"])
                self.assertAlmostEqual(result, case["expected"], delta=TOLERANCE)


if __name__ == '__main__':
    unittest.main()
