class Analiz_log:
    @classmethod
    def __get_even(cls):
        '''Получение строк из лога. В ней же сплитуем строку для последущей обработки по индексам
        Также проверяем на пустоту(пустые строки не обрабатываем)'''
        with open('log', 'r') as f:
            for i in f:
                i = i.split()
                if len(i) != 0:
                    yield i

    @staticmethod
    def __average_message_volume_per_day():
        '''Получение объем сообщений в Мб, обработанных системой по дням'''
        dct = {}
        for i in Analiz_log.__get_even():
            if i[0] in dct:
                dct[i[0]].append(int(i[14].split('=')[1]))
            else:
                dct.setdefault(i[0], [int(i[14].split('=')[1])])
        for key, value in dct.items():
            print(f'За {key} объём полученных сообщений: {sum(value) // 1024} Мб')

    @staticmethod
    def __average_processing_time():
        '''Получение среднее время обработки сообщений в секундах по дням'''
        dct = {}
        for i in Analiz_log.__get_even():
            if i[0] in dct:
                dct[i[0]].append(int(i[12].split('=')[1]))
            else:
                dct.setdefault(i[0], [int(i[12].split('=')[1])])
        for key, value in dct.items():
            print(f'За {key} среднее время обюработки сообщений: {round(sum(value) / len(value) / 1000, 1)} сек')

    @staticmethod
    def __messeage_notsend_notarchived():
        '''Получение суммарное количество сообщений, которые не были заархивированы и отправлены'''
        count = 0
        for i in Analiz_log.__get_even():
            if i[10].split('=')[1] == 'N':
                if i[11].split('=')[1] == 'N':
                    count += 1
        print(f'Cуммарное количество сообщений, которые не были заархивированы и отправлены: {count}')

    @staticmethod
    def __message_archived_send():
        '''Получение суммарное количество сообщений, которые были заархивированы и заблокированы'''
        count = 0
        for i in Analiz_log.__get_even():
            if i[11].split('=')[1] == 'Y':
                if i[10].split('=')[1] == 'Y':
                    count += 1
        print(f'Cуммарное количество сообщений, которые были заархивированы и заблокированы: {count}')

    @staticmethod
    def __count_event():
        '''Получение количество событий, которые были созданы системой, за весь период лога'''
        count = 0
        for i in Analiz_log.__get_even():
            count += 1
        print(f'Количество событий, которые были созданы системой, за весь период лога: {count}')

    @staticmethod
    def __average_volume_messages_average_processing_time():
        '''Получение средний объем сообщений и среднее время обработки сообщений, которые пришли с адреса test@ya.ru'''
        average_volume_messages = []
        average_processing_time = []
        count_mail = 0
        for i in Analiz_log.__get_even():
            if (i[7]) == 'test@ya.ru':
                average_volume_messages.append(int(i[-4].split('=')[1]))
                average_processing_time.append(int(i[-6].split('=')[1]))
                count_mail += 1
        print(
            f'Средний объем сообщений , которые пришли с адреса test@ya.ru: {sum(average_volume_messages) // count_mail // 1024} мб')
        print(
            f'Среднее время обработки сообщений, которые пришли с адреса test@ya.ru: {sum(average_processing_time) // count_mail // 1000} сек')

    @staticmethod
    def call_all_func():
        '''Вызов всех приватных функций'''
        Analiz_log.__average_message_volume_per_day()
        Analiz_log.__average_processing_time()
        Analiz_log.__messeage_notsend_notarchived()
        Analiz_log.__message_archived_send()
        Analiz_log.__count_event()
        Analiz_log.__average_volume_messages_average_processing_time()



Analiz_log.call_all_func()
