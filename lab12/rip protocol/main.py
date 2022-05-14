import json
from rip import Rip

json_file_path = 'config.json'


def json_2_rip(json_data):
    rip = Rip()
    for element in json_data:
        rip.add_edge(element['src'], element['dest'])
    return rip



if __name__ == "__main__":
    with open(json_file_path) as json_d:
        data = json.load(json_d)
        rip = json_2_rip(data)
        rip.start()