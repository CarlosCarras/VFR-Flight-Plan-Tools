import numpy as np

MIN_TEMPERATURE: int = -20
MAX_TEMPERATURE: int = 100
MIN_PRESSURE_ALT: int = 0
MAX_PRESSURE_ALT: int = 14000

ATMOSPHERE = {
    0:     [-4.77789030473128e-05, 0.131506514026525, -7.59524602258745],
    1000:  [-0.000168903847283149, 0.147291357282320, -5.73114592306456],
    2000:  [-0.000200409786342505, 0.149400044755393, -3.08570618254692],
    3000:  [-0.000100544244567627, 0.139505165115918, -0.662380862929779],
    4000:  [-0.000146650458153391, 0.144739802376415, 1.75708697204559],
    5000:  [-9.42032264657786e-05, 0.139334845060707, 4.38481284445414],
    6000:  [-0.000113887586662117, 0.139711191546429, 6.96477970840780],
    7000:  [-0.000133990847596815, 0.140358772051931, 9.43321069866182],
    8000:  [-0.000127035370571325, 0.140177981168579, 11.9550501756149],
    9000:  [-0.000101368580681147, 0.137425118639429, 14.3901002923885],
    10000: [-0.000137241816574115, 0.139303160945327, 16.9023276004411],
    11000: [-9.46370417100963e-05, 0.134978469704705, 19.4369137861611],
    12000: [-7.26786923577127e-05, 0.135406864214044, 21.9018721893922],
    13000: [-0.000249597756546181, 0.136858875985431, 24.4818863403171],
    14000: [-0.000177501407124483, 0.139735658894387, 26.9913719349442],
}


def evaluate_atmospheric_model(temperature: float, pressure_alt: float) -> float:
    """
    Computes the y-axis performance value based on a temperature and pressure altitude. The pressure
    altitude MUST be in the ATMOSPHERE model. For interplation, use the atmospheric_model() function.
    See Piper Cherokee Archer II POH, Figure 5-11

    :param temperature: float = outside air temperature (F)
    :param pressure_alt: float = pressure altitude (ft)

    :return: performance: float = computed aircraft performance value. see POH for details
    """
    assert (pressure_alt >= MIN_PRESSURE_ALT) and (pressure_alt <= MAX_PRESSURE_ALT), \
        f"Pressure altitude must be between {MIN_PRESSURE_ALT} and {MAX_PRESSURE_ALT} ft."

    assert pressure_alt in ATMOSPHERE, \
        "Pressure altitude is not in the ATMOSPHERE model. Use the atmospheric_model() for interpolation."

    model: list = ATMOSPHERE[pressure_alt]
    performance: float = np.polyval(model, temperature)
    return performance


def atmospheric_model(temperature: float, pressure_alt: float) -> float:
    """
    Computes the y-axis performance value based on a temperature and pressure altitude.
    Model fit using cubic polynomial approximation.
    See Piper Cherokee Archer II POH, Figure 5-11

    :param temperature: float = outside air temperature (F)
    :param pressure_alt: float = pressure altitude (ft)

    :return: performance: float = computed aircraft performance value. see POH for details
    """

    assert (temperature >= MIN_TEMPERATURE) and (temperature <= MAX_TEMPERATURE), \
        f"Temperature must be between {MIN_TEMPERATURE} and {MAX_TEMPERATURE} degrees F."

    assert (pressure_alt >= MIN_PRESSURE_ALT) and (pressure_alt <= MAX_PRESSURE_ALT), \
        f"Pressure altitude must be between {MIN_PRESSURE_ALT} and {MAX_PRESSURE_ALT} ft."

    if pressure_alt % 1000 == 0:
        return evaluate_atmospheric_model(temperature, pressure_alt)

    # linear interpolation step
    lower_pressure_alt: int = np.floor(pressure_alt / 1000) * 1000
    upper_pressure_alt: int = np.ceil(pressure_alt / 1000) * 1000
    lower_performance = evaluate_atmospheric_model(temperature, lower_pressure_alt)
    upper_performance = evaluate_atmospheric_model(temperature, upper_pressure_alt)
    xp = np.array([lower_pressure_alt, upper_pressure_alt])
    fp = np.array([lower_performance, upper_performance])
    performance: float = np.interp(pressure_alt, xp, fp)

    return performance


if __name__ == "__main__":
    performance = atmospheric_model(100, 2000)
    print(performance)

