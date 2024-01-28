import numpy
import pandas
import pandas.api.types as pd_types
import pytest

from utils import api


@pytest.mark.vcr
def test_return_value_and_format():

    result = api.get_coordinate_air(51.51, -0.13)


    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 1


@pytest.mark.vcr
def test_column_expected_contents():
    result = api.get_coordinate_air(51.51, -0.13)

    assert numpy.isnan(result.at[0, "city"]) 
    assert result.at[0, "station"] == "London"  

    # London's coordinates
    assert result.at[0, "latitude"] == pytest.approx(51.507351)
    assert result.at[0, "longitude"] == pytest.approx(-0.1277583)


@pytest.mark.vcr
def test_column_types():
    result = api.get_coordinate_air(51.51, -0.13)
    STR_COLUMNS = [
        "dominant_pollutant",
        "AQI_meaning",
        "AQI_health_implications",
        "timestamp",
        "timestamp_timezone",
    ]
    FLOAT_COLUMNS = [
        "latitude",
        "longitude",
        "aqi",
        "pm2.5",
        "pm10",
        "o3",
        "co",
        "no2",
        "so2",
        "dew",
        "h",
        "p",
        "t",
        "w",
        "wg",
    ]
    assert all([pd_types.is_string_dtype(result[col]) for col in STR_COLUMNS])
    assert all([pd_types.is_float_dtype(result[col]) for col in FLOAT_COLUMNS])


@pytest.mark.vcr
def test_bad_coordinates():
    with pytest.raises(Exception, match="Invalid geo position"):
        api.get_coordinate_air("not a lat", "not a lon")  

    with pytest.raises(Exception, match="Invalid geo position"):
        api.get_coordinate_air(None, None)  


    api.get_coordinate_air("51.51", "-0.13")  

    api.get_coordinate_air(5000, 5000)
    api.get_coordinate_air(-5000, -5000)

    api.get_coordinate_air(numpy.nan, numpy.nan)
