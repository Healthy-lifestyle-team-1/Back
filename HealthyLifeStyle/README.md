# Getting Started
***
### Клонируйте репозиторий с GitHub и переключитесь на директорию проекта
```commandline
git clone https://github.com/Healthy-lifestyle-team-1/Back
cd HealthyLifeStyle
```

### Создайте файл .env в корневой папке и укажите переменные для смс отправлений:
```
```

### Активируйте виртуальное окружение проекта:
```commandline
pip install -r ../requirements.txt
```

### Сделайте миграции:
```commandline
python manage.py migrate
```

### Запустите сервер:

```commandline
python manage.py runserver
```