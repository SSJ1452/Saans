import pandas
import pandas.api.types as pd_types
import pytest

from utils import api




@pytest.mark.vcr
def test_return_value_and_format():
  
    result = api.get_city_forecast("london")

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 7


@pytest.mark.vcr
def test_column_types():
    result = api.get_city_forecast("london")

    assert pd_types.is_datetime64_any_dtype(result["date"])

    for param in ["pm2.5", "pm10", "o3", "uvi"]:
        for stat in ["min", "max", "avg"]:
            assert pd_types.is_float_dtype(result[(param, stat)])


@pytest.mark.vcr
def test_bad_city_input():
  
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_city_forecast("a definitely nonexistent city")

    with pytest.raises(Exception):
        api.get_city_forecast("")
