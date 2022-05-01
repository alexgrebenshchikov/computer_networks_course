class Statistics:

    def __init__(self):
        self.rtt_min = None
        self.rtt_max = None
        self.rtt_avg = 0
        self.total_count = 0
        self.response_count = 0
        self.no_response_count = 0

    def register_rtt(self, new_rtt):
        self.rtt_avg = (self.rtt_avg * self.total_count + new_rtt) / (self.total_count + 1)
        self.total_count += 1
        self.response_count += 1
        self.rtt_min = new_rtt if self.rtt_min is None else min(self.rtt_min, new_rtt)
        self.rtt_max = new_rtt if self.rtt_max is None else max(self.rtt_max, new_rtt)

    def register_missed(self):
        self.total_count += 1
        self.no_response_count += 1

    def print_statistics(self, address):
        rtt_avg, missed = 0, 0

        if self.total_count > 0:
            missed = self.no_response_count / self.total_count * 100
        print(f'''
Статистика Ping для {address}:
    Пакетов: отправлено = {self.total_count}, получено = {self.response_count}, потеряно = {self.no_response_count}
    ({int(missed)}% потерь)
Приблизительное время приема-передачи в мс:
    Минимальное = {"<нет>" if self.rtt_min is None else int(self.rtt_min)} мсек, Максимальное = {"<нет>" if self.rtt_max 
                                                                                                            is None else 
        int(self.rtt_max)} мсек, Среднее = {"<нет>" if self.rtt_max is None or self.rtt_min is None else int(self.rtt_avg)} мсек 
''')
