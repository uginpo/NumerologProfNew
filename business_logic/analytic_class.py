from typing import Dict, List, Tuple

from loguru import logger
from business_logic.arcanes_classes import Star, Triangle
from report_storage.report_classes import Section

from text_storage.personality_dict import personality_dict
from text_storage.spirituality_dict import spirituality_dict
from text_storage.money_dict import money_dict
from text_storage.processing_dict import processing_dict
from text_storage.talents_dict import talents_dict
from text_storage.triples_dict import triples_dict


class StarAnalyticInfo:
    """Класс для хранения словарей аналитики страницы Звезда"""

    def __init__(self, star: Star):
        # Служебная информация
        self._star = star

        self._personality_dict = personality_dict.get(self._star.personality, None)
        self._spirituality_dict = spirituality_dict.get(self._star.spirituality, None)
        self._money_dict = money_dict.get(self._star.money, None)

        if not self._is_dict_correct():
            raise ValueError("В словаре(словарях) недостаточно данных")

        # Блок контента страницы аналитики
        self._personality_analytic = [
            Section(
                title="Личность",
                subtitle="Положительные черты",
                info=self._personality_dict.get("personality_positive"),
            ),
            Section(
                title="Личность",
                subtitle="Отрицательные черты",
                info=self._personality_dict.get("personality_negative"),
            ),
            Section(
                title="Личность",
                subtitle="Рекомендации",
                info=self._personality_dict.get("personality_recommendations"),
            ),
        ]

        self._spirituality_analytic = [
            Section(
                title="Духовность",
                subtitle="Программа рода:",
                info=self._spirituality_dict,  # type: ignore
            )
        ]

        self._money_analytic = [
            Section(
                title="Деньги",
                subtitle="Кем Вы были в прошлой жизни?",
                info=self._money_dict.get("main_number"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Профессии, которые Вам подходят:",
                info=self._money_dict.get("professions"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Ваша энергия:",
                info=self._money_dict.get("energy"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Ваши блоки и ограничения:",
                info=self._money_dict.get("restrictions"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Траты, увеличивающие доход:",
                info=self._money_dict.get("costs"),  # type: ignore
            ),
        ]

    def get_all_sections(self) -> List[Section]:
        """Возвращает контент для страницы аналитики звезды"""
        all_sections = self._personality_analytic
        all_sections.extend(self._spirituality_analytic)
        all_sections.extend(self._money_analytic)
        return all_sections

    def _is_dict_correct(self) -> bool:
        if not self._personality_dict:
            logger.error(
                f"В словаре personality_dict отсутствует информация по ключу {self._star.personality}"
            )

        if not self._spirituality_dict:
            logger.error(
                f"В словаре spirituality_dict отсутствует информация по ключу {self._star.spirituality}"
            )

        if not self._money_dict:
            logger.error(
                f"В словаре money_dict отсутствует информация по ключу {self._star.money}"
            )

        return all([self._personality_dict, self._spirituality_dict, self._money_dict])


class MoneyAnalyticInfo:
    """Класс для хранения словарей аналитики страницы ДТ"""

    def __init__(self, money: Triangle) -> None:
        self._money = money

        self._money_dict = money_dict.get(self._money.vertex)
        self._processing_dict = processing_dict.get(self._money.inv_vertex, None)
        self._talents_mat = talents_dict.get(self._money.mat_vertex, None)
        self._talents_pat = talents_dict.get(self._money.pat_vertex, None)
        self._talents_inv_mat = talents_dict.get(self._money.inv_mat_vertex, None)
        self._talents_inv_pat = talents_dict.get(self._money.inv_pat_vertex, None)
        self._talents_dict = talents_dict

        if not self._is_dict_correct():
            raise ValueError("В словаре(словарях) недостаточно данных")

    # Блок контента страницы аналитики
    @property
    def money_analytic(self):
        return [
            Section(
                title="Деньги",
                subtitle="Кем Вы были в прошлой жизни?",
                info=self._money_dict.get("main_number"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Профессии, которые Вам подходят:",
                info=self._money_dict.get("professions"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Ваша энергия:",
                info=self._money_dict.get("energy"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Ваши блоки и ограничения:",
                info=self._money_dict.get("restrictions"),  # type: ignore
            ),
            Section(
                title="Деньги",
                subtitle="Траты, увеличивающие доход:",
                info=self._money_dict.get("costs"),  # type: ignore
            ),
        ]

    @property
    def processing_analytic(self):
        return [
            Section(
                title="Проработка",
                subtitle="Важные качества",
                info=self._processing_dict.get("number"),  # type: ignore
            ),
            Section(
                title="Проработка",
                subtitle="Профессии, которые Вам подходят:",
                info=self._processing_dict.get("professions"),  # type: ignore
            ),
        ]

    @property
    def talents_analytic(self):
        set_vertex = set([self._money.inv_vertex, self._money.vertex])

        set_talents = set(
            [
                self._money.pat_vertex,
                self._money.mat_vertex,
                self._money.inv_pat_vertex,
                self._money.inv_mat_vertex,
            ]
        )

        self._talents_list = []
        for number in set_talents - set_vertex:
            self._talents_list.extend(self._talents_dict.get(number))

        return [
            Section(
                title="Таланты",
                subtitle="Таланты, переданные вашим родом:",
                info=self._talents_list,  # type: ignore
            )
        ]

    def get_all_sections(self) -> List[Section]:
        """
        Возвращает список словарей для создания страницы
        Returns:
            List: Список словарей c необходимой информацией
        """

        all_sections = self.money_analytic
        processing_flag, talent_flag = self._which_dict()

        if processing_flag:
            all_sections.extend(self.processing_analytic)

        if talent_flag:
            all_sections.extend(self.talents_analytic)

        return all_sections

    def _which_dict(self) -> List:
        """Возвращает список ключей для определения участия словарей
        в заполнения аналитики ДТ по определенному алгоритму
        вершина перевернутого треугольника не должна быть равна вершине основного
        треугольника и значения талантов не должны совпадать ни с вершиной
        основного треугольника, ни с вершиной перевернутого

        Returns:
            List[Dict]: Список ключей
        """

        set_vertex = set([self._money.inv_vertex, self._money.vertex])

        processing_flag = True if len(set_vertex) == 2 else False

        set_talents = set(
            [
                self._money.pat_vertex,
                self._money.mat_vertex,
                self._money.inv_pat_vertex,
                self._money.inv_mat_vertex,
            ]
        )
        talent_flag = True if len(set_talents - set_vertex) else False

        return [processing_flag, talent_flag]

    def _is_dict_correct(self) -> bool:
        if not self._money_dict:
            logger.error(
                f"В словаре money_dict отсутствует информация по ключу {self._money.vertex}"
            )

        if not self._processing_dict:
            logger.error(
                f"В словаре processing_dict отсутствует информация по ключу {self._money.inv_vertex}"
            )

        if not self._talents_mat:
            logger.error(
                f"В словаре talents_dict отсутствует информация по ключу {self._money.mat_vertex}"
            )

        if not self._talents_pat:
            logger.error(
                f"В словаре talents_dict отсутствует информация по ключу {self._money.pat_vertex}"
            )

        if not self._talents_inv_mat:
            logger.error(
                f"В словаре talents_dict отсутствует информация по ключу {self._money.inv_mat_vertex}"
            )

        if not self._talents_inv_pat:
            logger.error(
                f"В словаре talents_dict отсутствует информация по ключу {self._money.inv_pat_vertex}"
            )

        return all(
            [
                self._money_dict,
                self._processing_dict,
                self._talents_mat,
                self._talents_pat,
                self._talents_inv_mat,
                self._talents_inv_pat,
            ]
        )


def get_triples_analytic(page_of_triples: Dict | None) -> List[Section] | None:
    if isinstance(page_of_triples, dict):
        return [
            Section(
                title="Анализ ваших арканов",
                subtitle=f"Такая комбинация {key} позволяет предположить:",
                info=triples_dict.get(key, [f"не найдено {key}"]),
            )
            for key in page_of_triples.keys()
        ]
