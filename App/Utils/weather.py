from client import fetch


def getWeather(options):
    res = fetch(
        "https://api.open-meteo.com/v1/forecast?latitude="
        + options.latitude
        + "&longitude="
        + options.longitude
        + "14.51&hourly=temperature_2m",
        None,
    )
    print(res)
