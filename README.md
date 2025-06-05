{
    "email": "nurlan.test_course@mail.ru",
    "password": 12345678
}

{
    "email": "nurlan.grachyov@mail.ru",
    "password": 12345678
}

## Сервис обработки загружаемых документов
### <br>__📌Требования__<br>
Перед началом работы убедитесь, что у вас установлены следующие инструменты и библиотеки:

Python >= 3.8
Poetry >= 1.1.0
PostgreSQL >= 12 (рекомендуемый движок базы данных)
Git >= 2.20
Docker (необязательно, если планируется использовать Docker)

### 🔧 Установка и настройка

<br>__💾 Шаг 1. Клонируем репозиторий__<br>
<br>Склонируйте исходный код проекта:<br>
````
git clone https://github.com/your_username/your_project.git
cd your_project
````

<br>__📜 Шаг 2. Устанавливаем зависимости__<br>
Использование Poetry делает управление зависимостями проще. Просто введите:

```
poetry install
```
Это создаст виртуальное окружение и установит все зависимости, указанные в вашем проекте.

<br>__📖 Шаг 3. Настроим базу данных__<br>
Если вы используете PostgreSQL, опишите настройки базы данных и примените миграции

<br>__🔁 Шаг 4. Сборка статических файлов (если требуется)__<br>
Если ваш проект включает фронтенд-ресурсы, соберите статику:

````
python manage.py collectstatic
````

__🏃Локальный запуск проекта__

Просто активируйте виртуальное окружение и запустите сервер:
````
poetry shell
python manage.py runserver
````
Теперь ваш проект доступен по адресу: http://localhost:8000.

<br>__🚧 Запуск через Docker (опционально)__<br>
Если вы предпочитаете Docker, подготовьте контейнер и запустите его:

````
docker-compose build
docker-compose up
````
<br>__🆕 Автоматизация CI/CD с GitHub Actions__<br>
Наш проект использует GitHub Actions для автоматического тестирования, сборки и деплоя. Основной пайплайн состоит из нескольких этапов:

Тестирование: выполнение тестов (unittest).
Сборка: создание Docker-образа.
Деплой: автоматическое обновление удалённого сервера через SSH.
Пример workflow (.github/workflows/ci.yml):

````
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  ci_cd_pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install Dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run Tests
        run: |
          poetry run pytest
      - name: Build Docker Image
        run: |
          docker build -t your_dockerhub_user/image_name:$GITHUB_SHA .
      - name: Push Docker Image
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push your_dockerhub_user/image_name:$GITHUB_SHA
      - name: Deploy via SSH
        uses: appleboy/ec-deploy-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            docker pull your_dockerhub_user/image_name:$GITHUB_SHA
            docker stop $(docker ps -q) || true
            docker rm $(docker ps -aq) || true
            docker run -d -p 8000:8000 your_dockerhub_user/image_name:$GITHUB_SHA
````
<br>__📌 Настройки сервера__<br>
Если у вас специфические настройки на удаленном сервере, обратите внимание на:

Открытые порты: убедитесь, что порт 8000 открыт для входящих соединений.
Безопасность: обязательно используйте SSL/TLS сертификаты (например, Let’s Encrypt).
Мониторинг: установите систему мониторинга (например, Prometheus и Grafana) для отслеживания состояния приложения.