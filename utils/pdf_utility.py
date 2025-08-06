from fpdf import FPDF

from report_storage.report_classes import TextPageData


# Класс PDF
class CustomPDF(FPDF):
    def __init__(self, orientation="P", unit="mm", format="a4"):
        # Вызываем конструктор родительского класса с указанными параметрами
        super().__init__(orientation="P", unit="mm", format="a4")
        self._needs_background = False
        self._background_color = (0, 0, 0)
        # добавление пользовательских шрифтов
        self.add_font(
            "bebas_regular",
            "",
            "report_storage/fonts/BebasNeue-Regular.ttf",
            uni=True,
        )
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

    def add_page(self, orientation="P", format="mm", same=False):
        super().add_page(orientation="P", format="a4")
        if not same:
            self._needs_background = True
            self._fill_page_with_color(self._background_color)

        if self._needs_background:
            self._fill_page_with_color(self._background_color)

    def create_image_page(self, page_data: dict[str, dict], template: str):
        self._needs_background = False
        self.add_page()
        self.image(template, x=0, y=0, w=self.w)

        for _, element in page_data.items():
            text = element["text"]
            font = element["font"]
            color = element["color"]["rgb"]
            position = element["position"]

            self._add_text_element(text, font, color, position)

    def _add_text_element(
        self,
        text: str,
        font: dict,
        color: tuple[int, int, int],
        position: tuple[float, float],
    ):
        self.set_font(font["name"], size=font["size"])
        self.set_text_color(*color)

        text_width = self.get_string_width(text)
        text_height = self.font_size

        centered_x = position[0] - (text_width / 2)
        centered_y = position[1] - (text_height / 2)

        self.text(centered_x, centered_y, text)

    def create_text_pages(self, page_data: TextPageData):
        # Установка общего цвета текста
        self.set_text_color(*page_data.text_color)
        self._background_color = page_data.background_color
        self._needs_background = True

        old_title = ""
        for section in page_data.sections:
            # Проверяем место на странице перед добавлением заголовка раздела
            if self.y + 20 > self.h - 20:  # Если нет места для нового контента
                # Создаем новую страницу с цветом фона
                self.add_page()

            # Устанавливаем шрифт заголовка раздела
            self.set_font(
                str(section.title_font.get("name")),  # type: ignore
                str(section.title_font.get("style")),  # type: ignore
                int(section.title_font.get("size")),  # type: ignore
            )

            if old_title != section.title:
                # Выводим название раздела только если оно не повторяется
                old_title = section.title
                self.cell(0, 10, section.title, 0, 1, "C")
                self.ln(5)  # Отступ после названия раздела
                if self.y + 20 > self.h - 20:  # Если нет места
                    #    Создаем новую страницу с цветом фона
                    self.add_page()

            # Устанавливаем шрифт подзаголовка
            if section.subtitle and section.subtitle_font:
                self.set_font(
                    str(section.subtitle_font.get("name")),  # type: ignore
                    str(section.subtitle_font.get("style")),  # type: ignore
                    int(section.subtitle_font.get("size")),  # type: ignore
                )
                # Выводим подзаголовок
                self.cell(0, 10, section.subtitle, 0, 1, "C")
                self.ln(2)  # Отступ после подзаголовка
                if self.y + 20 > self.h - 20:  # Если нет места
                    # Создаем новую страницу с цветом фона
                    self.add_page()

            # Устанавливаем шрифт основного текста
            self.set_font(
                str(section.info_font.get("name")),  # type: ignore
                str(section.info_font.get("style")),  # type: ignore
                int(section.info_font.get("size")),  # type: ignore
            )

            # Уменьшаем интервал между строками
            line_height = (
                self.font_size * 1.5
            )  # Высота строки равна 1.2 от размера шрифта

            # Обработка информации внутри раздела
            for info_item in section.info:
                # Проверяем, достаточно ли места на странице
                # Выводим информацию через multi_cell
                self.multi_cell(0, line_height, info_item, align="L")
                # Отступ между элементами информации
                self.ln(self.font_size * 0.3)

                if self.y + 20 > self.h - 20:  # Если нет места
                    # Создаем новую страницу с цветом фона
                    self.add_page()
            self.ln(5)

    def _fill_page_with_color(self, background_color):
        """Создает новую страницу с заданным цветом фона"""
        self.set_fill_color(*background_color)
        # Прямоугольник со страницей, заполненный цветом
        self.rect(0, 0, self.w, self.h, "F")
        self.set_y(10)  # Начинаем с верхней части страницы

    def _add_centered_text(
        self, x: float, y: float, text: str, text_width: int, text_height: int
    ):
        """
        Выводит текст точно по центру относительно координаты x.

        Args:
            x (float): Центральная координата X.
            y (float): Координата Y, где должен начаться текст.
            text (str): Текст для вывода.
            text_width (int): Ширина текста.

        """
        # Корректируем координату x для центрирования текста
        centered_x = x - (text_width / 2)
        centered_y = y - (text_height / 2)

        # Устанавливаем позицию курсора
        self.set_xy(centered_x, centered_y)

        # Выводим текст
        self.cell(w=text_width, h=self.font_size,
                  txt=text, align="C")  # type: ignore
        self.set_xy(self.w, self.h)

    def accept_page_break(self):
        """Указываем, что следующая страница должна быть с заливкой"""
        self._needs_background = True
        return True  # Разрешаем разрыв страницы
