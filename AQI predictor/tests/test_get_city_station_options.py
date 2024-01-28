import pandas
import pandas.api.types as pd_types
import pytest

from utils import api


@pytest.mark.vcr
def test_return_value_and_format():
    result = api.get_city_station_options("ukraine")
    assert isinstance(result, pandas.DataFrame)
    assert len(result) > 0 


@pytest.mark.vcr
def test_columns():
    result = api.get_city_station_options("ukraine")

    COLUMNS = ["city_id", "country_code", "station_name", "city_url", "score"]
    assert all([col in result for col in COLUMNS])


@pytest.mark.vcr
def test_score_column():
    result = api.get_city_station_options("ukraine")

    assert pd_types.is_numeric_dtype(result["score"])

    score = result["score"].tolist()
    assert score == sorted(score, reverse=True)


@pytest.mark.vcr
def test_nonexistent_city():

    result = api.get_city_station_options("gibberish_nonexistent_place_name")

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 0

    COLUMNS = ["city_id", "country_code", "station_name", "city_url", "score"]
    assert all([col in result for col in COLUMNS])
