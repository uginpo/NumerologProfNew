from report_storage.report_classes import TextElement, ImagePageData
from report_storage.report_classes import Section, TextPageData
from typing import Dict, List, Any, Tuple
from enum import Enum


from report_storage.position_class import StarPositions, TrianglePositions
from report_storage.position_class import FullStarPositions
from report_storage.font_colors_class import FontsColorsConfig


class PageNames(str, Enum):
    STAR = "star"
    FULLSTAR = "fullstar"
    MONEY = "money"


def combine_all_data(
    image_content: Dict, text_content: List | None, page_name: str
) -> List:
    """Объединяет все данные для создания полного
    pdf отчета по странице Star

    Args:
        image_content (Dict): данные арканов
        text_content (List): аналитика (описание) данных арканов

    Returns:
        List: Полные данные, включая шрифты и настройки для
        создания pdf отчета
    """
    # Объединение данных для страницы-изображения
    union_data: List = combine_image_data(
        image_content=image_content, page_name=page_name
    )
    # union_text: TextPageData = combine_star_text_data(text_content)
    union_text: TextPageData | None = (
        combine_text_data(text_content, page_name=page_name) if text_content else None
    )

    return [union_data, union_text]


def combine_image_data(image_content: Dict, page_name: str) -> List:
    """Объединяет данные арканов с координатами и шрифтами
    Args:
        image_content (Dict): данные арканов
    Returns:
        List: Объединенные данные
    """
    fonts_colors = FontsColorsConfig()

    match page_name:
        case "star":
            # Получаем координаты
            data_positions: StarPositions | TrianglePositions | FullStarPositions = (
                StarPositions()
            )
            # Получаем шрифты
            fonts_list = fonts_colors.get_star_attributes().values()

        case "money":
            # Получаем координаты
            data_positions = TrianglePositions()
            # Получаем шрифты
            fonts_list = fonts_colors.get_triangle_attributes().values()

        case "fullstar":
            # Получаем координаты
            data_positions = FullStarPositions()
            # Получаем шрифты
            fonts_list = fonts_colors.get_fullstar_attributes().values()

    positions = data_positions.get_all_positions().values()
    # Получаем значения арканов
    arcanes = image_content.values()

    # объединяем в общий список
    combined_list = [
        TextElement(
            position=pos,
            text=arcane,
            font=font_dict.get("font"),
            color=font_dict.get("color"),
        )
        for pos, arcane, font_dict in zip(positions, arcanes, fonts_list)
    ]

    return combined_list


def combine_text_data(text_content: List, page_name: str) -> TextPageData | None:
    """Объединяет данные аналитики с координатами и шрифтами

    Args:
        text_content (List[Dict]): список словарей с аналитикой
        page_name (str): название страницы
    Returns:
        List: Объединенные данные
    """

    # Получаем шрифты
    fonts_colors = FontsColorsConfig()
    fonts_dict: Dict = fonts_colors.get_text_attributes()

    # цвета
    background_color: Tuple = fonts_dict.get("background_color")  # type: ignore

    text_color: Tuple = fonts_dict.get("text_color")  # type: ignore

    # шрифты
    title_font: Dict | Any = fonts_dict.get("title_text")
    subtitle_font = fonts_dict.get("subtitle_text")
    info_font = fonts_dict.get("plain_text")

    # Дополняем данные в Section информацией о шрифтах
    for item in text_content:
        item.subtitle_font = subtitle_font
        item.title_font = title_font
        item.info_font = info_font

    union_text = TextPageData(
        background_color=background_color, text_color=text_color, sections=text_content
    )

    return union_text
