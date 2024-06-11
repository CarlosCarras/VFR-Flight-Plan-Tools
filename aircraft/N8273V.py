import numpy as np
from classes.aircraft import Aircraft


class N8273V(Aircraft):
    def __init__(self) -> None:
        mag_dev_lookup = {0: -1, 30: 0, 60: 0, 90: 1, 120: 1, 150: 2,
                          180: 1, 210: 1, 240: 0, 270: 1, 300: -1, 330: -1}

        performance_profile = {
            "climb_speed_kts": 76,
            "cruise_speed_kts": 115,
            "descend_speed_kts": 122,
            "fuel_capacity_g": 48,
            "fuel_rate_gph": 7.6,   # 65% power
            "mag_dev_lookup": mag_dev_lookup
        }

        super().__init__(category="Airplane",
                         class_="SEI",
                         type="PA-28-181",
                         callsign="N8273V",
                         performance_profile=performance_profile)

        self.time_to_climb_model = np.array([2.87877650796108e-06, -0.000144802420551403, 0.00342898366361228, -0.0107917301934256, 0.634422192936824, -0.0186154940652254])
        self.distance_to_climb_model = np.array([4.42959545765142e-06, -0.000163476059542869, 0.00231669831047607, 0.0252978983345908, 0.678065767832256, -0.0732483197801467])
        self.fuel_to_climb_model = np.array([-1.94926996262817e-06, 0.000145480319823401, -0.00369494915915234, 0.0429170270715064, -0.0192274749207769, -0.0198608173346909])
        self.time_to_descend_model = np.array([-1.58341002886778e-06, 0.000108753346616133, -0.00206982222787217, -0.0214951101376967, 1.68166975233790, -0.00660865289312827])
        self.distance_to_descend_model = np.array([-1.29865755740527e-06, 5.78201345323594e-05, 0.00120320011417074, -0.121296457837932, 3.87191245881648, 0.181102740447271])
        self.fuel_to_descend_model = np.array([1.19726058053013e-07, -1.36088862232907e-06, -0.000200535974443365, 0.00344771825995696, 0.0981893803146724, 0.0140448819097330])


if __name__ == "__main__":
    aircraft = N8273V()

    heading = 151
    mag_dev = aircraft.compute_mag_dev(heading)

    print(f"For a heading of {heading}, the magnetic deviation correction angle is {mag_dev}")