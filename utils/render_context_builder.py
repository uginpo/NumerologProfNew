# utils/render_context_builder.py

import json
import math
from pathlib import Path

from glom import glom

from config.settings import SCALE_PX_MM
from utils.transform_utils import hex_to_rgb


def scale_position(
    position: tuple[int, int] | list, scale: float = SCALE_PX_MM
) -> tuple[float, float]:
    """Scale position from pixels to mm."""

    x, y = position[0], position[1]
    return (x * scale, y * scale)


def calculate_position(center, radius, angle_degrees):
    """Рассчитывает координаты точки на окружности"""
    angle_rad = math.radians(angle_degrees)
    x = center[0] + radius * math.cos(angle_rad)
    y = center[1] + radius * math.sin(angle_rad)
    return (x, y)


def resolve_ref(config: dict, ref_key: str = "$ref") -> dict:
    """Recursively resolve all $ref in config using glom."""

    def _resolve(value):
        if isinstance(value, dict):
            if ref_key in value:
                path = value[ref_key]
                return glom(config, path)
            return {k: _resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_resolve(item) for item in value]
        else:
            return value

    return {k: _resolve(v) for k, v in config.items()}


def load_config(json_path: Path) -> dict:
    """Load JSON config."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_render_context(
    config: dict, user_data: dict[str, str], scale: float = SCALE_PX_MM
) -> dict[str, dict]:
    """
    Build final data structure for rendering the page.
    """

    resolved_config = resolve_ref(config)

    render_context = {}

    for element_key, element in resolved_config["elements"].items():
        if element_key not in user_data:
            continue

        font = element["font"]
        color = element["color"]
        position = element["position"]
        text = user_data[element_key]

        # Apply scaling to positions and font sizes
        scaled_position = scale_position(position, scale)
        scaled_font_size = int(font["size"] * scale)

        # Create new entry
        render_context[element_key] = {
            "text": str(text),
            "font": {"name": font["name"], "size": scaled_font_size},
            "color": {
                "hex": color,
                "rgb": hex_to_rgb(color),
            },
            "position": scaled_position,
        }

    return render_context


def build_dial_context(
    config: dict, user_data: dict[str, str], scale: float = SCALE_PX_MM
) -> dict[str, dict]:
    """
    Build dial data structure for counting data (predict)"""

    # Извлекаем настройки
    fonts = config["fonts"]
    colors = config["colors"]
    geometry = config["geometry"]
    center = geometry["center"]

    # Преобразуем цвета из HEX в RGB
    colors_rgb = {
        "main_dial": {
            "hex": colors["main_dial"],
            "rgb": hex_to_rgb(colors["main_dial"]),
        },
        "inner_dial": {
            "hex": colors["inner_dial"],
            "rgb": hex_to_rgb(colors["inner_dial"]),
        },
    }

    # Создаем результирующий словарь
    context = {}

    # Рассчитываем позиции
    main_radius = geometry["main_dial"]["radius"]
    inner_radius = geometry["inner_dial"]["radius"]
    start_angle = geometry["start_angle"]
    angle_step = geometry["angle_step"]

    # Обрабатываем все данные в порядке их следования
    for idx, (key, value) in enumerate(user_data.items()):
        angle = start_angle + idx * angle_step

        if key.startswith("main_"):
            # Main dial settings
            radius = main_radius
            font_settings = {
                "name": fonts["main_dial"]["name"],
                "size": int(fonts["main_dial"]["size"] * scale),
            }
            color_settings = colors_rgb["main_dial"]
        else:
            # Inner dial settings
            radius = inner_radius
            font_settings = {
                "name": fonts["inner_dial"]["name"],
                "size": int(fonts["inner_dial"]["size"] * scale),
            }
            color_settings = colors_rgb["inner_dial"]

        # Рассчитываем позицию и масштабируем её
        raw_position = calculate_position(center, radius, angle)
        scaled_position = scale_position(raw_position, scale)

        context[key] = {
            "text": str(value),
            "font": font_settings,
            "color": color_settings,
            "position": scaled_position,
        }

    return context


def build_pythagorian_context(
    config: dict, user_data: dict[str, str], scale: float = SCALE_PX_MM
) -> dict[str, dict]:
    """
    Build dial data structure for pythagorian_table
    """

    fonts = config["fonts"]
    colors = config["colors"]
    geometry = config["geometry"]
    initial_point = geometry["initial_point"]
    sidelength = geometry["square"]

    colors_rgb = {
        "pythagorian": {
            "hex": colors["pythagorian"],
            "rgb": hex_to_rgb(colors["pythagorian"]),
        },
    }

    context = {}

    start_x = initial_point[0] + sidelength / 2
    start_y = initial_point[1] + sidelength / 2

    # Обрабатываем все данные в порядке их следования
    for idx, (key, value) in enumerate(user_data.items()):
        current_x = start_x + (idx % 3) * sidelength
        current_y = start_y + (idx // 3) * sidelength

        font_settings = {
            "name": fonts["pythagorian"]["name"],
            "size": int(fonts["pythagorian"]["size"] * scale),
        }
        color_settings = colors_rgb["pythagorian"]
        raw_position = (current_x, current_y)
        scaled_position = scale_position(raw_position, scale)

        context[key] = {
            "text": str(value),
            "font": font_settings,
            "color": color_settings,
            "position": scaled_position,
        }

    return context
