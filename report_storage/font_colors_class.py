from typing import Dict, Tuple

from config.settings import SCALE_PX_MM
from utils.color_utils import hex_to_rgb


class FontsColorsConfig:
    """Класс для хранения и получения шрифтов и цветов"""

    def __init__(self, scale: float = SCALE_PX_MM):
        self.scale = scale  # Масштаб пикселей в миллиметры

    def _create_font_settings(self, name: str, size: float, style: str = "") -> Dict:
        """Создает настройки шрифта"""
        return {"name": name, "style": style, "size": int(size * self.scale)}

    def _create_color_settings(self, hex_color: str) -> Tuple[int, int, int]:
        """Преобразует HEX-цвет в RGB"""
        return hex_to_rgb(hex_color)

    # Настройки для страницы Звезда
    @property
    def header_text(self) -> Dict:
        """Настройки для заголовка страницы"""
        return {
            "font": self._create_font_settings("roboto_regular", 240),
            "color": self._create_color_settings("#E3DDD0"),
        }

    @property
    def main_text(self) -> Dict:
        """Настройки для 'Личности'"""
        return {
            "font": self._create_font_settings("roboto_bold", 280),
            "color": self._create_color_settings("#E6DFD2"),
        }

    @property
    def fullstar_main(self) -> Dict:
        """Настройки для 'Личности'"""
        return {
            "font": self._create_font_settings("roboto_regular", 220),
            "color": self._create_color_settings("#F11616"),
        }

    @property
    def errors(self) -> Dict:
        """Настройки для ошибок"""
        return {
            "font": self._create_font_settings("roboto_medium", 220),
            "color": self._create_color_settings("#4E322B"),
        }

    @property
    def fullstar_errors(self) -> Dict:
        """Настройки для 'Личности'"""
        return {
            "font": self._create_font_settings("roboto_regular", 200),
            "color": self._create_color_settings("#00FFED"),
        }

    @property
    def mission(self) -> Dict:
        """Настройки для 'Миссии'"""
        return {
            "font": self._create_font_settings("roboto_regular", 300),
            "color": self._create_color_settings("#FF693A"),
        }

    @property
    def triangles_text(self) -> Dict:
        """Настройки для вершины треугольника"""
        return {
            "font": self._create_font_settings("roboto_regular", 145),
            "color": self._create_color_settings("#A9AAAA"),
        }

    @property
    def footer_text(self) -> Dict:
        """Настройки для текста в футере"""
        return {
            "font": self._create_font_settings("roboto_regular", 320),
            "color": self._create_color_settings("#E3DDD0"),
        }

    # Настройки для треугольника

    @property
    def vertex_text(self) -> Dict:
        """Настройки для вершины треугольника"""
        return {
            "font": self._create_font_settings("roboto_bold", 240),
            "color": self._create_color_settings("#04070F"),
        }

    @property
    def others_text(self) -> Dict:
        """Настройки для остальных вершин треугольника"""
        return {
            "font": self._create_font_settings("roboto_bold", 220),
            "color": self._create_color_settings("#E6DFD2"),
        }

    # Настройки для страницы аналитики
    @property
    def background_color(self) -> Tuple[int, int, int]:
        """Настройки для заголовков аналитики"""
        return self._create_color_settings("#DFFEF9")

    @property
    def text_color(self) -> Tuple[int, int, int]:
        """Настройки для заголовков аналитики"""
        return self._create_color_settings("#211A4E")

    @property
    def title_text(self) -> Dict:
        """Настройки для заголовков аналитики"""
        return self._create_font_settings("roboto_regular", 240)

    @property
    def subtitle_text(self) -> Dict:
        """Настройки для подзаголовков аналитики"""
        return self._create_font_settings("roboto_regular", 240 / 1.61)

    @property
    def plain_text(self) -> Dict:
        """Настройки для обычного текста аналитики"""
        return self._create_font_settings("roboto_light", (240 / 1.61 / 1.2))

    def get_fullstar_attributes(self) -> Dict:
        """Возвращает все атрибуты звезды"""
        attributes = {
            "header_text": self.header_text,
            "personality": self.fullstar_main,
            "spirituality": self.fullstar_main,
            "money": self.fullstar_main,
            "relationship": self.fullstar_main,
            "health": self.fullstar_main,
            "mission": self.fullstar_main,
            "mission_err": self.fullstar_main,
            "mission_all": self.fullstar_main,
            "pat_male_line_err": self.fullstar_errors,
            "mat_male_line_err": self.fullstar_errors,
            "pat_female_line_err": self.fullstar_errors,
            "doom_err": self.fullstar_errors,
            "mat_female_line_err": self.fullstar_errors,
            "foot_personality": self.footer_text,
            "foot_spirituality": self.footer_text,
            "foot_money": self.footer_text,
            "foot_relationship": self.footer_text,
            "foot_health": self.footer_text,
            "personal_inv_vertex": self.triangles_text,
            "personal_inv_mat_vertex": self.triangles_text,
            "personal_inv_pat_vertex": self.triangles_text,
            "spirituality_inv_vertex": self.triangles_text,
            "spirituality_inv_mat_vertex": self.triangles_text,
            "spirituality_inv_pat_vertex": self.triangles_text,
            "money_inv_vertex": self.triangles_text,
            "money_inv_mat_vertex": self.triangles_text,
            "money_inv_pat_vertex": self.triangles_text,
            "relationship_inv_vertex": self.triangles_text,
            "relationship_inv_mat_vertex": self.triangles_text,
            "relationship_inv_pat_vertex": self.triangles_text,
            "health_inv_vertex": self.triangles_text,
            "health_inv_mat_vertex": self.triangles_text,
            "health_inv_pat_vertex": self.triangles_text,
        }
        return attributes

    def get_triangle_attributes(self) -> Dict:
        """Возвращает все атрибуты Треугольника"""
        attributes = {
            "vertex": self.vertex_text,
            "mat_vertex": self.others_text,
            "pat_vertex": self.others_text,
            "inv_vertex": self.others_text,
            "inv_mat_vertex": self.others_text,
            "inv_pat_vertex": self.others_text,
        }
        return attributes

    def get_text_attributes(self) -> Dict:
        """Возвращает все атрибуты Треугольника"""
        attributes = {
            "background_color": self.background_color,
            "text_color": self.text_color,
            "title_text": self.title_text,
            "subtitle_text": self.subtitle_text,
            "plain_text": self.plain_text,
        }
        return attributes


"""
---------------------------------------------------------------
Использование
---------------------------------------------------------------
# Создаем конфигурацию с масштабом
config = FontsColorsConfig(scale=SCALE_PX_MM)

# Получаем настройки для заголовка
header_config = config.header_text
print(header_config)
# Вывод: {'font': {'name': 'roboto_regular', 'style': '', 'size': 24}, 'color': (227, 221, 208)}

# Получаем настройки для ошибок
errors_config = config.errors
print(errors_config)
# Вывод: {'font': {'name': 'roboto_medium', 'style': '', 'size': 22}, 'color': (78, 50, 43)}

# Создаем конфигурацию
config = FontsColorsConfig(scale=SCALE_PX_MM)

# Получаем все атрибуты
all_attributes = config.get_all_attributes()

# Выводим настройки для каждого элемента
for key, value in all_attributes.items():
    print(f"{key}: {value}")
"""
