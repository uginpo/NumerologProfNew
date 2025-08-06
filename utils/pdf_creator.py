from pathlib import Path

from loguru import logger

from report_storage.report_classes import TextPageData
from utils.pdf_utility import CustomPDF


class ReportCreatingError(Exception):
    pass


def generate_pdf(
    output_path: Path,
    page_data: dict[str, dict],
    template: Path,
    text_data: TextPageData | None = None,
) -> Path:
    """Создает файлы отчетов в формате pdf"""
    pdf = CustomPDF()

    pdf.create_image_page(page_data=page_data, template=str(template))

    if text_data:
        pdf.create_text_pages(text_data)

    pdf.output(str(output_path))
    if output_path.exists():
        return output_path

    logger.error(f"Отчет {output_path.name} не удалось создать")
    raise ReportCreatingError(f"Ошибка создания отчета {output_path.name}")
