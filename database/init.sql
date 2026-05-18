-- ============================================================
-- NexShop E-Commerce Database Init Script
-- Runs automatically on first PostgreSQL container start
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255) NOT NULL,
    description TEXT,
    price   DECIMAL(10, 2) NOT NULL,
    image_url TEXT
);

INSERT INTO products (name, description, price, image_url) VALUES
  ('Premium Wireless Headphones', 'High-quality noise-canceling wireless headphones.', 299.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=60'),
  ('Smart Fitness Watch', 'Track your health and activities with style.', 149.50, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=60'),
  ('Mechanical Keyboard', 'RGB mechanical keyboard with tactile switches.', 120.00, 'https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=60'),
  ('4K Action Camera', 'Capture your adventures in stunning 4K resolution.', 199.00, 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=500&q=60'),
  ('Minimalist Desk Lamp', 'Adjustable LED desk lamp with wireless charging.', 45.00, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=60'),
  ('Portable SSD 1TB', 'Ultra-fast portable solid-state drive.', 110.00, 'https://images.unsplash.com/photo-1531492746076-161ca9bcad58?auto=format&fit=crop&w=500&q=60')
ON CONFLICT DO NOTHING;
