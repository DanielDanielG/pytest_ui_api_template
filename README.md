# 🛍️ Автотесты для интернет-магазина МТС (UI + API)

> Комплексный фреймворк для автоматизированного тестирования веб-интерфейса и API интернет-магазина МТС.

## 📋 О проекте
Проект демонстрирует навыки автоматизации тестирования на стеке **Python + pytest**. Реализован подход **Page Object Model**, настроена генерация отчетов **Allure**, предусмотрена работа с конфигурациями и фикстурами.

### 🔍 Что тестируется
- ✅ Регистрация и авторизация пользователей (UI)
- ✅ Поиск и фильтрация товаров (UI)
- ✅ Работа с корзиной и оформлением заказа (UI)
- ✅ Валидация ответов сервера (API)
- ✅ Интеграция UI-действий с проверками через API

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
