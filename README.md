# Бот "Спросить не напрасно".
### Основа для телеграм бота, которую можно запускать, как в режиме polling'а, так и в режиме webhook'а

## Подготовка к запуску:
### Создать файл ".env" с парой ключ=значение, пример есть в файле .env.example
## Запуск приложения
### В режиме polling'а:
> python3 src/run_bot.py

### В режиме webhook'а (также в этом режиме будет запущена точка доступа для webhook'а trello):
> python3 src/run_webhook_api.py
#### Запросы от trello ожидаются на /trelloCallback, приходят в формате .json, [пример](src/example/trello_request.json). Принимает POST-запросы (с телом данных) и HEAD-запросы (для проверки доступности ресурса).
#### Пример curl-запроса для отправки данных на trello endpoint:
```
curl -X POST -d '@src/example/trello_request.json' -H "Content-Type: application/json" localhost:8000/trelloWebhookApi # (localhost). - адрес сайта. (:8000). - порт, на который будет стучаться запрос или не указывать, если 80.
```
## Проверка API сервера с использованием ngrok на локальном компьютере:
- Установить ngrok с [сайта](https://ngrok.com/download)
- [Зарегистрироваться](https://dashboard.ngrok.com/) и получить [токен](https://dashboard.ngrok.com/get-started/your-authtoken)
- в консоль вставить:
> ngrok config add-authtoken TOKEN  # (TOKEN). - токен с сайта ngrok
- запустить ngrok
> ngrok http 8000 --host-header=site.local
- скопировать адрес сайта из консоли, наподобие: https://8250-31-148-16-235.eu.ngrok.io в файл .env: WEBHOOK_URL=https://8250-31-148-16-235.eu.ngrok.io
- запустить приложение (см. выше).
### Больше информации по ngrok на [сайте](https://ngrok.com/docs/getting-started)


## Настройка poetry:

Poetry - это инструмент для управления зависимостями и виртуальными окружениями,
также может использоваться для сборки пакетов.

### Установка:

Для UNIX систем вводим в консоль следующую команду

> *curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -*

Для WINDOWS вводим в PowerShell

> *(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -*

После установки перезапустите оболочку и введите команду

> poetry --version

Ответ должен быть в формате

> Poetry version 1.1.13

Для дальнейшей работы введите команду:

> poetry config virtualenvs.in-project true

Выполнение данной команды необходимо для создания виртуального окружения в папке проекта,
по умолчанию папка .venv создается по пути **C:\Users\<username>\AppData\Local\pypoetry\Cache\virtualenvs**

После предыдущей команды создадим виртуальное окружение нашего проекта с помощью команды

> poetry install

Результатом выполнения команды станет создание в корне проекта папки .venv.
Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее) и pyproject.toml

Для добавления новой зависимости в окружение необходимо выполнить команду

> poetry add <package_name>
>
> poetry add starlette *пример использования*

Также poetry позволяет разделять зависимости необходимые для разработки, от основных.
Для добавления зависимости необходимой для разработки и тестирования необходимо добавить флаг ***--dev***

> poetry add <package_name> --dev
>
> poetry add pytest --dev *пример использования*

### Порядок работы после настройки

Существует возможность запуска скриптов и команд с помощью команды без активации окружения:

> poetry run <script_name>.py
>
> poetry run pytest
>
> poetry run black

Можно вызвать консоль poetry с помощью команды:

> poetry shell

В вызванной оболочке будет автоматически активировано окружение.
Порядок работы в оболочке не меняется. Пример команды для Win:

> C:\Dev\nenaprasno_bot\ask_nenaprasno_bot>python src\run_bot.py

Доступен стандартный метод работы с активацией окружения в терминале с помощью команд:

Для WINDOWS:

> source .venv/Scripts/activate

Для UNIX:

> source .venv/bin/activate


## Настройка pre-commit:

> poetry install
>
> pre-commit install

Далее при каждом коммите у вас будет происходить автоматическая проверка линтером, а так же будет происходить автоматическое приведение к единому стилю.

Если у вас произошло появление сообщений об ошибках, то в большинстве случаев достаточно повторить добавление файлов вызвавших ошибки в git и повторный коммит:

> git add .
>
> git commit -m "Текст комментария коммита"
