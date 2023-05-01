import io

import re

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class ReadAndWrite:
    def __extract_text_by_page(pdf_path):
        '''Тут описывать нечего, код взят с просторов интернета. Получаем данные с PDF.
        Автор не разбирался в работе данного блока'''

        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()

    def __extract_text(pdf_path):
        '''небольшой костыль, что б обрабатывать только страничку с примером логов
        и пропустить описание задания'''

        page = [page for page in ReadAndWrite.__extract_text_by_page(
            pdf_path)]  # небольшой генератор для последующего ретерна только второй странички
        return page[1]

    @staticmethod
    def write_log():
        '''Запись полученных данных в файл с форматом .txt'''

        pattern = r"blocked=(Y|N)"
        log = ReadAndWrite.__extract_text(
            'Анализ лог-файла.pdf').split()  # вызываем наш костыль и сплитим данные для последующей обработки

        with open('log', 'w') as f:
            for i in log:
                if re.search(pattern, i):
                    f.write(f'{i[:9]}\n{i[9:]} ')  # разбиваем строку и вставляем спецсимвол для корректной записи в лог
                else:
                    f.write(i + ' ')  # если строка не соотвествует паттерну - пишем как есть


ReadAndWrite.write_log()
