import psycopg2
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname="supply_management",
        user="postgres",
        password="0aH6PI7ymax",
        host="localhost"
    )
    return conn

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Добавление поставщика
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO suppliers (company_name, contact_info, terms_of_cooperation,'
        'rating) VALUES (%s, %s, %s, %s)',
        (data['company_name'], data['contact_info'], data['terms_of_cooperation'], data['rating'])
    )
    conn.commit()
    cursor.close()
    return jsonify({'status': 'Supplier added succesfully!'})

# Просмотр всех поставщиков
@app.route('/suppliers', methods=['GET'])
def view_suppliers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suppliers')
    suppliers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(suppliers)

# Удаление поставщика
@app.route('/delete_supplier/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM suppliers WHERE supplier_id=%s', (supplier_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'Supplier deleted succesfully!'})

if __name__ == '__main__':
    app.run(debug=True)