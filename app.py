import sqlite3
from flask import Flask, jsonify, render_template, request, g
import os

app = Flask(__name__)
DATABASE = 'ecommerce.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT
            )
        ''')
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            products = [
                ('Premium Wireless Headphones', 'High-quality noise-canceling wireless headphones.', 299.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=60'),
                ('Smart Fitness Watch', 'Track your health and activities with style.', 149.50, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=60'),
                ('Mechanical Keyboard', 'RGB mechanical keyboard with tactile switches.', 120.00, 'https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=60'),
                ('4K Action Camera', 'Capture your adventures in stunning 4K resolution.', 199.00, 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=500&q=60'),
                ('Minimalist Desk Lamp', 'Adjustable LED desk lamp with wireless charging.', 45.00, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=60'),
                ('Portable SSD 1TB', 'Ultra-fast portable solid-state drive.', 110.00, 'https://images.unsplash.com/photo-1531492746076-161ca9bcad58?auto=format&fit=crop&w=500&q=60')
            ]
            cursor.executemany('INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)', products)
            db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    return jsonify(products)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    # Explicitly listen on 0.0.0.0 so Docker can map the port
    app.run(host='0.0.0.0', port=5000, debug=True)
