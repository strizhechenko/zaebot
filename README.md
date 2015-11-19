# zaebot
Периодически читает ленту одного пользователя, дёргает оттуда существительные, относительно удачно склоняет подставляемое к ним слово "заебали" и постит это от второго пользователя.

Периодически удаляет те твиты, которые не набрали ни одного fav / rt.

## Конфиг
- common - настройки приложения
- reader - пользователь, ленту которого будем читать
- writer - бот, от имени которого будем постить

## Идеи
- Стоит перенести в конфиг некоторые параметры, например подставляемые слова, количество слов за пост и частоту постинга, но мне лениво.
- Чёрный список для слов. (лол, итд)

## usage
После вбивания параметров в конфиг:

    cd папка_с_проектом && setsid python bot.py &>/dev/null & disown -a

Поддерживает запуск в heroku и его конфиги в env:

    heroku create
    git push heroku master
    heroku config:set consumer_key=
    heroku config:set consumer_secret=
    heroku config:set writer_access_key=
    heroku config:set writer_access_secret=
    heroku config:set reader_access_key=
    heroku config:set reader_access_secret=
    heroku ps:scale worker=1

    
TODO: надо бы по уму сделать reader опциональным и при отсутствии дублировать из writer

## Воплощения:

- https://twitter.com/vsevsezaebali - читает ленту https://twitter.com/strizhechenko
- https://twitter.com/memes_zaebot - читает список https://twitter.com/strizhechenko/lists/memes-zaebali/members
