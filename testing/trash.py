import json
import requests

from google.protobuf.json_format import MessageToJson
from proto_structs import offers_pb2

def parse_page(city = "moskva", shop = "5ka", page_num = 1):
    """
    :param city: location of the shop
    :param shop: shop name
    :param page_num: parsed page number
    :return: None
    """
    url = f"https://squark.edadeal.ru/web/search/offers?count=30&locality={city}&page={page_num}&retailer={shop}"
    data = requests.get(url, allow_redirects=True)  # data.content is a protobuf message

    offers = offers_pb2.Offers()  # protobuf structure
    offers.ParseFromString(data.content)  # parse binary data
    products: str = MessageToJson(offers)  # convert protobuf message to json
    products = json.loads(products)
    print(json.dumps(products, indent=4, ensure_ascii=False,))

if __name__ == "_







