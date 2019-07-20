# Wchodzę na stronę GET / -> zostaje mi zwrócona lista moich wydatków, na górze przycisk z napisem
# "Dodaj kolejny". Po kliknięciu na ten guzik zostajemy przeniesieni na strone /add.
# Metoda GET na tej stronie zwróci nam formularz z dwoma inputami: kwota, opis.
# Po kliknięciu submit tego formularza zostaje wysłany POST na /add i wydatek zostaje zapisany w:
# a) pliku json (rzućcie okiem na poprzednie zadanie dodatkowe i sprawdźcie w necie jak zapisać json-a do pliku)
# b) w bazie danych (dopiero podczas 3 dnia na zajęciach będzie wyjaśnione jak to robić,
# dlatego jest to opcjonalne)
# Na stronie głównej obok przycisku "Dodaj kolejny" będzie przycisk
# "Wygeneruj raport" który będzie nam zwracał plik .pdf w którym będzie jakiś nagłówek w stylu
# "Raport z dnia {aktualna_data}", poniżej będzie tabelka zawierająca 3 kolumny: liczba porzadkowa, opis, kwota.
#
from flask import Flask, request, render_template, redirect, send_file, make_response
from psycopg2 import connect, OperationalError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import date

username = "postgres"
passwd = "coderslab"
hostname = "127.0.0.1"  # lub "localhost"
db_name = "costs_db"


def create_connection(username, passwd, hostname, db_name):
    try:
        # tworzymy nowe połączenie
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Połączenie udane.")
        return cnx
    except OperationalError:
        print("Nieudane połączenie.")
        return None


context = create_connection(username, passwd, hostname, db_name)
app = Flask(__name__)


@app.route("/", methods=["GET"])
def show_form():
    context = create_connection(username, passwd, hostname, db_name)
    parsedCostsList = ""

    if context:
        cursor = context.cursor()
        cursor.execute("SELECT id,purpose,description,amount FROM costs")
        for (cost_id, purpose, description, amount) in cursor:
            parsedCostsList += '<li>{}. {}, {}, {}</li>'.format(cost_id, purpose, description, amount)
        context.close()
    else:
        parsedCostsList = """
                  <li></li>
            """
    # return render_template('main_list.html', parsedCostsList=parsedCostsList)
    return """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>Main</title>
            </head>
            <body>
            <a href="/add">Dodaj kolejny</a>
            <a href="/get-pdf">Wygeneruj raport</a>
            
            <ul>
                {}
            </ul>
            </body>
            </html>
 
    """.format(parsedCostsList)

@app.route('/get-pdf')
def pdf():
    context = create_connection(username, passwd, hostname, db_name)
    parsedCostsList = []

    if context:
        cursor = context.cursor()
        cursor.execute("SELECT id,purpose,description,amount FROM costs")
        for (cost_id, purpose, description, amount) in cursor:
            parsedCostsList.append("{}. {}, {}, {}".format(cost_id, purpose, description, amount))
        context.close()
    c = canvas.Canvas("report.pdf", pagesize=letter)
    c.setFont('Helvetica', 12)
    c.setLineWidth(.3)
    c.drawString(30, 750, 'Raport z dnia: {}'.format(date.today()))
    y = 730
    for i in range(len(parsedCostsList)):
        c.drawString(30, y, parsedCostsList[i])
        y -= 15
    c.showPage()
    c.save()

    return send_file('report.pdf', as_attachment=True)


@app.route("/add", methods=["GET"])
def fill_form():
    return render_template("form.html")


@app.route("/add", methods=["POST"])
def add_to_db():
    purpose = request.form["purpose"]
    description = request.form["desc"]
    amount = request.form["amount"]

    context = create_connection(username, passwd, hostname, db_name)
    # parsedTable = ""

    if context:
        cursor = context.cursor()
        cursor.execute(
            "INSERT INTO costs(purpose,description,amount) VALUES (%s, %s, %s);",
            (purpose, description, amount)
        )
        context.commit()

        context.close()
    return redirect('/')


app.run()
