from __future__ import annotations

from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Iterable

COMMON_LOGS = (
    ("/var/log/syslog", "Системный лог"),
    ("/var/log/messages", "Сообщения системы"),
    ("/var/log/auth.log", "Авторизация"),
    ("/var/log/kern.log", "Лог ядра"),
    ("/var/log/dpkg.log", "Установка пакетов"),
)


def existing_logs() -> list[tuple[str, str]]:
    """Возвращает существующие стандартные Linux-логи."""
    return [(path, title) for path, title in COMMON_LOGS if Path(path).is_file()]


def tail_lines(path: str | Path, limit: int = 200) -> list[str]:
    """Читает последние строки файла без загрузки всего файла в память."""
    if limit < 1 or limit > 5000:
        raise ValueError("Количество строк должно быть от 1 до 5000.")

    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with file_path.open("r", encoding="utf-8", errors="replace") as source:
        return list(deque(source, maxlen=limit))


def filter_lines(lines: Iterable[str], query: str) -> list[str]:
    """Фильтрует строки без учета регистра."""
    normalized = query.strip().casefold()
    if not normalized:
        return list(lines)
    return [line for line in lines if normalized in line.casefold()]


def file_info(path: str | Path) -> dict[str, str]:
    """Возвращает информацию о выбранном файле."""
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    stat_result = file_path.stat()
    return {
        "path": str(file_path),
        "size": human_size(stat_result.st_size),
        "modified": datetime.fromtimestamp(stat_result.st_mtime).strftime("%d.%m.%Y %H:%M:%S"),
    }


def human_size(value: int) -> str:
    """Переводит байты в удобный формат."""
    size = float(value)
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if size < 1024 or unit == "ТБ":
            return f"{int(size)} {unit}" if unit == "Б" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"


def export_text(destination: str | Path, text: str) -> Path:
    """Сохраняет результат в текстовый файл."""
    output = Path(destination).expanduser()
    output.write_text(text, encoding="utf-8")
    return output
