import requests
import json

from get_date import get_date_now, get_date_14
from get_tokens import headers_OZON
from dict_status_OZON import status_OZON


def _get_zakaz_OZON():  # полуние JSON ОТ API OZON
    try:
        body = {  # запроса к API OZON
            "dir": "ASC",
            "filter": {
                "since": f"{get_date_14()}T23:59:59Z",
                "status": "",
                "to": f"{get_date_now()}T23:59:59Z",
            },
            "limit": 1000,
            "offset": 0,
            "translit": True,
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }
        rinquiry = requests.post(
            'https://api-seller.ozon.ru/v3/posting/fbs/list',
            json=body,
            headers=headers_OZON,
        ).json()
        with open("product_OZON.json", "w", encoding="utf_8") as file_create:
            json.dump(rinquiry, file_create, indent=4, ensure_ascii=False)
        return rinquiry
    except Exception:
        return "Ошибка запроса к API OZON"


# полуние JSON ОТ API OZON огарничений на складах
def _get_posting_number(data):
    # Ограничение по максимальному весу в граммах.
    posting_number1 = []
    # Ограничение по ширине в сантиметрах.
    posting_number2 = []
    # Ограничение по длине в сантиметрах.
    posting_number3 = []
    # Ограничение по высоте в сантиметрах.
    posting_number4 = []
    # Ограничение по максимальной стоимости отправления в рублях.
    posting_number5 = []
    for item in data:
        body = {
            "posting_number": f"{item}"
        }
        rinquiry = requests.post('https://api-seller.ozon.ru/v1/posting/fbs/restrictions',
                                 json=body, headers=headers_OZON).json()  # url запроса
        posting_number1.append(rinquiry["result"]["max_posting_weight"])
        posting_number2.append(rinquiry["result"]["width"])
        posting_number3.append(rinquiry["result"]["height"])
        posting_number4.append(rinquiry["result"]["length"])
        posting_number5.append(rinquiry["result"]["max_posting_price"])
    return [posting_number1, posting_number2,
            posting_number3, posting_number4,
            posting_number5]


def pars_date_OZON():
    try:
        rinquiry = _get_zakaz_OZON()
        list_date_obrabotki = []
        list_namber_otpravki = []
        list_status = []
        list_date_dostavki = []
        list_sostav = []
        list_sostav_name = []
        list_price = []
        list_sklad = []
        list_metod_dostavki = []
        list_sku = []
        for item in rinquiry["result"]["postings"]:
            date_obrabotki = item["in_process_at"].split("T")
            date_obrabotki_0 = date_obrabotki[0].split("-")
            date_obrabotki_1 = date_obrabotki[1].split(":")
            list_date_obrabotki.append(
                f"{date_obrabotki_0[2]}.{date_obrabotki_0[1]}.{date_obrabotki_0[0]} {date_obrabotki_1[0]}:{date_obrabotki_1[1]}")
            list_namber_otpravki.append(item["posting_number"])
            list_status.append(status_OZON[item["status"]])
            if item["shipment_date"] is None:
                list_date_dostavki.append(
                    "Не передан в доставку")
            else:
                date_dostavki = item["shipment_date"].split("T")
                date_dostavki_0 = date_dostavki[0].split("-")
                date_dostavki_1 = date_dostavki[1].split(":")
                list_date_dostavki.append(
                    f"{date_dostavki_0[2]}.{date_dostavki_0[1]}.{date_dostavki_0[0]} {date_dostavki_1[0]}:{date_dostavki_1[1]}")
            time_list_sostav = []
            time_list_sostav_name = []
            time_list_peice = []
            time_list_sku = []
            for item_name in item["products"]:
                time_list_sostav.append(
                    f"{item_name['offer_id']}, {item_name['quantity']} шт.")
                time_list_sostav_name.append(item_name['name'])
                time_list_peice.append(float(item_name["price"]))
                time_list_sku.append(item_name["sku"])
            list_sku.append(time_list_sku)
            list_sostav.append(time_list_sostav)
            list_sostav_name.append(time_list_sostav_name)
            list_price.append(f"{int(sum(time_list_peice))} ₽")
            list_sklad.append(item["delivery_method"]["warehouse"])
            list_metod_dostavki.append(
                f"{item['delivery_method']['tpl_provider']} {item['delivery_method']['name']}")
        posting_number = _get_posting_number(list_namber_otpravki)
        return [list_date_obrabotki, list_namber_otpravki,
                list_status, list_date_dostavki, list_sostav,
                list_sostav_name, list_price, list_sklad,
                list_metod_dostavki, list_sku, posting_number]
    except Exception:
        list_date_obrabotki = [1]
        list_namber_otpravki = [1]
        list_status = ["Заказов нет"]
        return [list_date_obrabotki, list_namber_otpravki,
                list_status]


def send_request(data):
    body = {
        "posting_number": f"{data}",
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "product_exemplars": True,
            "translit": True
        }
    }
    rinquiry = requests.post(
        'https://api-seller.ozon.ru/v3/posting/fbs/get', json=body, headers=headers_OZON).json()
    # with open("product_OZON555.json", "w", encoding="utf_8") as file_create:
    #     json.dump(rinquiry, file_create, indent=4, ensure_ascii=False)
    list_data = []
    for item in rinquiry["result"]["products"]:
        bod = {
            "product_id": item["sku"],
            "quantity": item["quantity"]
        }
        list_data.append(bod)
    body_1 = {
        "packages": [
            {
                "products": list_data
            }
        ],
        "posting_number": f"{data}",
        "with": {
            "additional_data": True
        }
    }
    rinquiry_1 = requests.post('https://api-seller.ozon.ru/v4/posting/fbs/ship', json=body_1, headers=headers_OZON).json()
    


if __name__ == "__main__":
    pars_date_OZON()
