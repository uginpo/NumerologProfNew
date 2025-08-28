#!/bin/bash

# Имя выходного файла
OUTPUT_FILE="project_structure.txt"

# Проверяем, установлен ли tree
if ! command -v tree &> /dev/null; then
    echo "❌ Ошибка: команда 'tree' не установлена."
    echo "Установите: sudo apt install tree (Ubuntu/Debian) или brew install tree (macOS)"
    exit 1
fi

echo "📂 Структура проекта: $(basename $(pwd))"
echo

# Генерируем структуру и выводим в терминал + записываем в файл
tree \
  -I '.git|__pycache__|venv|.venv|env|.pytest_cache|.mypy_cache|*.pyc|output|*.pyo|*.pyd|.*' \
  --prune \
  --dirsfirst

# Сохраняем ту же структуру в файл
tree \
  -I '.git|__pycache__|venv|.venv|env|.pytest_cache|.mypy_cache|*.pyc|output|*.pyo|*.pyd|.*' \
  --prune \
  --dirsfirst > "$OUTPUT_FILE"

# Проверяем, успешно ли записано
if [ $? -eq 0 ]; then
    echo
    echo "✅ Готово."
    echo "📄 Структура сохранена в файл: ./$OUTPUT_FILE"
else
    echo
    echo "❌ Ошибка при сохранении в файл."
fi
