CREATE DATABASE IF NOT EXISTS esgraph DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE esgraph;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS ml_prediction, audit_log, flag, variance_note, review_log, evidence, emission_factor, financials, corporate_entry, site_entry, indicator, reporting_period, user_site, user, entity;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE entity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('group','subsidiary','bu','site') NOT NULL,
    parent_id INT,
    state VARCHAR(100),
    country VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_id) REFERENCES entity(id) ON DELETE RESTRICT
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('engineer','manager','admin') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_site (
    user_id INT,
    entity_id INT,
    PRIMARY KEY (user_id, entity_id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE CASCADE
);

CREATE TABLE reporting_period (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fy_label VARCHAR(50) UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    boundary ENUM('standalone','consolidated') NOT NULL,
    status ENUM('open','closed','locked') NOT NULL DEFAULT 'open',
    format_version VARCHAR(50) NOT NULL
);

CREATE TABLE indicator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL,
    format_version VARCHAR(50) NOT NULL,
    section VARCHAR(100),
    principle VARCHAR(100),
    tier VARCHAR(50),
    is_core BOOLEAN DEFAULT FALSE,
    level VARCHAR(50),
    data_type VARCHAR(50),
    unit VARCHAR(50),
    aggregation_rule VARCHAR(50),
    formula_key VARCHAR(100),
    evidence_required BOOLEAN DEFAULT FALSE,
    evidence_hint TEXT,
    sub_keys JSON,
    sort_order INT DEFAULT 0,
    UNIQUE KEY (code, format_version)
);

CREATE TABLE site_entry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    month_date DATE NOT NULL,
    indicator_id INT NOT NULL,
    sub_key VARCHAR(100) DEFAULT '',
    value_num DECIMAL(20,4),
    value_text TEXT,
    status ENUM('draft','submitted','returned','verified','locked') DEFAULT 'draft',
    entered_by INT,
    verified_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (entity_id, period_id, month_date, indicator_id, sub_key),
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT,
    FOREIGN KEY (indicator_id) REFERENCES indicator(id) ON DELETE RESTRICT,
    FOREIGN KEY (entered_by) REFERENCES user(id) ON DELETE SET NULL,
    FOREIGN KEY (verified_by) REFERENCES user(id) ON DELETE SET NULL
);

CREATE INDEX idx_site_entry_status ON site_entry(entity_id, period_id, status);
CREATE INDEX idx_site_entry_indicator ON site_entry(period_id, indicator_id);

CREATE TABLE corporate_entry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    indicator_id INT NOT NULL,
    sub_key VARCHAR(100) DEFAULT '',
    value_num DECIMAL(20,4),
    value_text TEXT,
    value_json JSON,
    status ENUM('draft','submitted','returned','verified','locked') DEFAULT 'draft',
    entered_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT,
    FOREIGN KEY (indicator_id) REFERENCES indicator(id) ON DELETE RESTRICT,
    FOREIGN KEY (entered_by) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE financials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    revenue_inr DECIMAL(20,4),
    ppp_rate DECIMAL(10,4),
    cost_of_purchases_inr DECIMAL(20,4),
    accounts_payable_inr DECIMAL(20,4),
    source_note TEXT,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT
);

CREATE TABLE emission_factor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_type VARCHAR(100) NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    factor DECIMAL(10,4) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    source_note TEXT,
    valid_from DATE,
    is_placeholder BOOLEAN DEFAULT FALSE
);

CREATE TABLE evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT NOT NULL,
    entry_table VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    sha256 VARCHAR(64) NOT NULL,
    size_bytes INT NOT NULL,
    uploaded_by INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE review_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT NOT NULL,
    actor_id INT NOT NULL,
    action ENUM('submit','verify','return','lock','reopen') NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (actor_id) REFERENCES user(id) ON DELETE RESTRICT
);

CREATE TABLE variance_note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    indicator_id INT NOT NULL,
    note TEXT NOT NULL,
    author_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT,
    FOREIGN KEY (indicator_id) REFERENCES indicator(id) ON DELETE RESTRICT,
    FOREIGN KEY (author_id) REFERENCES user(id) ON DELETE RESTRICT
);

CREATE TABLE flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    indicator_id INT NOT NULL,
    rule_key VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    source ENUM('rule','ml') NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT,
    FOREIGN KEY (indicator_id) REFERENCES indicator(id) ON DELETE RESTRICT
);
CREATE INDEX idx_flag_lookup ON flag(entity_id, period_id, is_resolved);

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actor_id INT,
    action VARCHAR(50) NOT NULL,
    object_type VARCHAR(50) NOT NULL,
    object_id INT NOT NULL,
    old_value JSON,
    new_value JSON,
    ip VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (actor_id) REFERENCES user(id) ON DELETE SET NULL
);
CREATE INDEX idx_audit_lookup ON audit_log(object_type, object_id);

CREATE TABLE ml_prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    period_id INT NOT NULL,
    indicator_id INT NOT NULL,
    kind ENUM('anomaly','forecast','extraction') NOT NULL,
    payload JSON,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE RESTRICT,
    FOREIGN KEY (period_id) REFERENCES reporting_period(id) ON DELETE RESTRICT,
    FOREIGN KEY (indicator_id) REFERENCES indicator(id) ON DELETE RESTRICT
);
