def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Перевод цвета из формата hex
    в формат rgb
    Args:
        hex_color (str): hex-format
    Raises:
        ValueError: _description_
        ValueError: _description_
    Returns:
        tuple: rgb-format
    """
    # Убираем символ '#' если он есть
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    # Проверяем длину hexadecimal-кода
    if len(hex_color) not in [3, 6]:
        raise ValueError(
            f"Неверный HEX-код {hex_color=}. Необходимо 3/6 символов.")

    # Если используется формат(3 символа), разворачиваем его до 6 символов
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])

    try:
        # Преобразуем каждые два символа в десятичное число
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError("Некорректный HEX-код.")


def repr_data(data_to_print: dict | list | None) -> str | None:
    """
    Формирует строку для вывода данных о словаре или списке в логах.
    Args:
        data_to_print (dict | list): Данные для представления
        (словарь или список).
    Returns:
        str | None: Строковое представление данных или None,
        если тип данных не поддерживается.
    """
    if not isinstance(data_to_print, (dict, list)) or not data_to_print:
        return None

    indent = " " * 4
    res = ["("]

    if isinstance(data_to_print, dict):
        for key, value in data_to_print.items():
            res.append(f"{indent}{key}: {value!r}")
    elif isinstance(data_to_print, list):
        for item in data_to_print:
            if isinstance(item, dict):
                for key, value in item.items():
                    res.append(f"{indent}{key}: {value!r}")
            else:
                res.append(f"{indent}- {item!r}")

    res.append(")")
    return "\n".join(res)
