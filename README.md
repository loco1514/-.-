# S21 Meeting Room Bot


## Описание

В _Школе 21_ есть пять переговорных комнат предназначеных для обучения, совещаний и других рабочих целей.

Однако, некоторые пиры и сотрудники **злоупотребляют этим ресурсом** и занимают переговорные комнаты на весь день для своих личных дел, не давая возможности другим людям ими пользоваться.

Для решения вышеописанной проблемы мы, **команда『 』"_Пустые_"**, создали сервис для удобного отслеживания и бронирования переговорных комнат.  


## Стек

**C#, SQLite:** Разработка и поддержка API, используемого для взаимодействия с базой данных SQLite и чат-ботом

**Python, aiogram v3.3.0:** Настройка и создание телеграм-бота

**HTML, CSS, JavaScript:** Пользовательский интерфейс для бота


## Настройка и запуск бота

Чтобы запустить бота, необходимо выполнить следующие действия:

1. Создать и активировать окружение
    
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Создать бота
   
    Открыть [BotFather](https://t.me/BotFather>) и следовать инструкциям по созданию нового бота.

    Создать *.env* файл с токеном (после '='):

    ```
    TOKEN=
    ```

3. Запустить бота

    ```
    python3 tg_bot.py
    ```

    Теперь можно использовать бота. Для этого отправьте боту команду */start* в приложении Telegram.


## Использование бота

Первым делом пиру нужно зарегистрироваться в телеграм-боте:

![Регистрация](img/registration.png)

1. Перейти в чат с ботом и начать переписку
2. Нажать кнопку "Зарегистироваться", пройти регистрацию


После успешной регистрации пользователь может посмотреть список его бронирований и забронировать комнату:

![Бронь телеграм](img/reserve.png)

1. Нажать кнопку "Забронировать". 
После, откроется сайт
2. На сайте нужно выбрать желаемую дату и кликнуть по ней.
3. Затем пользователь выбирает время и комнату для бронирования
4. Нажать кнопку "Забронировать"


## Идеи и предложения

**Ограничения на бронь:** 
Введение ограничений на количество и продолжительность бронирования (сейчас пир может забронировать комнату 24 раза на час (то есть на весь день))

**Аналитика по использованию:**
Возможность отслеживать и анализировать статистику по использованию переговорных комнат. Включает в себя также статистику по нарушениям и злоупотреблениям.

**Уникальные QR-коды:** 
Генерация уникальных QR-кодов для учета времени прихода и ухода. Планируется установка мини-экранов около переговорных комнат, где будет отображаться QR-код. Пользователи будут сканировать QR-код при входе и выходе для регистрации времени.
