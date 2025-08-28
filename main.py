# main.py

from pathlib import Path

from loguru import logger

from business_logic.arcanes_classes import Scenario
from input_module.input_data import enter_data
from src.main_reports import (collect_adult_report, collect_child_report,
                              collect_couple_report)


class MainReportError(Exception):
    pass


def main() -> None:
    scenario: Scenario = enter_data()
    logger.debug(f"{scenario=}")

    match scenario.scenario:
        case "adult":
            report: Path = collect_adult_report(scenario.clients[0])

        case "child":
            report: Path = collect_child_report(scenario.clients[0])

        case "couple":
            report: Path = collect_couple_report(scenario)

    if report.exists():
        logger.info("Программа успешно завершила работу.")
    else:
        logger.error(f"Error when creating the report {report}")
        raise MainReportError(f"Error when creating the report {report}")


if __name__ == "__main__":
    from utils.log_utils import configure_logger

    configure_logger()
    main()
