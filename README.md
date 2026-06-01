# LogView

**LogView** — графическая Linux-утилита для просмотра и фильтрации логов.

В интерфейсе есть:
- просмотр стандартных Linux-логов;
- открытие собственного текстового файла;
- вывод последних строк;
- фильтрация по тексту;
- сохранение результата;

## Установка зависимостей

Войти в root:

```bash
su
```

Установить необходимые пакеты:

```bash
apt update
apt install python3 python3-tk git -y
```

Выйти из root:

```bash
exit
```

## Скачивание проекта

После загрузки проекта в свой GitHub-репозиторий выполнить:

```bash
git clone https://github.com/USERNAME/LogView.git
cd LogView
```

## Запуск

```bash
./LogView
```

`pip`, `venv` и дополнительные Python-библиотеки не нужны.

### Если проект загружался на GitHub через сайт

GitHub может убрать право на запуск у файла. Тогда один раз выполнить готовую команду:

```bash
chmod +x LogView && ./LogView
```

После этого следующие запуски выполняются обычной командой:

```bash
./LogView
```

## Проверка тестов

```bash
python3 -m unittest discover -s tests -v
```

## Структура

```text
LogView/
├── LogView
├── logview_gui.py
├── logview_core.py
├── README.md
├── LICENSE
├── .gitignore
└── tests/
    └── test_core.py
```
