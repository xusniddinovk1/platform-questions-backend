import logging

LoggerType = logging.Logger


def get_logger_service(path: str = __name__) -> LoggerType:
    """
    Функция для создания логгера.

    Args:
        path (str): Путь к месту, где будет использоваться логгер.

    Returns:
        LoggerType: Логгер c указанным путем.
    """
    return logging.getLogger(path)
