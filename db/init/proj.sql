-- Pełna, profesjonalna baza z opiniami i dodatkowymi polami

CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255),
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  gender ENUM('M', 'F', 'Other'),
  birth_date DATE,
  phone VARCHAR(32) DEFAULT NULL,
  is_email_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cities (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  region VARCHAR(64),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS specializations (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS doctors (
  id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  specialization_id INT NOT NULL,
  city_id INT NOT NULL,
  visit_type ENUM('gabinet', 'online', 'both') NOT NULL DEFAULT 'both',
  address VARCHAR(255),
  phone VARCHAR(32),
  email VARCHAR(255),
  description TEXT,
  rating FLOAT DEFAULT 0,
  rating_count INT DEFAULT 0,
  experience_years INT DEFAULT 0,
  photo_url VARCHAR(255),
  price DECIMAL(10,2) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE,
  FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS services (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS doctor_services (
  doctor_id INT NOT NULL,
  service_id INT NOT NULL,
  PRIMARY KEY (doctor_id, service_id),
  FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
  FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS reviews (
  id INT NOT NULL AUTO_INCREMENT,
  doctor_id INT NOT NULL,
  user_id INT,
  rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS appointments (
  id INT NOT NULL AUTO_INCREMENT,
  doctor_id INT NOT NULL,
  user_id INT,
  appointment_date DATETIME NOT NULL,
  status ENUM('pending','confirmed','completed','cancelled') DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE doctors
  ADD COLUMN working_hours VARCHAR(255) DEFAULT '08:00-16:00' AFTER price,
  ADD COLUMN working_days VARCHAR(20) DEFAULT '01234' AFTER working_hours;

-- Przykładowe miasta
INSERT INTO cities (id, name, region) VALUES
(1, 'Warszawa', 'Mazowieckie'),
(2, 'Kraków', 'Małopolskie'),
(3, 'Wrocław', 'Dolnośląskie');

-- Przykładowe specjalizacje
INSERT INTO specializations (id, name, description) VALUES
(1, 'Kardiolog', 'Specjalista chorób serca i układu krążenia.'),
(2, 'Dermatolog', 'Specjalista chorób skóry.'),
(3, 'Pediatra', 'Lekarz dla dzieci i niemowląt.');

-- Przykładowe usługi
INSERT INTO services (id, name, description, price) VALUES
(1, 'Konsultacja ogólna', 'Podstawowa konsultacja lekarska.', 150.00),
(2, 'Badanie EKG', 'Standardowe badanie EKG serca.', 100.00),
(3, 'USG jamy brzusznej', 'Badanie USG brzucha.', 200.00);

-- Przykładowi użytkownicy
INSERT INTO users (id, email, password_hash, first_name, last_name, gender, birth_date, phone, is_email_confirmed) VALUES
(1, 'jan.kowalski@example.com', 'hash1', 'Jan', 'Kowalski', 'M', '1980-01-01', '501234567', 1),
(2, 'anna.nowak@example.com', 'hash2', 'Anna', 'Nowak', 'F', '1990-05-20', '502345678', 1);

-- Przykładowi lekarze
INSERT INTO doctors (id, first_name, last_name, specialization_id, city_id, visit_type, address, phone, email, description, rating, rating_count, experience_years, photo_url, price)
VALUES
(1, 'Jan', 'Kowalski', 1, 1, 'both', 'ul. Sezamkowa 1', '501234567', 'dr.jan.kowalski@example.com', 'Doświadczony kardiolog z ponad 15-letnim stażem.', 4.8, 5, 15, NULL, 200.00),
(2, 'Anna', 'Nowak', 2, 2, 'online', NULL, '502345678', 'dr.anna.nowak@example.com', 'Dermatolog specjalizujący się w leczeniu trądziku i chorób skóry.', 4.6, 3, 10, NULL, 180.00),
(3, 'Marek', 'Wiśniewski', 3, 3, 'gabinet', 'ul. Przykładowa 5', '503456789', 'dr.marek.wisniewski@example.com', 'Pediatra z pasją do pracy z dziećmi.', 4.9, 8, 20, NULL, 160.00);

-- Połączenia lekarz-usługa
INSERT INTO doctor_services (doctor_id, service_id) VALUES
(1, 1), (1, 2), (2, 1), (2, 3), (3, 1), (3, 3);

-- Opinie o lekarzach
INSERT INTO reviews (doctor_id, user_id, rating, comment) VALUES
(1, 1, 5, 'Świetny specjalista, bardzo pomocny!'),
(1, 2, 4, 'Profesjonalna obsługa, polecam.'),
(2, 2, 5, 'Wyleczyła mi cerę, bardzo miła.'),
(3, 1, 5, 'Dziecko nie boi się wizyt, super podejście.'),
(3, 2, 5, 'Polecam każdemu rodzicowi.');

-- Przykładowe wizyty
INSERT INTO appointments (doctor_id, user_id, appointment_date, status, notes)
VALUES
(1, 1, '2025-07-05 10:00:00', 'confirmed', 'Wizyta kontrolna po zawale'),
(2, 2, '2025-07-06 12:30:00', 'pending', 'Zmiany skórne na twarzy'),
(3, 1, '2025-07-07 09:00:00', 'completed', 'Szczepienie dziecka');