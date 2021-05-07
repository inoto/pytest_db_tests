# Desctiption
This is a technical task made with **pytest** and **sqlite**. Nothing super special.

# Given requirements
* Python version – 3.8
* Тесты должны быть написаны с использованием фрейморка pytest
* В качестве параметризации использовать pytest.mark.parametrize или хук pytest_generate_tests.
* В результате прогона должно получиться 600 тестов.
* В результате выполнения задания должно быть по крайней мере следующее:
    - Скрипт, создающий и заполняющий исходную базу данных
    - Python-модуль, содержащий тесты
    - (Опционально) conftest.py, содержащий фикстуры и хуки
* Стиль кода – PEP8.

# Usage
## Prepare environment
`pip install -r requirements.txt`

## Run
Using terminal: `python -m pytest tests/test_ships.py`.

Or you can use saved PyCharm configuration named `pytest test_ships`.

Also you can add option `-tb=no` to reduce output size removing tracebacks.
