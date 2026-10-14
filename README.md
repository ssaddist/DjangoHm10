# Django Home Work 10: Battle Simulator API

REST API на базі Django REST Framework для створення персонажів, проведення покрокових боїв та перегляду історії битв.

## Встановлення та запуск

1. Створення та активація віртуального оточення:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Встановлення залежностей:

```bash
pip install -r requirements.txt
```

3. Застосування міграцій:

```bash
python manage.py migrate
```

4. Запуск сервера розробки:

```bash
python manage.py runserver
```

5. Запуск тестів:

```bash
python manage.py test
```

## API Ендпоінти

### Персонажі

- `GET /api/characters/` — список персонажів
- `GET /api/characters/{id}/` — інформація про персонажа
- `POST /api/characters/` — створення персонажа
- `PUT /api/characters/{id}/` — повне оновлення персонажа
- `PATCH /api/characters/{id}/` — часткове оновлення персонажа
- `DELETE /api/characters/{id}/` — видалення персонажа

### Бої

- `POST /api/battle/` — симуляція бою між двома персонажами
- `GET /api/battles/` — історія проведених боїв

## Тестування через Bruno

Для зручного тестування API підготовлено колекцію запитів у директорії `bruno/`.

Bruno — це швидкий open-source API клієнт, альтернатива Postman.

- Офіційний сайт: [usebruno.com](https://www.usebruno.com)
- Завантажити Bruno: [usebruno.com/downloads](https://www.usebruno.com/downloads)

### Як відкрити колекцію

1. Встановити та відкрити Bruno.
2. Натиснути `Open Collection`.
3. Обрати папку `bruno` в корені цього репозиторію.
4. Використовувати готові запити з папок `Characters` та `Battle`.
