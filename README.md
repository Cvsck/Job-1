# Создание виртуального окружения
python -m venv .venv

# Активация виртуального окружения (на Windows)
.venv\Scripts\activate

# Push в основную ветку и ветку разработки
git push origin main
git push origin develop

# Создание init файла для src
New-Item -Path 'src/__init__.py' -ItemType File

# Создание init файла для тестов
New-Item -Path 'tests/__init__.py' -ItemType File

# Установка необходимых пакетов
pip install isort
pip install black
pip install flake8
pip install requests
pip install python-dotenv
pip install mypy
pip install poetry
python.exe -m pip install --upgrade pip
pip install pandas
pip install pandas openpyxl
python -m pip install eodhd -U
pip install pytest
pip install pytest-cov
pip install pytest-html

# Запуск тестов с отчетом покрытия и HTML отчетом
pytest --cov=src --cov-report=html:htmlcov --html=report.html
# Создание модулей
main
reports
services
utils
# Приведение модулей к PEP8
# Пример использования инструментов для приведения кода к стандарту PEP8
flake8 src/main.py
isort src/main.py
black src/main.py
mypy src/main.py
# В папке Tests добавлены тесты к модулям
