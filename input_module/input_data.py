# input_module/input_data.py
from datetime import datetime

from business_logic.arcanes_classes import Client, GenderType, Scenario


class ExitError(Exception):
    pass


def validate_gender(gender: str) -> tuple[bool, GenderType]:
    if gender.upper() in ["М", "M", "МУЖ", "MALE"]:
        return True, "M"
    elif gender.upper() in ["Ж", "F", "ЖЕН", "FEMALE"]:
        return True, "F"
    else:
        return False, "F"


# dob - day_of_birthday
def calculate_age(dob: datetime) -> int:
    today = datetime.today()
    diff = (today.month, today.day) < (dob.month, dob.day)
    return today.year - dob.year - diff


def validate_date(
    dob_str: str, is_adult: bool = False, is_child: bool = False
) -> tuple[bool, str]:
    try:
        dob = datetime.strptime(dob_str, "%d.%m.%Y")
    except ValueError:
        return False, "Некорректный формат даты. Используйте ДД.ММ.ГГГГ."

    if dob > datetime.today():
        return False, "Дата рождения не может быть больше текущей даты."

    age = calculate_age(dob)

    if is_adult and age < 12:
        return False, "Клиент должен быть не младше 12 лет (взрослый)."

    if is_child and age >= 12:
        return False, "Ребёнок должен быть младше 12 лет."

    return True, ""


def enter_data() -> Scenario:
    def input_client(is_adult: bool = False, is_child: bool = False):
        name = input("Введите имя: ").strip()
        while not name:
            name = input("Введите имя: ").strip()

        gender_valid, gender_result = validate_gender(input("Пол (М/Ж): "))
        while not gender_valid:
            print("Пол должен быть указан как 'М', 'Ж', 'M' или 'F'.")
            gender_valid, gender_result = validate_gender(input("Пол (М/Ж): "))

        gender = gender_result

        dob = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
        valid, msg = validate_date(dob, is_adult=is_adult, is_child=is_child)
        while not valid:
            print(msg)
            dob = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
            valid, msg = validate_date(
                dob, is_adult=is_adult, is_child=is_child)

        name = name.strip() if len(name) <= 10 else name.strip().split(" ")[0]
        birthday = datetime.strptime(dob, "%d.%m.%Y").date()
        return Client(name=name, birthday=birthday, gender=gender)

    print("Выберите тип отчета:")
    print("1. Один взрослый (по умолчанию)")
    print("2. Один ребенок")
    print("3. Отношения в паре")
    print("11. Adult")
    print("22. Child")
    print("33. Couple")
    print("4. Выход")

    choice = input(
        "Введите номер (или нажмите Enter для выбора 'Один взрослый'): "
    ).strip()

    match choice:
        case "1":
            print("\n--- Ввод данных для клиента (взрослый) ---")
            client = input_client(is_adult=True)
            result = Scenario(scenario="adult", clients=[client])

        case "2":
            print("\n--- Ввод данных для ребенка ---")
            client = input_client(is_child=True)
            result = Scenario(scenario="child", clients=[client])

        case "3":
            print("\n--- Ввод данных для партнера 1 (взрослый) ---")
            client1 = input_client(is_adult=True)
            print("\n--- Ввод данных для партнера 2 (взрослый) ---")
            client2 = input_client(is_adult=True)
            result = Scenario(scenario="couple", clients=[client1, client2])

        case "11":
            birthday = datetime.strptime("7.12.1963", "%d.%m.%Y").date()
            result = Scenario(
                scenario="adult",
                clients=[Client(name="John", birthday=birthday, gender="M")],
            )
            return result

        case "22":
            birthday = datetime.strptime("6.02.2019", "%d.%m.%Y").date()
            result = Scenario(
                scenario="child",
                clients=[Client(name="John", birthday=birthday, gender="M")],
            )
            return result

        case "33":
            birthday1 = datetime.strptime("7.12.1963", "%d.%m.%Y").date()
            birthday2 = datetime.strptime("23.7.1982", "%d.%m.%Y").date()
            result = Scenario(
                scenario="couple",
                clients=[
                    Client(name="John", birthday=birthday1, gender="F"),
                    Client(name="Jul", birthday=birthday2, gender="M"),
                ],
            )
            return result

        case _:
            raise ExitError("Выход из программы")

    return result
