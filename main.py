from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route("/")  # создание декоратора для корневой страницы
def status():
    with open("settings.json", 'r') as file:  # чтение из файла настроек и запись их в словарь
        settings = json.load(file)
    if settings["online"]:  # условие для вывода результата
        return "<h1>Приложение работает</h1>"
    else:
        return "<h1>Приложение не работает</h1>"


@app.route('/candidate/<int:id>')  # создание декоратора для персональной страницы кандидата
def decribe_candidate(id):
    with open("candidates.json", 'r', encoding="utf-8") as file:  # чтение из файла данных кандидата
        dict_of_candidate = json.load(file)  # и запись их в список python
    return render_template("candidate.html", candidate=dict_of_candidate[id - 1])  # запуск рендеринга для
    # генерации персональной страницы кандидата


@app.route('/list/')  # создание декоратора для списка кандидатов
def list_of_candidate():
    with open("candidates.json", 'r', encoding="utf-8") as file:  # чтение из файла данных кандидата
        dict_of_candidate = json.load(file)  # и запись их в список python
    return render_template("all_candidates.html", candidates=dict_of_candidate)  # запуск рендеринга для
    # генерации страницы со списком кандидатов


@app.route('/search/')  # создание декоратора для поиска по буквам в имени
def search():
    combination = request.args.get("name")  # получаем значение по ключу "name"
    coincidence = []  # создание пустого списка совпадений для дальнейшего добавления в него значений
    with open("candidates.json", 'r', encoding="utf-8") as file:
        dict_of_candidate = json.load(file)  # создание списка python с данными кандидатов
    with open("settings.json", 'r') as file:
        settings = json.load(file)  # создание словаря python с настройками
    if settings["case-sensitive"]:  # проверка на зависимость регистра
        for candidate in dict_of_candidate:
            if combination in candidate["name"]:
                coincidence.append(candidate)  # добавление регистрозависимых совпадений в список
    else:
        for candidate in dict_of_candidate:
            if combination.lower() in candidate["name"].lower():
                coincidence.append(candidate)  # добавление регистронезависимых совпадений в список
    return render_template("search.html", coincidence=coincidence, num=len(coincidence))  # запуск рендеринга для
    # генерации страницы с результатами поиска


@app.route('/skill/')  # создание декоратора для поиска по буквам в навыках
def skill():
    combination = request.args.get("skill")  # получаем значение по ключу "name"
    coincidence = []  # создание пустого списка совпадений для дальнейшего добавления в него значений
    with open("candidates.json", 'r', encoding="utf-8") as file:
        dict_of_candidate = json.load(file)  # создание списка python с данными кандидатов
    with open("settings.json", 'r') as file:
        settings = json.load(file)  # создание словаря python с настройками
    for candidate in dict_of_candidate:  # проверка совпадений (регистр не учитывается)
        if combination.lower() in candidate["skills"].lower():
            coincidence.append(candidate)  # добавление в финальный список совпадений
    if len(coincidence) > settings["limit"]:  # сверка финального списка
        coincidence_with_limit = []  # создание нового списка, для добавление в него строго ограниченного настройками
        # количества кандидатов
        for i in range(settings["limit"]):  # запуск цикла с количеством итераций раным значению "limit" в настройках
            coincidence_with_limit.append(coincidence[i])
        return render_template("skills.html", coincidence=coincidence_with_limit, num=len(coincidence_with_limit),
                               skill=combination)
    else:
        return render_template("skills.html", coincidence=coincidence, num=len(coincidence), skill=combination)  # в
    # случае, когда количество кандидатов не превышает установленный лимит, тогда для рендеринга используется список
    # "coincidence", а не "coincidence_with_limit"


app.run(debug=True)
