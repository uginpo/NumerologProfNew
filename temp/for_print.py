from fpdf import FPDF


class CustomPDF(FPDF):
    def __init__(self, orientation="P", unit="mm", format="A4"):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self._needs_background = False
        self._background_color = (0, 0, 0)
        self.add_font(
            "roboto_bold",
            "",
            "report_storage/fonts/Roboto Mono Bold for Powerline.ttf",
            uni=True,
        )
        self.add_font(
            "roboto_medium",
            "",
            "report_storage/fonts/Roboto Mono Medium for Powerline.ttf",
            uni=True,
        )
        self.add_font(
            "roboto_regular",
            "",
            "report_storage/fonts/Roboto Mono for Powerline.ttf",
            uni=True,
        )
        self.add_font(
            "roboto_light",
            "",
            "report_storage/fonts/Roboto Mono Light for Powerline.ttf",
            uni=True,
        )

    def add_page(self, orientation="", format="", same=False):
        """Переопределяем add_page, чтобы добавлять заливку при необходимости"""
        super().add_page(orientation=orientation, format=format)
        if not same:
            self._needs_background = True
            self._fill_page_with_color(self._background_color)

        if self._needs_background:
            self._fill_page_with_color(self._background_color)
            # self._needs_background = False  # Сбрасываем флаг

    def create_image_page(self, page_data: dict):
        """
        Создает страницу с фоновым изображением и добавляет текстовые элементы.
        """
        # Добавляем страницу с фоновым изображением
        self.add_page()
        self.image(page_data["background_image_path"], x=0, y=0, w=self.w)

        # Добавляем текстовые элементы
        for element_key, element in page_data.items():
            if element_key == "background_image_path":
                continue  # Пропускаем путь к изображению

            text = element["text"]
            font = element["font"]
            color = element["color"]["rgb"]  # RGB-цвет
            position = element["position"]

            # Добавляем текст на страницу
            self._add_text_element(text, font, color, position)

    def _add_text_element(
        self,
        text: str,
        font: dict,
        color: Tuple[int, int, int],
        position: Tuple[float, float],
    ):
        """
        Добавляет текстовый элемент на страницу.
        """
        # Устанавливаем шрифт
        self.set_font(font["name"], size=font["size"])

        # Устанавливаем цвет текста
        self.set_text_color(*color)

        # Получаем размеры текста
        text_width = self.get_string_width(text)
        text_height = self.font_size

        # Выравниваем текст по центру
        centered_x = position[0] - (text_width / 2)
        centered_y = position[1] - (text_height / 2)

        # Выводим текст
        self.text(centered_x, centered_y, text)

    def _fill_page_with_color(self, background_color):
        """Создает новую страницу с заданным цветом фона"""
        self.set_fill_color(*background_color)
        # Прямоугольник со страницей, заполненный цветом
        self.rect(0, 0, self.w, self.h, "F")
        self.set_y(10)  # Начинаем с верхней части страницы

    def accept_page_break(self):
        """Указываем, что следующая страница должна быть с заливкой"""
        self._needs_background = True
        return True  # Разрешаем разрыв страницы
