import requests
import json

from get_date import get_date_now, get_date_14
from get_tokens import headers_OZON
from dict_status_OZON import status_OZON

def test():
    body =  {
            "dir": "ASC",
            "filter": {
                "since": f"{get_date_14()}T23:59:59Z",
                "status": "",
                "to": f"{get_date_now()}T23:59:59Z",
            },
            "limit": 100,
            "offset": 0,
            "translit": True,
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }
    rinquiry = requests.post('https://api-seller.ozon.ru/v3/posting/fbs/list', json=body, headers=headers_OZON).json()
    with open("zakazi_OZON_10.json", "w", encoding="utf_8") as file_create:
        json.dump(rinquiry, file_create, indent=4, ensure_ascii=False)

if __name__=="__main__":
    test()