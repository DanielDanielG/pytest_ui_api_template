@echo off
:: ============================================
:: СКРИПТ ЗАПУСКА АВТОТЕСТОВ С ALLURE
:: ============================================
:: Автоматическая очистка, запуск тестов,
:: сохранение истории и открытие отчёта
:: ============================================

:: Настройка путей (относительные)
set results=allure-results
set report=allure-report
set history=%report%\history

:: Шаг 1: Очистка папки с предыдущими результатами тестов
echo [1/4] Clean allure-results
rmdir /S /Q %results% 2>nul

:: Шаг 2: Запуск тестов pytest с сохранением результатов
echo [2/4] Start test on pytest...
python -m pytest --alluredir=%results%


:: Шаг : Генерация нового HTML-отчёта Allure
echo [3/4] Generate Allure...
allure serve  %results% 

:: Шаг 6: Открытие отчёта в браузере по умолчанию
echo [4/4] Open Allure on browser
allure serve %report%

echo.
echo ============================================
echo Allure open on browser
echo ============================================
pause