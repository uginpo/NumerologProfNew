#!/bin/bash

DOT_FILE="call_graph.dot"
PNG_FILE="call_graph.png"

# Проверка Graphviz
if ! command -v dot &> /dev/null; then
    echo "❌ dot не установлен. Выполни: brew install graphviz"
    exit 1
fi

echo "🔍 Ищем .py файлы..."

# Собираем файлы через NUL-разделители (безопасно для пробелов)
readarray -t PYTHON_FILES < <(find . -type f -name "*.py" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.venv/*" \
  -not -path "*/venv/*" \
  -not -path "*/env/*" \
  -not -path "*/tests/*" \
  -not -name "test_*.py" \
  -print0 | xargs -0 printf '%s\n')

# Проверка
if [ ${#PYTHON_FILES[@]} -eq 0 ]; then
    echo "❌ Не найдено .py файлов."
    exit 1
fi

echo "📦 Найдено файлов: ${#PYTHON_FILES[@]}"
echo "📄 Примеры:"
printf '  %s\n' "${PYTHON_FILES[@]}" | head -5
echo

# Экспортируем PYTHONPATH
export PYTHONPATH=.

echo "🎨 Генерируем граф вызовов..."
python -m pyan "${PYTHON_FILES[@]}" \
  --uses \
  --defines \
  --grouped \
  --colored \
  --annotated \
  --dot \
  --output "$DOT_FILE"

if [ $? -ne 0 ]; then
    echo "❌ Ошибка при генерации графа."
    exit 1
fi

echo "🖼️  Конвертируем в PNG..."
dot -Tpng "$DOT_FILE" -o "$PNG_FILE"

echo "✅ Готово! Граф вызовов сохранён в:"
echo "   • $DOT_FILE"
echo "   • $PNG_FILE"
