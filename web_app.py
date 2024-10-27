import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base.config import Client, Base  # Модель Client с полем user_text

app = Flask(__name__)

# Настройка базы данных
engine = create_engine("sqlite:///keywords.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_intent(contract, service, intent, phone, address, user_text):
    """Добавляет новую запись в базу данных и отправляет уведомление на почту."""
    session = Session()
    new_intent = Client(
        contract=contract,
        service=service,
        intent=intent,
        phone=phone,
        address=address,
        user_text=user_text
    )
    session.add(new_intent)
    session.commit()
    session.close()

    # Отправка уведомления по почте
    send_email_to_admin(contract, service, intent, phone, address, user_text)


def send_email_to_admin(contract, service, intent, phone, address, user_text):
    """Отправляет письмо админу с информацией о новой записи."""
    admin_email = "prap0235@gmail.com"  # Адрес администратора
    from_email = "fvbitteam@gmail.com"  # Ваша почта
    password = "fkln sabt enmm gpdi"  # Пароль от почты

    # Формируем содержимое письма
    message = MIMEText(
        f"Номер договора: {contract}\nКлючевое слово: {service}\nНамерение: {intent}\n"
        f"Телефон: {phone}\nEmail: {address}\nОписание: {user_text}"
    )
    message['Subject'] = "Новая запись в системе"
    message['From'] = from_email
    message['To'] = admin_email

    # Отправка письма
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, admin_email, message.as_string())


@app.route('/table', methods=['GET', 'POST'])
def show_table():
    if request.method == 'POST':
        # Получаем данные из формы
        contract = request.form['contract']
        service = request.form['keyword']
        intent = request.form['intent']
        phone = request.form['phone']
        address = request.form['email_address']
        user_text = request.form['user_text']

        # Добавляем запись в базу данных и отправляем письмо админу
        add_intent(contract, service, intent, phone, address, user_text)

        return redirect(url_for('show_table'))

    # Получаем все записи для отображения в таблице
    session = Session()
    clients = session.query(Client).all()
    session.close()

    return render_template('table.html', clients=clients)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_intent(id):
    session = Session()
    intent_to_delete = session.query(Client).filter_by(id=id).first()
    if intent_to_delete:
        session.delete(intent_to_delete)
        session.commit()
    session.close()
    return redirect(url_for('show_table'))


if __name__ == "__main__":
    app.run(debug=True)