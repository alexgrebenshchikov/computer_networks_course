class DistanceList:
    INF = 10 ** 9 + 7

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return DistanceList.INF

    def __setitem__(self, key, value):
        if value < DistanceList.INF:
            self.data[key] = value

    def __str__(self):
        return '{' + ', '.join(
            f"'{key}': {self.data[key]}"
            for key in sorted(self.data.keys())
        ) + '}'

    def update_item(self, key, value):
        if value >= DistanceList.INF:
            return False
        if key not in self.data or value < self.data[key]:
            self.data[key] = value
            return True
        return False

    def update_dist_list(self, other_data):
        other_data = {
            key: value
            for key, value in other_data.items()
            if value < DistanceList.INF
        }
        self.data = other_data
