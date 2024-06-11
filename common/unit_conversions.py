def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Converts temperature from Celcius to Fahrenheit.

    :param celsius: temperature in Celsius.
    :return: fahrenheit: temperature in Fahrenheit.
    """
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit


def nm_to_sm(nm: float) -> float:
    """
    Converts nautical miles to statute miles.

    :param nm: statute miles.
    :return: sm: nautical miles.
    """

    sm = nm * 1.15078
    return sm
