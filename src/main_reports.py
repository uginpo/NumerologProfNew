from pathlib import Path

from loguru import logger

from business_logic.arcanes_classes import Client, Scenario

from .reports_collection import (
    collect_predict_report,
    collect_triangles_adult,
    collect_triangles_child,
    create_couple_report,
    create_fullstar_report,
    create_pythagorian_table,
)


class ReportGenerationError(Exception):
    pass


def _has_report(report: Path | list[Path] | None) -> None:
    if not report:
        logger.error(f"Не создан отчет {report}")
        raise ReportGenerationError(f"Ошибка при генерации отчета {report}")


def collect_adult_report(client_info: Client) -> list[Path]:
    """Собирает блок отчетов для одного взрослого клиента
    и возвращает список сформированных файлов отчетов.
    """

    adult_report = []

    fullstar_report = create_fullstar_report(client_info=client_info)
    _has_report(report=fullstar_report)
    adult_report.append(fullstar_report)

    triangle_reports = collect_triangles_adult(client_info=client_info)
    _has_report(report=triangle_reports)
    adult_report.append(triangle_reports)

    predict_report = collect_predict_report(client_info=client_info)
    _has_report(report=predict_report)
    adult_report.append(predict_report)

    pythagorian_report = create_pythagorian_table(client_info=client_info)
    _has_report(report=pythagorian_report)
    adult_report.append(pythagorian_report)

    logger.debug("Все отчеты на взрослого клиента созданы")

    return adult_report


def collect_child_report(client_info: Client) -> list[Path]:
    """Собирает блок отчетов для ребенка
    и возвращает список сформированных файлов отчетов.
    """

    child_report = []

    triangle_reports = collect_triangles_child(
        client_info=client_info, pointers=["personality", "money"]
    )
    _has_report(report=triangle_reports)
    child_report.append(triangle_reports)

    pythagorian_report = create_pythagorian_table(client_info=client_info)
    _has_report(report=pythagorian_report)
    child_report.append(pythagorian_report)

    logger.debug("Все отчеты на ребенка созданы")

    return child_report


def collect_couple_report(scenario: Scenario) -> list[list[Path]]:
    """Собирает блок отчетов для пары
    и возвращает список сформированных файлов отчетов.
    """

    couple_report = []
    for client_info in scenario.clients:
        client_report = collect_adult_report(client_info=client_info)
        _has_report(report=client_report)
        couple_report.append(client_report)

    couple_relation_report = create_couple_report(scenario=scenario)
    _has_report(report=couple_relation_report)
    couple_report.append(couple_relation_report)

    logger.debug("Все отчеты на пару созданы")

    return couple_report
