# Звіт до Лабораторної роботи №5: Бізнес-логіка, сервіси, модульне тестування

## 1. Реалізовані бізнес-сценарії
У рамках розробки системи управління бібліотекою (Library System) було реалізовано наступні критичні сценарії:
1. **Реєстрація користувача:** Створення нового читача з перевіркою унікальності email та встановленням ліміту на кількість взятих книг (максимум 5).
2. **Додавання книги:** Поповнення каталогу бібліотеки. Якщо книга з таким ISBN вже існує, збільшується кількість доступних примірників.
3. **Пошук книги:** Можливість знайти книгу за назвою з використанням часткового збігу (regex у MongoDB).
4. **Видача книги:** Комплексний сценарій, який перевіряє: наявність користувача, доступність примірників книги та поточні ліміти читача. У разі успіху створюється запис про видачу (BorrowRecord).
5. **Повернення книги:** Закриття активного запису про видачу та повернення примірника в загальний доступ каталогу.

## 2. Структура коду (Controller-Service-Repository)
Проект організовано за принципами чистої архітектури:
* **Models (`src/models/`):** Визначають структуру сутностей (User, Book, BorrowRecord).
* **DTO (`src/dto/`):** Об'єкти передачі даних для безпечного отримання інформації від клієнта.
* **Repositories (`src/repositories/`):** Інкапсулюють логіку роботи з базою даних (MongoDB). Тільки вони знають про колекції та специфіку запитів.
* **Services (`src/services/`):** Містять "серце" системи — бізнес-логіку. Вони оркеструють репозиторії, але не залежать від конкретної реалізації БД.
* **Controllers (`src/controllers/`):** Приймають вхідні дані, формують DTO та викликають відповідні сервіси, повертаючи результат.

## 3. Рефакторинг та Лінтинг
Після реалізації основного функціоналу було проведено рев'ю коду. Жодних критичних "запахів коду" не виявлено. Це пов'язано з тим, що впродовж курсу навички програмування були вдосконалені достатньо, щоб не припускатися очевидних помилок на етапі проектування. Код відповідає принципам SOLID.

Для стандартизації стилю було використано лінтер **flake8**.
Команда перевірки: `flake8 src/ tests/ --max-line-length=120`
Результат: 0 помилок та попереджень. Код повністю відповідає стандартам PEP 8.

## 4. Юніт-тестування
Для перевірки бізнес-логіки використано фреймворк `pytest` та бібліотеку `unittest.mock` для ізоляції бази даних. Написано 13 тестів, які покривають 100% позитивних та негативних сценаріїв сервісного шару.

**Приклади тестових сценаріїв:**
* Успішна видача книги відповідному читачу.
* Відмова у видачі, якщо ліміт книг перевищено (викликається ValueError).
* Відмова у реєстрації користувача з існуючим email.

**Інструкція для запуску тестів:**
1. Активуйте віртуальне середовище (`venv\Scripts\activate` для Windows).
2. Встановіть залежності: `pip install -r requirements.txt`.
3. Виконайте команду: `python -m pytest tests/ -v`

**Журнал успішного виконання тестів:**
============================= test session starts =============================
collected 13 items
tests/test_book_service.py::test_add_new_book_success PASSED             [  7%]
tests/test_book_service.py::test_add_existing_book_updates_copies PASSED [ 15%]
tests/test_book_service.py::test_search_books_found PASSED               [ 23%]
tests/test_book_service.py::test_search_books_not_found PASSED           [ 30%]
tests/test_library_service.py::test_borrow_book_success PASSED           [ 38%]
tests/test_library_service.py::test_borrow_book_user_not_found_raises_error PASSED [ 46%]
tests/test_library_service.py::test_borrow_book_book_not_found_raises_error PASSED [ 53%]
tests/test_library_service.py::test_borrow_book_no_available_copies_raises_error PASSED [ 61%]
tests/test_library_service.py::test_borrow_book_limit_reached_raises_error PASSED [ 69%]
tests/test_library_service.py::test_return_book_success PASSED           [ 76%]
tests/test_library_service.py::test_return_book_record_not_found_raises_error PASSED [ 84%]
tests/test_user_service.py::test_register_user_success PASSED            [ 92%]
tests/test_user_service.py::test_register_user_duplicate_email_raises_error PASSED [100%]
============================== 13 passed in 0.12s =============================