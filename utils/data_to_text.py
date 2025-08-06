def save_to_text_file(file_path, data) -> None:
    """
    Сохраняет данные в текстовый файл, формируя их построчно.
    :param file_path: Путь к файлу для записи (строка).
    :param data: Список строк для записи в файл.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            # Записываем каждую строку из списка в файл
            for line in data:
                # Добавляем перевод строки (\n) после каждой записи
                file.write(str(line) + "\n")
    except Exception as e:
        raise Exception(f"Произошла ошибка при записи файла {e}")
