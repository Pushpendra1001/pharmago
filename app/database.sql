DROP TABLE IF EXISTS orders_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255),
    stock INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    address TEXT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    delivery_fee DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL DEFAULT 'Cash on Delivery',
    delivery_method VARCHAR(50) NOT NULL DEFAULT 'Standard Delivery',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE orders_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);


INSERT INTO products (name, description, price, image) VALUES
('Emergency First Aid Kit', 'Complete emergency medical kit for home or travel. Includes all essential first aid supplies for handling common injuries and emergencies.', 49.99, 'firstaid.jpg'),
('Digital Thermometer', 'Instant read digital thermometer with fever alert. Provides accurate temperature readings in seconds with easy-to-read display.', 24.99, 'dtherometer.jpg'),
('Blood Pressure Monitor', 'Automatic digital blood pressure monitor with memory. Tracks your readings over time and provides comprehensive health data.', 59.99, 'bloodpressuremonitor.jpg'),
('Pulse Oximeter', 'Fingertip pulse oximeter for oxygen level monitoring. Compact, portable device for checking your oxygen saturation and pulse rate.', 34.99, 'puleseoximeter.jpg'),
('Prescription Delivery', 'Fast delivery of your prescription medications. Upload your prescription and get your medications delivered to your doorstep.', 0.00, 'Prescription.jpg'),
('Glucose Monitoring Kit', 'Complete blood glucose monitoring system with strips. Essential tool for diabetes management with accurate results in seconds.', 79.99, 'Glucose Monitoring Kit.jpg'),
('CPAP Machine', 'Continuous positive airway pressure therapy device. High-quality sleep apnea treatment device with adjustable pressure settings.', 599.99, 'CPAP Machine.jpg'),
('Advanced Wound Care Kit', 'Professional wound care supplies for home use. Contains specialized dressings, antiseptics, and bandages for treating complex wounds.', 39.99, 'Advanced Wound Care Kit.jpg'),
('Stethoscope', 'High-quality dual-head stethoscope for accurate auscultation. Ideal for professionals and students.', 29.99, 'stethoscope.jpg'),
('Disposable Surgical Gloves (Pack of 100)', 'Latex-free, powder-free surgical gloves for infection control. Each box contains 100 sterile gloves.', 19.99, 'surgical_gloves.jpg'),
('Infrared Forehead Thermometer', 'Non-contact infrared thermometer with fever alarm. Provides fast, accurate temperature readings on the forehead.', 39.99, 'infrared_thermometer.jpg'),
('Portable Nebulizer Machine', 'Compact ultrasonic nebulizer for respiratory therapy. Converts liquid medication into fine mist for inhalation.', 49.99, 'nebulizer.jpg'),
('Medical Wheelchair', 'Lightweight, foldable wheelchair with adjustable footrests. Easy to transport and ideal for home or hospital use.', 199.99, 'wheelchair.jpg'),
('Handheld ECG Monitor', 'Portable 1-lead ECG monitor with LCD display. Records and displays real-time heart-rate data anywhere.', 89.99, 'ecg_monitor.jpg'),
('Adult Blood Glucose Test Strips (50-count)', 'Compatible with most glucometers. Provides accurate blood sugar readings for diabetes management.', 24.99, 'glucose_strips.jpg'),
('Medical Face Shield (Pack of 5)', 'Full-coverage, anti-fog face shields for protection against droplets. Adjustable headband for a secure fit.', 14.99, 'face_shield.jpg');
