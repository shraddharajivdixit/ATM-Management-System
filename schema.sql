CREATE DATABASE IF NOT EXISTS atm_gui;
USE atm_gui;

CREATE TABLE users (
    account_no VARCHAR(20) PRIMARY KEY,
    pin VARCHAR(10) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_no VARCHAR(20),
    type VARCHAR(20),
    amount DECIMAL(12,2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (account_no, pin, balance) VALUES
('101', '1234', 5000),
('102', '2345', 5000),
('103', '3456', 5000);

