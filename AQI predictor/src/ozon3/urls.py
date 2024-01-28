
from dataclasses import dataclass


@dataclass(frozen=True)
class URLs:
  


    _base_url: str = "https://api.waqi.info/"


    search_aqi_url: str = f"{_base_url}feed/"


    find_stations_url: str = f"{_base_url}search/"

    find_coordinates_url: str = f"{_base_url}map/"


if __name__ == "__main__":
    pass
