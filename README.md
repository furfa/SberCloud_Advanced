# ege_project

read_data.py генерация данных во фронт

парсеры по названию уника лежат

Крч parse.sh запуск всех парсеров + генерация данных во фронт

app.py запуск фронта

В tools.functions.py вынесены функции общие для всех скриптов

собрать докер

docker build -t egengine1 .

запустить докер
docker run -p 8001:8001 egengine1 
