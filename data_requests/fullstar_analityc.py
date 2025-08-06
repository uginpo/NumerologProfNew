from typing import Dict, List
from data_requests.triple_request import fill_star_triples, create_triples_dict


def get_fullstar_analytic(fullstar_content: Dict[str, str]) -> Dict | None:
    # формируем заполненные тройки арканов
    triples_lst: List = fill_star_triples(content_dict=fullstar_content)
    # получаем словарь с ключами - тройками арканов для страницы аналитики
    # подсказками для оператора
    triples_dict: Dict[str, List[str]] | None = create_triples_dict(triples_lst)

    return triples_dict
