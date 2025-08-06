from pathlib import Path

# Logs
INFO_FILE = Path("logs/info.log")
DEBUG_FILE = Path("logs/debug.log")
ERROR_FILE = Path("logs/error.log")

# Templates
FULLSTAR = {
    "json": Path("config/pages/fullstar.json"),
    "jpg": Path("templates/fullstar.jpg"),
}
TRIANGLES = {
    "json": Path("config/pages/triangles.json"),
    "personality": Path("templates/personality.jpg"),
    "spirituality": Path("templates/spirituality.jpg"),
    "money": Path("templates/money.jpg"),
    "relationship": Path("templates/relationship.jpg"),
    "health": Path("templates/health.jpg"),
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

OUTPUT_PATH = Path("output")

"""
Размеры страницы A4:
В миллиметрах: 210 мм × 297 мм .
В пикселях: 2380 × 3368 пикселей .
    """
SCALE_PX_MM: float = 0.0882
