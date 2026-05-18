import os
import time
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url
        }


def seed_products():
    if Product.query.count() == 0:
        items = [
            Product(name='Premium Wireless Headphones', description='High-quality noise-canceling wireless headphones.',
                    price=299.99, image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=60'),
            Product(name='Smart Fitness Watch', description='Track your health and activities with style.',
                    price=149.50, image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=60'),
            Product(name='Mechanical Keyboard', description='RGB mechanical keyboard with tactile switches.',
                    price=120.00, image_url='https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=60'),
            Product(name='4K Action Camera', description='Capture your adventures in stunning 4K resolution.',
                    price=199.00, image_url='https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=500&q=60'),
            Product(name='Minimalist Desk Lamp', description='Adjustable LED desk lamp with wireless charging.',
                    price=45.00, image_url='https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=60'),
            Product(name='Portable SSD 1TB', description='Ultra-fast portable solid-state drive.',
                    price=110.00, image_url='https://images.unsplash.com/photo-1531492746076-161ca9bcad58?auto=format&fit=crop&w=500&q=60'),
        ]
        db.session.add_all(items)
        db.session.commit()
        print("✅ Database seeded with products.")


def init_db_with_retry(retries=10, delay=3):
    for attempt in range(retries):
        try:
            with app.app_context():
                db.create_all()
                seed_products()
            print("✅ Database initialized successfully.")
            return
        except Exception as e:
            print(f"⏳ DB not ready (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after multiple retries.")


@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'ecommerce-backend'})


@app.route('/api/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


if __name__ == '__main__':
    init_db_with_retry()
    app.run(host='0.0.0.0', port=5000, debug=False)
