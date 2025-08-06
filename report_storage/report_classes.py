from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Union, Literal, Any


# Определение классов для данных
@dataclass
class TextElement:
    """Описывает один текстовый элемент"""

    position: Tuple[float, float] | None = None  # Координаты (x, y)
    text: str | None = None  # Текст
    font: (
        Dict[
            str,
            Union[
                Literal[
                    "",
                    "B",
                    "I",
                    "U",
                    "BU",
                    "UB",
                    "BI",
                    "IB",
                    "IU",
                    "UI",
                    "BIU",
                    "BUI",
                    "IBU",
                    "IUB",
                    "UBI",
                    "UIB",
                ],
                int,
            ],
        ]
        | None
    ) = None  # Параметры шрифта
    color: Tuple[int, int, int] | None = None  # Цвет текста (RGB)


@dataclass
class ImagePageData:
    """Описывает данные для страницы с изображением"""

    image_path: str  # Путь к изображению
    info_positions: List[TextElement]  # Группы текстовых элементов


@dataclass
class Section:
    """Описывает раздел текста"""

    title: str = ""  # Название раздела
    subtitle: str = ""  # Название подраздела
    info: List[str] = field(
        default_factory=list  # Создаем новый пустой список для каждого экземпляра
    )
    # Шрифт названия раздела
    title_font: Dict[str, Union[Any, int]] | None = None
    subtitle_font: Dict[str, Union[Any, int]] | None = None
    info_font: Dict[str, Union[Any, int]] | None = None


@dataclass
class TextPageData:
    """Описывает данные для страницы с текстом"""

    background_color: Tuple[int, int, int] = (
        255,
        255,
        255,
    )  # Цвет фона по умолчанию (белый)
    # Цвет текста по умолчанию (черный)
    text_color: Tuple[int, int, int] = (0, 0, 0)
    sections: List[Section] = field(
        default_factory=list  # Создаем новый пустой список для каждого экземпляра
    )


""" Данные для страницы с изображением
    text2 = TextElement(
        position=(60, 120),
        text="Текст 2",
        font={"name": "DejaVu", "style": "U", "size": 14},
        color=(0, 0, 255)
    )
    image_page_data = ImagePageData(
        image_path="example_image.jpg", info_positions=[group1, group2])
"""

"""
        # Данные для страниц с текстом
    section1 = Section(
        title="Раздел 1",
        title_font={"name": "DejaVu", "style": "B", "size": 20},
        subsections=[
            {
                "title": "Подраздел 1.1",
                "subtitle_font": {"name": "DejaVu", "style": "U", "size": 16},
                "info": "Информация о подразделе 1.1",
                "info_font": {"name": "DejaVu", "style": "I", "size": 12},
            },
            {
                "title": "Подраздел 1.2",
                "subtitle_font": {"name": "DejaVu", "style": "B", "size": 14},
                "info": "Информация о подразделе 1.2",
                "info_font": {"name": "DejaVu", "style": "", "size": 10},
            },
        ],
    )
    section2 = Section(
        title="Раздел 2",
        title_font={"name": "DejaVu", "style": "B", "size": 18},
        subsections=[
            {
                "title": "Подраздел 2.1",
                "subtitle_font": {"name": "DejaVu", "style": "BI", "size": 14},
                "info": "Информация о подразделе 2.1",
                "info_font": {"name": "DejaVu", "style": "", "size": 12},
            },
            {
                "title": "Подраздел 2.2",
                "subtitle_font": {"name": "DejaVu", "style": "U", "size": 12},
                "info": "Информация о подразделе 2.2",
                "info_font": {"name": "DejaVu", "style": "I", "size": 10},
            },
        ],
    )
    text_page_data = TextPageData(background_color, text_color, sections=[section1, section2])
    """
