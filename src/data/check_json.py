import json

def check():
    with open('./json/DXYNews-TimeSeries.json', 'r') as file:
        data = json.load(file)
    print("\tRead {} lines from file".format(len(data)))
    mark = []

