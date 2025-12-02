CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    gender VARCHAR(20),
    date_of_birth DATE,
    phone VARCHAR(50) UNIQUE,
    email VARCHAR(255),
    photo_path VARCHAR(512),
    balance NUMERIC(12,2) DEFAULT 0,
    barcode VARCHAR(128) UNIQUE,
    vip BOOLEAN DEFAULT FALSE,
    notes TEXT,
    health_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscription_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    duration_days INTEGER,
    visit_count INTEGER,
    description TEXT,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    subscription_type_id INTEGER REFERENCES subscription_types(id),
    start_date DATE NOT NULL,
    end_date DATE,
    remaining_visits INTEGER,
    status VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50),
    amount_paid NUMERIC(12,2),
    admin_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS visits (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    admin_id INTEGER REFERENCES users(id),
    direction VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_clients_full_name ON clients(full_name);
CREATE INDEX IF NOT EXISTS idx_clients_barcode ON clients(barcode);
CREATE INDEX IF NOT EXISTS idx_visits_timestamp ON visits(timestamp);
