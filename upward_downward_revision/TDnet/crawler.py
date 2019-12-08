from datetime import datetime
import json
import requests
import pandas as pd


TDNET_JSON_URL_FMT = 'https://webapi.yanoshin.jp/webapi/tdnet/list/{start}-{end}.json'
# ex. https://webapi.yanoshin.jp/webapi/tdnet/list/20191204-20191209.json


def fetch_company_announcements(
    start: datetime,
    end: datetime,
):
    """fetch comapny announcements data via TDnet API

    Args:
        start (datetime): Start date of data to fetch
        end (datetime): End date of data to fetch

    Returns:
        res (dict): response dict
    """
    res = requests.get(
        TDNET_JSON_URL_FMT.format(
            start=start.strftime('%Y%m%d'),
            end=end.strftime('%Y%m%d')
        )
    )

    return res.json()


def parse_tdnet_json_response(res_json):
    return res['items']


def filter_updown_revison(parsed_data):
    """業績予想修正の開示情報のみ取り出す
    """
    return [d['Tdnet'] for d in parsed_data if '業績予想' in d['Tdnet']['title']]


if __name__ == '__main__':
    start = datetime(2019, 12, 1)
    end = datetime(2019, 12, 3)

    res = fetch_company_announcements(
        start, end
    )
    parsed_data = parse_tdnet_json_response(res)
    print(parsed_data)
    json.dump(
        parsed_data,
        open(f'raw_json_{start.strftime("%Y%m%d")}_{end.strftime("%Y%m%d")}', 'w')
    )
    updown_infos = filter_updown_revison(parsed_data)
    print(updown_infos)
    df_updown_infos = pd.DataFrame.from_records(
        updown_infos,
        index=None
    )
    print(df_updown_infos)

    df_updown_infos.to_csv(
        f'sample_data_{start.strftime("%Y%m%d")}_{end.strftime("%Y%m%d")}.csv',
        index=None
    )

    print(len(parsed_data))
