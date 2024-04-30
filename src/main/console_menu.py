import prettytable as pt
import os

import src.main.database_actions as database_actions


def get_actions() -> str:
    """
    Получает выводимый пользователю список действий.

    :return: str: Список действий
    """
    result: str = ''
    for key, value in menu_actions.items():
        result += f'{key} - {value}\n'
    return result


def clear_screen() -> None:
    """
    Очищает экран.
    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    return None


def exit_app() -> None:
    """
    Завершает работу программы.
    :return: None
    """
    print('Завершение работы')
    return None


def wait_for_enter() -> None:
    """
    Ожидает нажатия Enter.
    :return: None
    """
    input('Нажмите Enter для продолжения...')
    return None


def start_print():
    table = pt.PrettyTable()
    table.add_column(fieldname='',
                     column=[
                         'МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ',
                         'ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ',
                         'ВЫСШЕГО ОБРАЗОВАНИЯ УЧРЕЖДЕНИЕ',
                         'РЯЗАНСКИЙ ГОСУДАРСТВЕННЫЙ РАДИОТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ',
                         'имени В.Ф. УТКИНА\n',
                         'ФАКУЛЬТЕТ ВЫЧИСЛИТЕЛЬНОЙ ТЕХНИКИ\n',
                         'КАФЕДРА ВЫЧИСЛИТЕЛЬНОЙ И ПРИКЛАДНОЙ МАТЕМАТИКИ\n',
                         'программа к курсовой работе по лисциплине',
                         'АЛГОРИТМИЧЕСКИЕ ЯЗЫКИ И ПРОГРАММИРОВАНИЕ',
                         'на тему',
                         'РАБОТА СО СЛОВАРЯМИ\n',
                         'автор программы: студент группы 345',
                         'Кулев Г.А.',
                         'проверил: доцент кафедры ВПМ',
                         'Коротаев Алексей Тимофеевич',
                         'Рязань, 2024\n'
                     ])
    table.set_style(pt.PLAIN_COLUMNS)
    print(table)
    wait_for_enter()
    return None


def get_next_action() -> int:
    """
    Запрашивает действие пользователя и возвращает его.
    :return: int: Номер действия
    """
    try:
        action: int = int(input('Выберите действие: ')) - 1
        if str(action + 1) in (menu_actions.keys()):
            print(f'Вы выбрали действие: {menu_actions[str(action + 1)]}')
            return action
        else:
            raise ValueError
    except ValueError:
        print('Такого действия нет')
        return get_next_action()


def determine_action(action: int) -> bool:
    """
    Выполняет действие пользователя.
    :param action: Номер действия
    :return: База данных и флаг завершения действия
    """
    if action == -1:
        return False
    else:
        if action == 0:
            print(database_actions.display_all())
        elif action == 1:
            database_actions.add_new_rows()
        elif action == 2:
            database_actions.delete_row()
        elif action == 3:
            database_actions.search_row()
        elif action == 4:
            print(database_actions.display_ordered_items())
        wait_for_enter()
        clear_screen()
    return True


menu_actions: dict[str, str] = {
    '1': 'Просмотр всех записей в базе данных',
    '2': 'Добавление N записей',
    '3': 'Удаление записи по ключу',
    '4': 'Поиск необходимой информации',
    '5': 'Отобразить отсортированные данные',
    '0': 'Завершение работы с базой данных',
}
