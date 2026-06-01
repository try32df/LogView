# LogView

**LogView** — графическая Linux-утилита для просмотра и фильтрации логов.

---

# Полная пошаговая установка и запуск

## 1. Войти в root

```bash
su
```

Введите пароль root.

---

## 2. Установить зависимости

```bash
apt update
apt install python3 python3-tk git -y
```

---

## 3. Выйти из root

```bash
exit
```

---

## 4. Скачать проект с GitHub

```bash
git clone https://github.com/USERNAME/LogView.git
```

---

## 5. Перейти в папку проекта

Важно заходить именно через `~`:

```bash
cd ~/LogView
```

---

## 6. Выдать право на запуск

После скачивания с GitHub файл запуска может быть без права выполнения.

Поэтому нужно выполнить:

```bash
chmod +x LogView
```

---

## 7. Запустить программу

```bash
./LogView
```

---

# Коротко все команды вместе

```bash
su
apt update
apt install python3 python3-tk git -y
exit
git clone https://github.com/USERNAME/LogView.git
cd ~/LogView
chmod +x LogView
./LogView
```

---

# Возможности программы

LogView позволяет:
- просматривать Linux-логи;
- открывать `.txt` и `.log` файлы;
- фильтровать строки по тексту;
- сохранять результат;
- работать через GUI интерфейс;
- закрывать программу через кнопку **Выход** или **✕**.

---

# Структура проекта

```text
LogView/
├── LogView
├── logview_gui.py
├── logview_core.py
├── README.md
├── LICENSE
└── tests/
    └── test_core.py
```

---

# Используемые технологии

- Python 3
- Tkinter
- pathlib
- Linux logs
- GitHub

---

# Автор

Артем, Мария
