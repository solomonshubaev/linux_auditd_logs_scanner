CREATE DATABASE IF NOT EXISTS cyngular;

CREATE TABLE IF NOT EXISTS cyngular.raw_data (
    id VARCHAR(36) PRIMARY KEY,
    data JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cyngular.audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(255),
    msg VARCHAR(255),
    pid INT,
    ses INT UNSIGNED,
    uid INT,
    res VARCHAR(255),
    target VARCHAR(255),
    subj VARCHAR(255),
    fd INT,
    syscall VARCHAR(255),
    auid INT UNSIGNED,
    comm VARCHAR(255),
    exe VARCHAR(255),
    path VARCHAR(255),
    name VARCHAR(255),
    msg_audit_datetime DATETIME,
    msg_audit_unique_id INT,
    `key` VARCHAR(255),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
	INDEX idx_type (type),
    INDEX idx_msg_audit_datetime (msg_audit_datetime),
    INDEX idx_msg_audit_unique_id (msg_audit_unique_id),
    INDEX idx_key (`key`),
    INDEX idx_auid (auid),
    INDEX idx_comm (comm),
    INDEX idx_exe (exe),
    INDEX idx_path (path),
    INDEX idx_name (name)
);
