-- Projeto incompleto, implementar e ajustar...

-- For MySQL

CREATE TABLE web_message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    created_date TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- For PostgreSQL

CREATE TABLE web_message (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
