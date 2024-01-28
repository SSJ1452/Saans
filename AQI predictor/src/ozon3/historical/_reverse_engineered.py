import json
from datetime import datetime
from typing import Any, Dict, List

import js2py
import pandas
import requests
from sseclient import SSEClient

from .relevant_funcs import JS_FUNCS



_context = js2py.EvalJs()
_context.execute(JS_FUNCS)


def get_results_from_backend(city_id: int) -> List[Dict[str, Any]]:
    event_data_url = f"https://api.waqi.info/api/attsse/{city_id}/yd.json"

    r = requests.get(event_data_url)

    if "text/event-stream" not in r.headers["Content-Type"]:
        raise Exception(
            "Server does not return data stream. "
            f'It is likely that city ID "{city_id}" does not exist.'
        )

    client = SSEClient(r)
    result = []

    for event in client.events():
        if event.event == "done":
            break

        try:
            if "msg" in event.data:
                result.append(json.loads(event.data))
        except json.JSONDecodeError:
            pass

    return result


def parse_incoming_result(json_object: dict) -> pandas.DataFrame:
    
    OUTPUT = _context.gatekeep_convert_date_object_to_unix_seconds(
        json_object["msg"]
    ).to_dict()

    result_dict = {}
    for spec in OUTPUT["species"]:
        pollutant_name: str = spec["pol"]

        dates, values = [], []
        for step in spec["values"]:
         
            date = datetime.fromtimestamp(step["t"]["d"])
            value: int = step["v"]

            dates.append(date)
            values.append(value)

        series = pandas.Series(values, index=dates)
        result_dict[pollutant_name] = series

    FRAME = pandas.DataFrame(result_dict)
    return FRAME


def get_data_from_id(city_id: int) -> pandas.DataFrame:
    backend_data = get_results_from_backend(city_id)
    result = pandas.concat([parse_incoming_result(data) for data in backend_data])

    result = result.sort_index(ascending=False, na_position="last")


    result = result[~result.index.duplicated()]

    
    if len(result) > 1:
        complete_days = pandas.date_range(
            result.index.min(), result.index.max(), freq="D"
        )
        result = result.reindex(complete_days, fill_value=None)

  
        result = result.sort_index(ascending=False, na_position="last")

    return result


if __name__ == "__main__":
    pass
