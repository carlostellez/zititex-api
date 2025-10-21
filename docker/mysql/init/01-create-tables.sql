-- Initial database schema for Zititex API
-- This script is automatically executed when MySQL container starts

-- Use the database
USE zititex_db;

-- Create client table
CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique client identifier',
    full_name VARCHAR(100) NOT NULL COMMENT 'Client full name',
    email VARCHAR(255) NOT NULL COMMENT 'Client email address',
    phone VARCHAR(20) NOT NULL COMMENT 'Client phone number',
    company VARCHAR(255) NULL COMMENT 'Company name (optional)',
    product_type VARCHAR(100) NULL COMMENT 'Type of product interested in (optional)',
    quantity INT NULL COMMENT 'Quantity requested (optional)',
    message TEXT NOT NULL COMMENT 'Client message or inquiry',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp',
    INDEX idx_email (email),
    INDEX idx_full_name (full_name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Contact form submissions';

-- Create indexes for better query performance
CREATE INDEX idx_company ON client(company);
CREATE INDEX idx_product_type ON client(product_type);
CREATE INDEX idx_created_email ON client(created_at, email);

-- Display table structure
DESCRIBE client;

-- Show confirmation message
SELECT 'Database schema created successfully!' as Status;

