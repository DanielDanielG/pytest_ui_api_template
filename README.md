# API_UI тесты Магазин МТС

## Автоматизация тестирования на python

### Шаги
1. Склонировать проект 'git clone https://github.com/имя_пользователя/
   pytest_ui_api_template.git'
2. Установить зависимости
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'

Альтарнативный вариант автоматический запуск тестов UI (pytest+allure)
Через BAT-файлы (Windows)
Все тесты: Test MTS\AUTO_API+UI_PY+AL.bat
UI тесты: Test MTS\Test UI\AUTO_UI_PY+AL.bat
API тесты: Test MTS\Test API\AUTO_API_PY+AL.bat

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Струткура:
├── API/             # API клиенты
├── pages/           # Page Objects
├── Test MTS/
│   ├── Test UI/     # UI тесты
│   └── Test API/    # API тесты
├── conftest.py      # Фикстуры
├── requirements.txt # Зависимости
└── README.md        # Документация

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Тест-план проекта Интернет-магазин МТС](https://dantestit.yonote.ru/share/3909c880-72b5-49ff-ab7c-01d1becf9107#h-testovaya-dokumentaciya

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager
