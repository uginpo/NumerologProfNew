from pathlib import Path

# Logs
INFO_FILE = Path("logs/info.log")
DEBUG_FILE = Path("logs/debug.log")
ERROR_FILE = Path("logs/error.log")

# Templates
FULLSTAR = {
    "json": Path("config/pages/fullstar.json"),
    "jpg": Path("templates/fullstar.jpg"),
    "tex_templates": {"personality": Path("latex_storage/fullstar.tex")},
}
TRIANGLES = {
    "json": Path("config/pages/triangles.json"),
    "personality": {
        "jpg": Path("templates/personality.jpg"),
        "tex": Path("latex_storage/personality.tex"),
    },
    "spirituality": {
        "jpg": Path("templates/spirituality.jpg"),
        "tex": Path("latex_storage/spirituality.tex"),
    },
    "money": {
        "jpg": Path("templates/money.jpg"),
        "tex": Path("latex_storage/money.tex"),
    },
    "relationship": {
        "jpg": Path("templates/relationship.jpg"),
        "tex": Path("latex_storage/relationship.tex"),
    },
    "health": {
        "jpg": Path("templates/health.jpg"),
        "tex": Path("latex_storage/health.tex"),
    },
}
COUPLE = {
    "json": Path("config/pages/couple.json"),
    "jpg": Path("templates/couple.jpg"),
}

PREDICT = {
    "json": [
        Path("config/pages/predict.json"),
        Path("config/pages/dial.json"),
    ],
    "jpg": Path("templates/predict.jpg"),
}

PITHAGORIAN_TABLE = {
    "json": Path("config/pages/pythagorian_table.json"),
    "jpg": Path("templates/pythagorian_table.jpg"),
}
OUTPUT_PATH = Path("output")

"""
Размеры страницы A4:
В миллиметрах: 210 мм × 297 мм .
В пикселях: 2380 × 3368 пикселей .
    """
SCALE_PX_MM: float = 0.0882
