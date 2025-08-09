from pathlib import Path

from loguru import logger

from business_logic.arcanes_classes import (
    TRIANGLES_NAMES,
    Client,
    ErrorStar,
    FooterStar,
    MainStar,
    MissionStar,
    PointerType,
    PythagorianTable,
    Scenario,
    Triangle,
    combine_couple_star,
    get_full_dial,
    get_inner_star,
)
from config.settings import (
    COUPLE,
    FULLSTAR,
    OUTPUT_PATH,
    PITHAGORIAN_TABLE,
    PREDICT,
    TRIANGLES,
)
from utils.pdf_creator import generate_pdf
from utils.render_context_builder import (
    build_dial_context,
    build_pythagorian_context,
    build_render_context,
    load_config,
)
from utils.transform_utils import repr_data


class DataCheckError(Exception):
    pass


def create_fullstar_report(
    client_info: Client, pointers: list[PointerType] = TRIANGLES_NAMES
) -> Path:
    mainstar = MainStar(client_info=client_info)
    errorstar = ErrorStar(star=mainstar)
    missionstar = MissionStar(star=mainstar, error=errorstar)
    footerstar = FooterStar(client_info=client_info)
    fullstar: dict = {
        **mainstar.to_dict(),
        **missionstar.to_dict(),
        **errorstar.to_dict(),
        **footerstar.to_dict(),
    }

    for pointer in pointers:
        triangle_dict = Triangle(
            star=mainstar, err=errorstar, pointer=pointer
        ).to_dict_inverted()
        fullstar = fullstar | triangle_dict  # main.py

    json_path = FULLSTAR.get("json", Path("."))
    config = load_config(json_path=json_path)
    context: dict[str, dict] = build_render_context(config, fullstar)

    fullstar_path: Path = OUTPUT_PATH / f"{client_info.name}_fullstar.pdf"
    template_path = FULLSTAR.get("jpg", Path("."))

    # TODO: реализовать функцию создания текстовых страниц описания звезды
    result: Path = generate_pdf(
        output_path=fullstar_path, template=template_path, page_data=context
    )

    return result


def collect_triangles_adult(
    client_info: Client, pointers: list[PointerType] = TRIANGLES_NAMES
) -> list[Path]:
    mainstar = MainStar(client_info=client_info)
    errorstar = ErrorStar(star=mainstar)

    result_list = [Path, ...]
    for pointer in pointers:
        triangle: dict = Triangle(
            star=mainstar, err=errorstar, pointer=pointer
        ).to_dict()

        triangle_path: Path = OUTPUT_PATH / f"{client_info.name}_{pointer}.pdf"

        json_path = TRIANGLES.get("json", Path("."))
        config = load_config(json_path=json_path)
        context: dict[str, dict] = build_render_context(config, triangle)
        template_path: Path = TRIANGLES.get(pointer, Path("."))

        result = generate_pdf(
            triangle_path, template=template_path, page_data=context)

        result_list.append(result)

    # TODO: реализовать функцию создания текстовых страниц треугольников
    logger.debug(f"{result_list=}")
    return result_list


def collect_triangles_child(
    client_info: Client, pointers: list[PointerType] = ["personality", "money"]
) -> list[Path]:
    # NOTE::будет использовано для выбора детского словаря
    is_child: bool = True

    mainstar = MainStar(client_info=client_info)
    errorstar = ErrorStar(star=mainstar)

    result_list = [Path, ...]
    for pointer in pointers:
        triangle: dict = Triangle(
            star=mainstar, err=errorstar, pointer=pointer
        ).to_dict()

        triangle_path: Path = OUTPUT_PATH / f"{client_info.name}_{pointer}.pdf"

        json_path = TRIANGLES.get("json", Path("."))
        config = load_config(json_path=json_path)
        context: dict[str, dict] = build_render_context(config, triangle)
        template_path: Path = TRIANGLES.get(pointer, Path("."))

        result = generate_pdf(
            triangle_path, template=template_path, page_data=context)

        result_list.append(result)
    # TODO: создать функцию создания текстовых страниц детских треугольников
    return result_list


def collect_predict_report(client_info: Client) -> Path:
    inner_star = get_inner_star(client_info)
    full_dial = get_full_dial(client_info)

    json_path = PREDICT.get("json", Path("."))
    config = load_config(json_path=json_path[0])
    context_star: dict[str, dict] = build_render_context(config, inner_star)

    config = load_config(json_path=json_path[1])
    context_dial: dict[str, dict] = build_dial_context(config, full_dial)
    context = context_star | context_dial

    predict_path: Path = OUTPUT_PATH / f"{client_info.name}_predict.pdf"
    template_path = PREDICT.get("jpg", Path("."))
    result: Path = generate_pdf(
        output_path=predict_path, template=template_path, page_data=context
    )
    # TODO: создать функцию создания текстовых страниц predict
    return result


def create_couple_report(scenario: Scenario) -> Path:
    client_info1 = scenario.clients[0]
    client_info2 = scenario.clients[1]

    star1 = MainStar(client_info=client_info1)
    star2 = MainStar(client_info=client_info2)

    couple_dict = combine_couple_star(star1=star1, star2=star2)

    logger.debug(f"{couple_dict=}")

    json_path = COUPLE.get("json", Path("."))
    config = load_config(json_path=json_path)
    context: dict[str, dict] = build_render_context(config, couple_dict)

    couple_path: Path = OUTPUT_PATH / f"{client_info1.name}_couple.pdf"
    template_path = COUPLE.get("jpg", Path("."))

    # TODO: реализовать функцию создания текстовых страниц описания пары
    result: Path = generate_pdf(
        output_path=couple_path, template=template_path, page_data=context
    )
    return result


def create_pythagorian_table(client_info: Client) -> Path:
    pythagorian_table = PythagorianTable(client_info).to_dict()

    json_path = PITHAGORIAN_TABLE.get("json", Path("."))
    config = load_config(json_path=json_path)
    context: dict[str, dict] = build_pythagorian_context(
        config, pythagorian_table)

    logger.debug(f"{pythagorian_table=}")
    logger.debug(f"pythagorian{context=}")

    pythagorian_path: Path = OUTPUT_PATH / \
        f"{client_info.name}_pythagorian.pdf"
    template_path = PITHAGORIAN_TABLE.get("jpg", Path("."))
    result: Path = generate_pdf(
        output_path=pythagorian_path, template=template_path, page_data=context
    )
    # TODO: создать функцию создания текстовых страниц predict
    return result
