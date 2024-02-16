import json
import math
import os
import re


class Member:
    """
    Описывает контакт в справочнике.
    """

    def __init__(self, name: str, last_name: str, surname: str, name_company: str, work_number: str,
                 member_phone: str, pk=None):
        """
        Инициализация контакта.

        :param name: Имя.
        :param last_name: Фамилия.
        :param surname: Отчество.
        :param name_company: Название компании.
        :param work_number: Рабочий номер.
        :param member_phone: Личный номер.
        :param pk: Уникальный идентификатор контакта.
        """

        self.name = name
        self.last_name = last_name
        self.surname = surname
        self.name_company = name_company
        self.work_number = work_number
        self.member_phone = member_phone
        self.pk = pk


class PhoneBook:
    """
    Описывает справочник.
    """

    @staticmethod
    def open_file() -> list[dict[str, str]]:
        """
        Загружает данные из файла возвращает в виде списка
        """
        with open('phonemembers.json', 'r') as file:
            values = json.load(file)
        return values

    @staticmethod
    def close_file(values: list[dict]) -> None:
        """
        Записывает новые данные в файл json.
        :param values:.
        :return: None
        """
        with open('phonemembers.json', 'w', encoding='utf-8') as file:
            json.dump(values, file, indent=2, ensure_ascii=False)

    def edit_member(self, criteria: str, target: int, new_data) -> None:
        """
        Изменяет данные о контакте в телефонном справочнике.

        :param criteria: Атрибут для изменения.
        :param target: Индекс контакта для изменения.
        :param new_data: Новое значение для указанного атрибута.
        :return: None
        """

        values = self.open_file()

        if self.validate({criteria: new_data}):
            print('Данные успешно изменены!')
            values[int(target) - 1][criteria] = new_data

        self.close_file(values)

    def add_member(self, member: Member) -> None:
        """
        Добавляет новый контакт в справочник.

        :param member: Экземпляр класса Member.
        :return: None
        """
        total_entries = 0
        if os.path.exists('phonemembers.json'):
            values = self.open_file()
        else:
            values = []

        total_entries += len(values) + 1
        member.pk = total_entries
        values.append(member.__dict__)

        self.close_file(values)

    def get_page(self, page: int) -> None:
        """
        Выводит постранично записи из справочника.

        :param page: Номер страницы.
        :return: None
        """

        values = self.open_file()
        if len(values) >= ((page - 1) * 5):
            start = (page - 1) * 5
            end = page * 5
            for data in values[start:end]:
                print(data)
        else:
            print(f'СТРАНИЦА "{page}" НЕ НАЙДЕНА!')

    def binary_search_member(self, val: str, target: str) -> None:
        """
        Выполняет бинарный поиск по одной из характеристик.

        :param val: Характеристика.
        :param target: Значение, которое найти.
        :return: None
        """

        values = self.open_file()
        sorted_data = sorted(values, key=lambda x: str(x[val]))

        low, high = 0, len(sorted_data) - 1
        found = False

        while low <= high:
            mid = (low + high) // 2
            mid_name = sorted_data[mid]

            if str(mid_name[val]) == target:
                found = True
                print(mid_name)
                left = mid - 1
                while left >= 0 and str(sorted_data[left][val]) == target:
                    print(sorted_data[left])
                    left -= 1

                right = mid + 1
                while right < len(sorted_data) and str(
                        sorted_data[right][val]) == target:
                    print(sorted_data[right])
                    right += 1
                break
            elif str(mid_name[val]) < target:
                low = mid + 1
            else:
                high = mid - 1

        if not found:
            print("Запись не найдена.")

    @staticmethod
    def validate(member_data: dict[str, str]) -> bool:
        """
        Валидация данных при создании ЭК
        :param member_data:
        :return: bool значение True/False
        """

        for key, value in member_data.items():
            if key in ('name', 'last_name', 'surname', 'name_company'):
                if not value.strip():
                    print(f'Некорректные данные {key} {value}')
                    return False
            elif key in ['work_number', 'member_phone']:
                if not re.match(r'^8.{10}$', value):
                    print(f'Некорректные данные: номер телефона {value} введите в формате 8-ХХХХХХХХХХ')
                    return False

        return True

    def scan_number(self, *args) -> bool:
        """
        Проверяет наличие уже существующих номеров в справочнике.

        :return: False, если хотя бы один из номеров уже существует, иначе True.
        """
        values = self.open_file()

        if len(args) == 1:
            work_number = member_phone = str(args[0])
        elif len(args) == 2:
            work_number, member_phone = map(str, args)

        for data in values:
            if data['work_number'] == work_number:
                print('Рабочий номер уже есть в справочнике.')
                return False
            elif data['member_phone'] == member_phone:
                print('Личный номер уже есть в справочнике.')
                return False
        return True

    def start(self) -> None:
        """
        Запуск консольного интерфейса.

        :return: None
        """

        while True:
            print('Список действий:\n'
                  '1. Добавления новой записи в справочник\n'
                  '2. Вывод постранично данных на экран\n'
                  '3. Поиск в справочнике\n'
                  '4. Редактирования записи в справочнике\n'
                  '5. Выход')
            choice = input('Введите номер действия: ')

            try:
                if choice == '1':
                    name = input('Введите Имя: ')
                    last_name = input('Введите Фамилию: ')
                    surname = input('Введите Отчество: ')
                    name_company = input('Введите название компании: ')
                    work_number = input('Введите номер телефона компании: ')
                    member_phone = input('Введите личный номер телефона: ')
                    member = Member(name, last_name, surname, name_company, work_number, member_phone)
                    is_valid = self.validate(member.__dict__)
                    if is_valid:
                        is_scan = self.scan_number(work_number, member_phone)
                        if is_scan:
                            self.add_member(member)
                            print('ЮЗЕР УСПЕШНО ДОБАВЛЕН')

                elif choice == '2':
                    count_page = len(self.open_file())
                    self.get_page(int(input(
                        f'Введите номер страницы (страниц в справочнике - {math.ceil(count_page / 5)}): ')))

                elif choice == '3':
                    val = int(input('Выберите критерий для поиска:\n'
                                    '1. Имя\n'
                                    '2. Фамилия\n'
                                    '3. Отчество\n'
                                    '4. Название компании\n'
                                    '5. Номер компании\n'
                                    '6. Личный номер\n'
                                    'Введите номер критерия: '))
                    criteria_dict = {
                        '1': 'name',
                        '2': 'last_name',
                        '3': 'surname',
                        '4': 'name_company',
                        '5': 'work_number',
                        '6': 'member_phone',
                    }
                    target = input(f'Укажите {criteria_dict[str(val)]} для поиска: ')
                    criteria = criteria_dict.get(str(val))
                    if criteria:
                        self.binary_search_member(criteria, target)

                elif choice == '4':
                    criteria_dict = {
                        '1': 'name',
                        '2': 'last_name',
                        '3': 'surname',
                        '4': 'name_company',
                        '5': 'work_number',
                        '6': 'member_phone',
                    }

                    target = int(input('Введите номер PK пользователя: '))
                    criteria_choice = input('Выберите критерий для изменения:\n'
                                            '1. Имя\n'
                                            '2. Фамилия\n'
                                            '3. Отчество\n'
                                            '4. Название компании\n'
                                            '5. Номер компании\n'
                                            '6. Личный номер\n'
                                            'Введите номер критерия: ')

                    new_value = input('Введите новое значение: ')
                    if self.scan_number(new_value):
                        criteria = criteria_dict.get(criteria_choice)
                        self.edit_member(criteria, target, new_value)

                elif choice == '5':
                    print('Программа завершена.')
                    break

                else:
                    raise ValueError('Некорректный ввод, пожалуйста выберите номер действия из списка')

            except ValueError as e:
                print(e)


if __name__ == "__main__":
    phone_book = PhoneBook()
    phone_book.start()
