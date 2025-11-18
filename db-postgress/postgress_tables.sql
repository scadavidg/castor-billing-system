-- postgres_clients.sql
-- Crear tabla de clientes y datos de prueba

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(50),
    direccion VARCHAR(200)
);

-- Datos de prueba (ON CONFLICT evita duplicados si se ejecuta varias veces)
INSERT INTO clients (nombre, email, telefono, direccion)
VALUES 
('Juan Pérez', 'juan@example.com', '555-1234', 'Calle 1 #123'),
('Ana Gómez', 'ana@example.com', '555-5678', 'Calle 45 #12-34')
ON CONFLICT (email) DO NOTHING;