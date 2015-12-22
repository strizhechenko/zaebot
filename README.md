# zaebot
Периодически читает ленту одного пользователя, дёргает оттуда существительные, относительно удачно склоняет подставляемое к ним слово "заебали" и постит это от второго пользователя.

Периодически удаляет те твиты, которые не набрали ни одного fav / rt.

## Конфиг
- common - настройки приложения
- reader - пользователь, ленту которого будем читать
- writer - бот, от имени которого будем постить

## Идеи
- Добавить поддержку нескольких источников.
- Добавить поддержку заголовков с http://eg.ru/daily/assorti/

## usage
После вбивания параметров в конфиг:

    cd папка_с_проектом && setsid python bot.py &>/dev/null & disown -a

## Воплощения:

- https://twitter.com/vsevsezaebali - читает ленту https://twitter.com/strizhechenko
- https://twitter.com/memes_zaebot - читает список [никроблоггеров](https://twitter.com/strizhechenko/lists/memes-zaebali/members) ([отдельная ветка](https://github.com/strizhechenko/zaebot/tree/memes))
- https://twitter.com/__coding_tips__ - ищет в твиттере сексуальные советы и переделывает их в советы по программированию ([отдельная ветка](https://github.com/strizhechenko/zaebot/tree/__coding_tips__))
