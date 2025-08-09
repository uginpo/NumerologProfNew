# business_logic/arcanes_classes.py
from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import Dict, Literal, OrderedDict, Tuple

from loguru import logger

ScenarioType = Literal["adult", "child", "couple"]
GenderType = Literal["M", "F"]
PointerType = Literal["personality", "spirituality",
                      "money", "relationship", "health"]


TRIANGLES_NAMES: list[PointerType] = [
    "personality",
    "spirituality",
    "money",
    "relationship",
    "health",
]


@dataclass
class Client:
    name: str
    birthday: date
    gender: GenderType


@dataclass
class Scenario:
    scenario: ScenarioType
    clients: list[Client]


@dataclass(frozen=True)
class MainStar:
    client_info: Client

    @cached_property
    def personality(self) -> int:
        return digital_root(self.client_info.birthday.day)

    @cached_property
    def spirituality(self) -> int:
        return digital_root(self.client_info.birthday.month)

    @cached_property
    def money(self) -> int:
        return digital_root(self.client_info.birthday.year)

    @cached_property
    def relationship(self) -> int:
        return digital_root(self.personality + self.spirituality + self.money)

    @cached_property
    def health(self) -> int:
        return digital_root(2 * self.relationship)

    def to_dict(self) -> dict[str, str]:
        formatted_birthdate = self.client_info.birthday.strftime("%d.%m.%y")

        return {
            "header_text": f"{self.client_info.name} {formatted_birthdate}",
            "personality": str(self.personality),
            "spirituality": str(self.spirituality),
            "money": str(self.money),
            "relationship": str(self.relationship),
            "health": str(self.health),
        }


@dataclass(frozen=True)
class ErrorStar:
    star: MainStar

    @cached_property
    def err_personality(self) -> int:
        return digital_root(self.star.personality + self.star.spirituality)

    @cached_property
    def err_spirituality(self) -> int:
        return digital_root(self.star.spirituality + self.star.money)

    @cached_property
    def err_money(self) -> int:
        return digital_root(self.star.money + self.star.relationship)

    @cached_property
    def err_relationship(self) -> int:
        return digital_root(self.star.relationship + self.star.health)

    @cached_property
    def err_health(self) -> int:
        return digital_root(self.star.health + self.star.personality)

    def to_dict(self) -> Dict[str, str]:
        return {
            "err_personality": str(self.err_personality),
            "err_spirituality": str(self.err_spirituality),
            "err_money": str(self.err_money),
            "err_relationship": str(self.err_relationship),
            "err_health": str(self.err_health),
        }


@dataclass(frozen=True)
class MissionStar:
    star: MainStar
    error: ErrorStar

    @cached_property
    def mission(self) -> int:
        return digital_root(
            self.star.personality
            + self.star.spirituality
            + self.star.money
            + self.star.relationship
            + self.star.health
        )

    @cached_property
    def mission_error(self) -> int:
        return digital_root(
            self.error.err_personality
            + self.error.err_spirituality
            + self.error.err_money
            + self.error.err_relationship
            + self.error.err_health
        )

    @cached_property
    def mission_full(self) -> int:
        return digital_root(self.mission + self.mission_error)

    def to_dict(self) -> Dict[str, str]:
        return {
            "mission": str(self.mission),
            "mission_error": str(self.mission_error),
            "mission_full": str(self.mission_full),
        }


@dataclass(frozen=True)
class FooterStar:
    client_info: Client

    @cached_property
    def foot_personality(self) -> int:
        return digital_root(self.client_info.birthday.day, arcanes_number=9)

    @cached_property
    def foot_spirituality(self) -> int:
        return digital_root(self.client_info.birthday.month, arcanes_number=9)

    @cached_property
    def foot_money(self) -> int:
        return digital_root(self.client_info.birthday.year, arcanes_number=9)

    @cached_property
    def foot_relationship(self) -> int:
        return digital_root(
            self.foot_personality + self.foot_spirituality + self.foot_money,
            arcanes_number=9,
        )

    @cached_property
    def foot_health(self) -> int:
        return digital_root(2 * self.foot_relationship, arcanes_number=9)

    def to_dict(self) -> Dict[str, str]:
        return {
            "foot_personality": str(self.foot_personality),
            "foot_spirituality": str(self.foot_spirituality),
            "foot_money": str(self.foot_money),
            "foot_relationship": str(self.foot_relationship),
            "foot_health": str(self.foot_health),
        }


@dataclass(frozen=True)
class Triangle:
    star: MainStar
    err: ErrorStar
    pointer: PointerType

    @cached_property
    def vertex_data(self) -> Tuple[int, int, int]:
        mapping: Dict[PointerType, Tuple[int, int, int]] = {
            "personality": (
                self.star.personality,
                self.err.err_health,
                self.err.err_personality,
            ),
            "spirituality": (
                self.star.spirituality,
                self.err.err_personality,
                self.err.err_spirituality,
            ),
            "money": (
                self.star.money,
                self.err.err_spirituality,
                self.err.err_money,
            ),
            "relationship": (
                self.star.relationship,
                self.err.err_money,
                self.err.err_relationship,
            ),
            "health": (
                self.star.health,
                self.err.err_relationship,
                self.err.err_health,
            ),
        }
        if self.pointer not in mapping:
            logger.error(f"Недопустимый поинтер {self.pointer}")
            raise ValueError(f"Недопустимый поинтер {self.pointer}")

        return mapping[self.pointer]

    @cached_property
    def vertex(self) -> int:
        return self.vertex_data[0]

    @cached_property
    def left_vertex(self) -> int:
        return self.vertex_data[1]

    @cached_property
    def right_vertex(self) -> int:
        return self.vertex_data[2]

    @cached_property
    def inverted_vertex(self) -> int:
        return digital_root(self.left_vertex + self.right_vertex)

    @cached_property
    def inverted_left_vertex(self) -> int:
        return digital_root(self.left_vertex + self.vertex)

    @cached_property
    def inverted_right_vertex(self) -> int:
        return digital_root(self.right_vertex + self.vertex)

    @cached_property
    def right_middle_vertex(self) -> int:
        result = self.vertex + self.inverted_vertex
        return digital_root(result)

    @cached_property
    def left_middle_vertex(self) -> int:
        result = self.inverted_left_vertex + self.inverted_right_vertex
        return digital_root(result)

    def to_dict_predicted(self) -> Dict[str, str]:
        pref = self.pointer
        return {
            f"{pref}_inverted_left_vertex": str(self.inverted_left_vertex),
            f"{pref}_inverted_right_vertex": str(self.inverted_right_vertex),
        }

    def to_dict_inverted(self) -> Dict[str, str]:
        pref = self.pointer
        return {
            f"{pref}_inverted_vertex": str(self.inverted_vertex),
            f"{pref}_inverted_left_vertex": str(self.inverted_left_vertex),
            f"{pref}_inverted_right_vertex": str(self.inverted_right_vertex),
        }

    def to_dict(self) -> Dict[str, str]:
        return {
            "vertex": str(self.vertex),
            "left_vertex": str(self.left_vertex),
            "right_vertex": str(self.right_vertex),
            "inverted_vertex": str(self.inverted_vertex),
            "inverted_left_vertex": str(self.inverted_left_vertex),
            "inverted_right_vertex": str(self.inverted_right_vertex),
            "left_middle_vertex": str(self.left_middle_vertex),
            "right_middle_vertex": str(self.right_middle_vertex),
        }


@dataclass(frozen=True)
class PythagorianTable:
    client_info: Client

    @cached_property
    def _dob_before_2000(self) -> bool:
        return self.client_info.birthday.year < 2000

    @cached_property
    def number_1(self) -> int:
        return (
            simple_digital_root(self.client_info.birthday.day)
            + simple_digital_root(self.client_info.birthday.month)
            + simple_digital_root(self.client_info.birthday.year)
        )

    @cached_property
    def number_2(self) -> int:
        if self.number_1 in [11, 22, 33]:
            return self.number_1
        else:
            return digital_root(self.number_1, arcanes_number=9)

    @cached_property
    def number_3(self) -> int:
        if self._dob_before_2000:
            first_symbol = int(str(self.client_info.birthday.day)[0])
            return self.number_1 - 2 * first_symbol
        else:
            return 19

    @cached_property
    def number_4(self) -> int:
        if self._dob_before_2000:
            return digital_root(self.number_3, arcanes_number=9)
        else:
            return self.number_1 + 19

    @cached_property
    def number_5(self) -> int:
        if self._dob_before_2000:
            return 0
        else:
            return digital_root(self.number_4, arcanes_number=9)

    def to_dict(self) -> dict[str, str]:
        all_numbers = "".join(
            [
                str(self.number_1),
                str(self.number_2),
                str(self.number_3),
                str(self.number_4),
                str(self.number_5),
            ]
        )
        logger.debug(f"{all_numbers=}")
        result = OrderedDict()
        for d in range(1, 10):
            count_d = all_numbers.count(str(d))
            result[str(d)] = str(d) * count_d if count_d else "—"

        return result


def combine_couple_star(star1: MainStar, star2: MainStar) -> dict[str, str]:
    """создание звезды для пары клиентов"""

    attributes = [
        "personality",
        "spirituality",
        "money",
        "relationship",
        "health",
    ]
    combined_attrs = {
        attr: str(digital_root(getattr(star1, attr) + getattr(star2, attr)))
        for attr in attributes
    }
    header = f"{star1.client_info.name} + {star2.client_info.name}"
    combined_attrs["header_text"] = header

    return combined_attrs


def get_inner_star(
    client_info: Client, pointers: list[PointerType] = TRIANGLES_NAMES
) -> dict[str, str]:
    mainstar = MainStar(client_info=client_info)
    errorstar = ErrorStar(star=mainstar)
    inner_star: dict = {
        **mainstar.to_dict(),
        **errorstar.to_dict(),
    }
    if "header_text" in inner_star:
        del inner_star["header_text"]

    for pointer in pointers:
        triangles = Triangle(
            star=mainstar, err=errorstar, pointer=pointer
        ).to_dict_inverted()
        inner_star = inner_star | triangles

    return inner_star


def get_full_dial(
    client_info: Client, pointers: list[PointerType] = TRIANGLES_NAMES
) -> dict[str, str]:
    mainstar = MainStar(client_info=client_info)
    errorstar = ErrorStar(star=mainstar)
    main_dial: dict = {
        **mainstar.to_dict(),
        **errorstar.to_dict(),
    }
    if "header_text" in main_dial:
        del main_dial["header_text"]

    for pointer in pointers:
        triangles = Triangle(
            star=mainstar, err=errorstar, pointer=pointer
        ).to_dict_predicted()
        main_dial = main_dial | triangles

    key_mapping = [
        ("personality", "main_1"),
        ("personality_inverted_right_vertex", "main_2"),
        ("err_personality", "main_3"),
        ("spirituality_inverted_left_vertex", "main_4"),
        ("spirituality", "main_5"),
        ("spirituality_inverted_right_vertex", "main_6"),
        ("err_spirituality", "main_7"),
        ("money_inverted_left_vertex", "main_8"),
        ("money", "main_9"),
        ("money_inverted_right_vertex", "main_10"),
        ("err_money", "main_11"),
        ("relationship_inverted_left_vertex", "main_12"),
        ("relationship", "main_13"),
        ("relationship_inverted_right_vertex", "main_14"),
        ("err_relationship", "main_15"),
        ("health_inverted_left_vertex", "main_16"),
        ("health", "main_17"),
        ("health_inverted_right_vertex", "main_18"),
        ("err_health", "main_19"),
        ("personality_inverted_left_vertex", "main_20"),
    ]

    new_main_dial = OrderedDict()
    for old_key, new_key in key_mapping:
        if old_key in main_dial:
            new_main_dial[new_key] = main_dial[old_key]

    full_dial = count_dial_data(new_main_dial)

    return full_dial


def count_dial_data(dial: dict) -> dict[str, str]:
    """Создание данных для заполнения промежуточных данных шкалы
    в отчете predict"""

    keys = list(dial.keys())
    full_dial = OrderedDict()
    for i in range(len(keys)):
        current_key = keys[i]
        next_key = keys[(i + 1) % len(keys)]

        full_dial[current_key] = dial[current_key]

        left_key = f"inner_{current_key}_left"
        middle_key = f"inner_{current_key}_middle"
        right_key = f"inner_{current_key}_right"

        middle = digital_root(int(dial[current_key]) + int(dial[next_key]))
        left = digital_root(int(dial[current_key]) + middle)
        right = digital_root(int(dial[next_key]) + middle)

        full_dial[left_key] = str(left)
        full_dial[middle_key] = str(middle)
        full_dial[right_key] = str(right)
    return full_dial


def simple_digital_root(num: int) -> int:
    """Рассчитывает числовой корень из суммы цифр входящего числа."""
    return sum(int(d) for d in str(num))


def digital_root(num: int, arcanes_number: int = 22) -> int:
    """Рассчитывает числовой корень из суммы цифр входящего числа.
    Args:
        num (int): исходное число
        arcanes_number (int, optional): Максимальное количество арканов.
         Defaults to 22.
    Returns:
        int: числовой корень
    """
    number = num

    while number > arcanes_number:
        number = sum(int(d) for d in str(number))

    return number
