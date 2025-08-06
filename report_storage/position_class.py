from config.settings import SCALE_PX_MM


class BasePositions:
    """Базовый класс для хранения и преобразования координат"""

    def __init__(
        self, coordinates_px: dict[str, tuple[int, int]], scale: float = SCALE_PX_MM
    ):
        self.scale = scale
        self._coordinates_px = coordinates_px

    @property
    def positions_mm(self) -> dict[str, tuple[float, float]]:
        """Преобразует координаты из пикселей в миллиметры"""
        return {
            key: (value[0] * self.scale, value[1] * self.scale)
            for key, value in self._coordinates_px.items()
        }

    def get_all_positions(self) -> dict[str, tuple[float, float]]:
        """Возвращает полный словарь позиций в миллиметрах"""
        return self.positions_mm


class TrianglePositions(BasePositions):
    """Класс для хранения координат страницы 'Треугольник'"""

    def __init__(self, scale: float = SCALE_PX_MM):
        coordinates_px = {
            "vertex": (1190, 1327),
            "mat_vertex": (414, 2856),
            "pat_vertex": (1966, 2856),
            "inv_vertex": (1190, 2856),
            "inv_pat_vertex": (692, 2311),
            "inv_mat_vertex": (1688, 2311),
        }
        super().__init__(coordinates_px, scale)


class FullStarPositions(BasePositions):
    """Класс для хранения координат страницы 'Полная Звезда'"""

    def __init__(self, scale: float = SCALE_PX_MM):
        coordinates_px = {
            # header
            "header_text": (1190, 296),
            # main arcanes
            "personality": (184, 1291),
            "spirituality": (1190, 527),
            "money": (2196, 1291),
            "relationship": (1914, 2554),
            "health": (466, 2554),
            "mission": (1034, 1683),
            "mission_err": (1190, 1683),
            "mission_all": (1346, 1683),
            # errors arcanes
            "pat_male_line_err": (896, 1291),
            "mat_male_line_err": (1484, 1291),
            "pat_female_line_err": (1699, 1849),
            "doom_err": (1190, 2201),
            "mat_female_line_err": (687, 1849),
            # footer arcanes
            "foot_personality": (781, 2993),
            "foot_spirituality": (985, 2993),
            "foot_money": (1190, 2993),
            "foot_relationship": (1395, 2993),
            "foot_health": (1599, 2993),
            # trianges arcanes
            "personal_inv_vertex": (927, 1614),
            "personal_inv_mat_vertex": (541, 1291),
            "personal_inv_pat_vertex": (413, 1614),
            "spirituality_inv_vertex": (1190, 1412),
            "spirituality_inv_mat_vertex": (1388, 949),
            "spirituality_inv_pat_vertex": (992, 949),
            "money_inv_vertex": (1454, 1614),
            "money_inv_mat_vertex": (1968, 1614),
            "money_inv_pat_vertex": (1840, 1291),
            "relationship_inv_vertex": (1346, 1904),
            "relationship_inv_mat_vertex": (1454, 2370),
            "relationship_inv_pat_vertex": (1780, 2178),
            "health_inv_vertex": (1034, 1904),
            "health_inv_mat_vertex": (601, 2178),
            "health_inv_pat_vertex": (927, 2370),
        }
        super().__init__(coordinates_px, scale)


"""
---------------------------------------------------
Вариант использования
---------------------------------------------------
# Создаем объект StarPositions
star_positions = StarPositions(scale=SCALE_PX_MM)

# Получаем полный словарь позиций в миллиметрах
all_star_positions = star_positions.get_all_positions()

# Выводим все координаты для страницы "Звезда"
print("Координаты для страницы 'Звезда':")
for key, value in all_star_positions.items():
    print(f"  {key}: {value}")

# Создаем объект TrianglePositions
triangle_positions = TrianglePositions(scale=SCALE_PX_MM)

# Получаем полный словарь позиций в миллиметрах
all_triangle_positions = triangle_positions.get_all_positions()

# Выводим все координаты для страницы "Треугольник"
print("Координаты для страницы 'Треугольник':")
for key, value in all_triangle_positions.items():
    print(f"  {key}: {value}")
        """
