# Job-1
1.  Организация проекта
'''
python -m venv .venv
.venv\Scripts\activate (на Windows:)
git push origin main
git push origin develop
New-Item -Path 'src/__init__.py' -ItemType File
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
pytest --cov=src --cov-report=html:htmlcov --html=report.html

'''
2. Создание модулей:
'''
main
reports
services
utils
views
'''
3. Приведение модулей к PEP8:
'''
Пример:
flake8 src/main.py
isort src/main.py
black src/main.py
mypy src/main.py
'''
4. В папке Tests добавлены тесты к модулям