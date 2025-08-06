from business_logic.star_triples_data import fullstar_triples, Triple
from business_logic.star_triples_data import fullstar_id
from business_logic.star_triples_data import triples_combinations

from loguru import logger
from utils.color_utils import repr_data

from typing import List, Dict


def fill_star_triples(content_dict: Dict[str, str]) -> List[Triple]:
    """Заполняет тройки в звезде соответствующими арканами
    Args:
        content_dict (dict): арканы полной звезды

    Returns:
        List: список заполненных троек арканами
    """

    fullstar_triples_value: List[Triple] = []
    for triple in fullstar_triples:
        first, second, third = triple.pos
        triple.values = (
            arcane_from_number(first, content_dict),
            arcane_from_number(second, content_dict),
            arcane_from_number(third, content_dict),
        )
        fullstar_triples_value.append(triple)
    logger.debug(f"Заполненные тройки {repr_data(fullstar_triples_value)}")

    return fullstar_triples_value


def arcane_from_number(key: int, content_dict: Dict[str, str]) -> int:
    """Возвращает значение аркана по номеру его позиции в словаре fullstar_dict
    Args:
        key (int): номер позиции аркана
        id_name (dict, optional): словарь связи номера с названием
        content_dict (dict, optional): словарь всех арканов Полной звезды
    Returns:
        int: значение аркана
    """
    name: str | None = fullstar_id.get(key)
    arcane: str = content_dict.get(name, "") if name else ""

    return int(arcane)


def create_triples_dict(
    fullstar_triples_value: List[Triple],
) -> Dict[str, List[str]] | None:
    """Создает словарь - ключи: комбинации троек арканов,
    находящиеся в Полной звезде, значения - подсказки, где искать эти
    тройки

    Args:
        fill_star_triples (List[Triple]): список заполненных арканами троек
                                          полной Звезды

    Returns:
        Dict[str, List[tuple]]: словарь комбинация - подсказка
    """
    triples_dict = {}
    for combination in triples_combinations:
        for item in fullstar_triples_value:
            triple: tuple | None = item.values

            if triple and are_tuples_identical(combination, triple):
                key: str = "-".join([str(n) for n in combination])
                triples_dict.setdefault(key, []).append(item.name)

    return triples_dict


def are_tuples_identical(tuple1: tuple, tuple2: tuple) -> bool | None:
    """Сравнивает два кортежа.
    Args:
        tuple1 (tuple): кортеж из списка комбинаций
                        может иметь два или три элемента
        tuple2 (tuple): кортеж троек арканов в Полной звезде

    Returns:
        bool: True если кортеж-комбинация "совпадает" с кортежем
              из тройки
    """
    match len(tuple1):
        case 3:
            return any([tuple1 == tuple2, tuple1[::-1] == tuple2])

        case 2:
            first_two_match = tuple1 == tuple2[:2]
            last_two_match = tuple1 == tuple2[1:]
            reversed_first_two_match = tuple1[::-1] == tuple2[:2]
            reversed_last_two_match = tuple1[::-1] == tuple2[1:]
            return any(
                [
                    first_two_match,
                    last_two_match,
                    reversed_first_two_match,
                    reversed_last_two_match,
                ]
            )
