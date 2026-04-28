from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# --- ฟังก์ชันจัดการฐานข้อมูล ---
def init_db():
    conn = sqlite3.connect('/home/Akorn/Cs104-Week13/food_made_to_order_shop.db')
    c = conn.cursor()
    # สร้างตารางหมวดหมู่
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL)''')
    # สร้างตารางสินค้า (เมนูอาหาร)
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    product_description TEXT,
                    product_price REAL NOT NULL,
                    product_stock INTEGER NOT NULL,
                    product_image_url TEXT,
                    category_id INTEGER)''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('/home/Akorn/Cs104-Week13/food_made_to_order_shop.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Routes ---

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['product_name']
        desc = request.form['product_description']
        price = request.form['product_price']
        stock = request.form['product_stock']
        url = request.form['product_image_url']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO products (product_name, product_description, product_price, product_stock, product_image_url) VALUES (?, ?, ?, ?, ?)',
                     (name, desc, price, stock, url))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE product_id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['product_name']
        desc = request.form['product_description']
        price = request.form['product_price']
        stock = request.form['product_stock']
        url = request.form['product_image_url']

        conn.execute('UPDATE products SET product_name=?, product_description=?, product_price=?, product_stock=?, product_image_url=? WHERE product_id=?',
                     (name, desc, price, stock, url, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE product_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("---------------------------------------")
    print("Food Made to Order Shop is running at: http://127.0.0.1:5000")
    print("---------------------------------------")
    app.run(debug=True)
