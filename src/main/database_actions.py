import prettytable as pt

from src.data import materials
from src.data import database


def input_value(message: str) -> int | None:
    try:
        return int(input(message))
    except ValueError:
        print('Неверное значение')
        if input('Хотите попробовать ещё раз? (y/n) ') == 'y':
            return input_value(message)
        else:
            return None


def get_product_volume(product_name: str) -> float:
    """
    возвращает объем заготовки
    :param product_name: название заготовки
    :return: объем заготовки
    """
    product: dict = database[product_name]
    return product["dimensions"][0] * product["dimensions"][1] * product["dimensions"][2]


def get_product_weight(product_name: str) -> float:
    """
    возвращает вес заготовки
    :param product_name: название заготовки
    :return: вес заготовки
    """
    product: dict = database[product_name]
    material_name: str = product["material"]
    material: dict = materials[material_name]
    product_volume: float = get_product_volume(product_name)
    return product["count"] * product_volume * material["weight"]


def is_transferable(product_name: str, max_weight: float) -> bool:
    """
    проверяет можно ли перемещать заготовку
    :param product_name: название заготовки
    :param max_weight: максимальный вес транспортного средства
    :return: bool - может ли перемещаться
    """
    product_weight = get_product_weight(product_name)
    return product_weight <= max_weight


def display_product_info(product_name: str) -> str:
    """
    выводит информацию о заготовке
    :param product_name: название заготовки
    :return: str - информация о заготовке
    """
    product = database[product_name]
    return "{name}: [\n\tmaterial: {material},\n\tdimensions: {dimensions},\n\tcount: {count}\n]".format(
        name=product["name"],
        material=product["material"],
        dimensions=product["dimensions"],
        count=product["count"]
    )


def display_all(data: dict | None = None) -> str:
    """
    выводит информацию о заготовках
    :param data: база данных
    :return: str - информация о заготовках
    """
    if data is None:
        data = database
    table: pt.PrettyTable = pt.PrettyTable()
    table.field_names = ["name", "material", "dimensions", "count"]
    for product_name in data.keys():
        product = data[product_name]
        table.add_row([product["name"], product["material"], product["dimensions"], product["count"]])
    return table.get_string()


def display_ordered_items() -> str:
    """
    Отображает список ресурсов в порядке убывания.
    :return: None
    """
    database_names = [key for key in database.keys()]
    sort_database = {key: database[key] for key in database_names}
    return display_all(sort_database)


def input_key(new_key_required: bool) -> str | None:
    """
    Запрашивает у пользователя ключ записи.
    :return: str: Ключ записи
    """
    try:
        print(f"Существующие ключи: {', '.join(list(database.keys()))}")
        key: str = input('Введите ключ записи: ')
        if new_key_required ^ (key in database.keys()):
            return key
        else:
            raise ValueError
    except ValueError:
        print('Неверный ключ')
        if input('Хотите попробовать ещё раз? (y/n) ') == 'y':
            return input_key(new_key_required)
        else:
            return None


def delete_row() -> None:
    key: str = input_key(False)
    if key:
        del database[key]
        print(f'Ресурс {key} удален')


def add_new_rows():
    """
    Добавляет N записей в базу данных.
    """
    n = input_value('Введите количество записей, которые хотите добавить: ')
    for _ in range(n):
        add_new_row()


def add_new_row() -> None:
    """
    Добавляет одну запись в базу данных.
    """
    new_key: str = input_key(True)
    if new_key is not None:
        database[new_key] = {
            "name": input('Введите название: '),
            "material": input_material(),
            "dimensions": input_dimensions(),
            "count": input_value('Введите количество: ')
        }


def input_material() -> str:
    """
    Запрашивает у пользователя название материала.
    :return: str: Название материала
    """
    print(f"Существующие материалы: {', '.join(list(materials.keys()))}")
    material: str = input('Введите название материала: ')
    if material in materials.keys():
        return material
    else:
        print('Неверное название материала')
        return input_material()


def input_dimensions() -> list:
    """
    Запрашивает у пользователя размеры.
    :return: list: Размеры
    """
    dimensions: str = input('Введите размеры через пробел: ')
    try:
        return list(map(float, dimensions.split()))
    except Exception as e:
        print(f'Неверные данные: {e}')
        return input_dimensions()


def search_row() -> None:
    """
    Поиск записи по ключу.
    :return: None
    """
    key: str = input_key(False)
    if key:
        value = database[key]
        print(
            f'{key}: {value[0]}\n'
            f'План производства: {value[2]}\n'
            f'Факт производства: {value[3]}\n'
            f'Отклонение: {int(value[3]) - int(value[2])}'
        )
    return None
