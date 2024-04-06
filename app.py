import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load existing passwords from a file
with open('passwords.txt', 'r') as file:
    passwords = {line.strip() for line in file}

def save_order_to_csv(data):
    fieldnames = ['Фамилия', 'Инициалы', 'Адрес получателя', 'Количество', 'Тип яиц', 'Характеристики', 'Способ доставки', 'Накладная', 'Дополнительная информация']
    with open('orders.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty and write header if necessary
        if csvfile.tell() == 0:
            writer.writeheader()

        # Remove the 'submit_button' field if present
        data.pop('submit_button', None)

        # Rename fields to Russian
        russian_data = {
            'Фамилия': data.get('surname', ''),
            'Инициалы': data.get('initials', ''),
            'Адрес получателя': data.get('recipient_address', ''),
            'Количество': data.get('quantity', ''),
            'Тип яиц': data.get('type', ''),
            'Характеристики': data.get('characteristics', ''),  # Adjusted field name
            'Способ доставки': ', '.join(request.form.getlist('delivery')),  # Retrieving list of selected delivery options
            'Накладная': data.get('invoice', ''),
            'Дополнительная информация': data.get('additional_info', '')
        }

        # Write the order data to the CSV file
        writer.writerow(russian_data)

@app.route('/')
def index():
    return render_template('order_form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.form.to_dict()

    # Check if the password is correct
    if 'password' in data and data['password'] in passwords:
        # Remove the password from the data before saving
        password = data.pop('password')

        # Save the data to a CSV file
        save_order_to_csv(data)

        return jsonify({'message': 'Заказ успешно размещен!'})
    else:
        return jsonify({'message': 'Неверный пароль!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
