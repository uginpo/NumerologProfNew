from datetime import date

import pytest

from business_logic.arcanes_classes import (
    Client,
    ErrorStar,
    FooterStar,
    MainStar,
    MissionStar,
    Triangle,
    digital_root,
)


# Тест функции digital_root
def test_digital_root():
    assert digital_root(23) == 5  # 2 + 3 = 5
    assert digital_root(1990) == 19  # 1 + 9 + 9 + 0 = 19
    assert digital_root(21) == 21  # <= 22 → остаётся
    assert digital_root(22) == 22  # точно равно
    assert digital_root(24) == 6  # 2 + 4 = 6
    assert digital_root(99) == 18  # 9 + 9 = 18
    assert digital_root(100) == 1  # 1 + 0 + 0 = 1
    assert digital_root(1990, arcanes_number=9) == 1  # 1+9+9+0=19→1+9=10→1
    assert digital_root(21, arcanes_number=20) == 3  # 21 > 20 → 2+1 = 3


# Параметризованный тест для MainStar
@pytest.mark.parametrize(
    "name, birthday, gender, expected",
    [
        (
            "Иван",
            date(1990, 5, 15),
            "male",
            {
                "personality": 15,
                "spirituality": 5,
                "money": 19,
                "relationship": 12,
                "health": 6,
            },
        ),
        (
            "Мария",
            date(1985, 12, 3),
            "female",
            {
                "personality": 3,
                "spirituality": 12,
                "money": 5,
                "relationship": 20,
                "health": 4,
            },
        ),
        (
            "Петр",
            date(2000, 1, 1),
            "male",
            {
                "personality": 1,
                "spirituality": 1,
                "money": 2,
                "relationship": 4,
                "health": 8,
            },
        ),
    ],
)
def test_main_star(name, birthday, gender, expected):
    client = Client(name=name, birthday=birthday, gender=gender)
    main_star = MainStar(client_info=client)

    assert main_star.personality == expected["personality"]
    assert main_star.spirituality == expected["spirituality"]
    assert main_star.money == expected["money"]
    assert main_star.relationship == expected["relationship"]
    assert main_star.health == expected["health"]


# Параметризованный тест для ErrorStar
@pytest.mark.parametrize(
    "main_star_values, expected",
    [
        (
            (6, 5, 19, 3, 6),
            {
                "err_personality": 11,
                "err_spirituality": 6,
                "err_money": 22,
                "err_relationship": 9,
                "err_health": 12,
            },
        ),
        (
            (3, 3, 5, 11, 4),
            {
                "err_personality": 6,
                "err_spirituality": 8,
                "err_money": 16,
                "err_relationship": 15,
                "err_health": 7,
            },
        ),
        (
            (1, 1, 2, 4, 8),
            {
                "err_personality": 2,
                "err_spirituality": 3,
                "err_money": 6,
                "err_relationship": 12,
                "err_health": 9,
            },
        ),
    ],
)
def test_error_star(main_star_values, expected):
    class MockMainStar:
        def __init__(self, values):
            self.personality = values[0]
            self.spirituality = values[1]
            self.money = values[2]
            self.relationship = values[3]
            self.health = values[4]

        def to_dict(self): ...

    mock_star = MockMainStar(main_star_values)
    error_star = ErrorStar(star=mock_star)

    assert error_star.err_personality == expected["err_personality"]
    assert error_star.err_spirituality == expected["err_spirituality"]
    assert error_star.err_money == expected["err_money"]
    assert error_star.err_relationship == expected["err_relationship"]
    assert error_star.err_health == expected["err_health"]


# Параметризованный тест для MissionStar
@pytest.mark.parametrize(
    "mission_values, mission_error_values, expected",
    [
        (
            (6, 5, 19, 3, 6),
            (11, 6, 22, 9, 12),
            {
                "mission": 12,
                "mission_error": 6,
                "mission_full": 18,
            },
        ),
        (
            (3, 3, 5, 11, 4),
            (6, 8, 16, 15, 7),
            {
                "mission": 8,
                "mission_error": 7,
                "mission_full": 15,
            },
        ),
        (
            (1, 1, 2, 4, 8),
            (2, 3, 6, 12, 9),
            {
                "mission": 16,
                "mission_error": 5,
                "mission_full": 21,
            },
        ),
    ],
)
def test_mission_star(mission_values, mission_error_values, expected):
    class MockMainStar:
        def __init__(self, values):
            self.personality = values[0]
            self.spirituality = values[1]
            self.money = values[2]
            self.relationship = values[3]
            self.health = values[4]

        def to_dict(self): ...

    class MockErrorStar:
        def __init__(self, values):
            self.err_personality = values[0]
            self.err_spirituality = values[1]
            self.err_money = values[2]
            self.err_relationship = values[3]
            self.err_health = values[4]

        def to_dict(self): ...

    mock_star = MockMainStar(mission_values)
    mock_error = MockErrorStar(mission_error_values)
    mission_star = MissionStar(star=mock_star, error=mock_error)

    assert mission_star.mission == expected["mission"]
    assert mission_star.mission_error == expected["mission_error"]
    assert mission_star.mission_full == expected["mission_full"]


# Параметризованный тест для FooterStar
@pytest.mark.parametrize(
    "birthday, expected",
    [
        (
            date(1990, 5, 15),
            {
                "foot_personality": 6,
                "foot_spirituality": 5,
                "foot_money": 1,
                "foot_relationship": 3,
                "foot_health": 6,
            },
        ),
        (
            date(1985, 12, 3),
            {
                "foot_personality": 3,
                "foot_spirituality": 3,
                "foot_money": 5,
                "foot_relationship": 2,
                "foot_health": 4,
            },
        ),
        (
            date(2000, 1, 1),
            {
                "foot_personality": 1,
                "foot_spirituality": 1,
                "foot_money": 2,
                "foot_relationship": 4,
                "foot_health": 8,
            },
        ),
    ],
)
def test_footer_star(birthday, expected):
    client = Client(name="Тест", birthday=birthday, gender="unknown")
    footer_star = FooterStar(client_info=client)

    assert footer_star.foot_personality == expected["foot_personality"]
    assert footer_star.foot_spirituality == expected["foot_spirituality"]
    assert footer_star.foot_money == expected["foot_money"]
    assert footer_star.foot_relationship == expected["foot_relationship"]
    assert footer_star.foot_health == expected["foot_health"]


# Проверка ошибок
def test_invalid_pointer():
    with pytest.raises(ValueError):
        Triangle(
            star=MainStar(Client("Test", date(2000, 1, 1), "male")),
            err=ErrorStar(MainStar(Client("Test", date(2000, 1, 1), "male"))),
            pointer="invalid",
        )
