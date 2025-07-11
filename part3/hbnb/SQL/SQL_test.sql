-- A script to create table booking for HBnB
CREATE TABLE IF NOT EXISTS booking (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Trigger for booking.updated_at
CREATE TRIGGER IF NOT EXISTS update_booking_timestamp
AFTER UPDATE ON booking
FOR EACH ROW
BEGIN
    UPDATE booking SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- A script to create table user for HBnB
CREATE TABLE IF NOT EXISTS user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    photo_url VARCHAR(2048)
);

-- Trigger for user.updated_at
CREATE TRIGGER IF NOT EXISTS update_user_timestamp
AFTER UPDATE ON user
FOR EACH ROW
BEGIN
    UPDATE user SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- A script to create table place for HBnB
CREATE TABLE IF NOT EXISTS place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0) NOT NULL,
    latitude FLOAT CHECK (-90 <= latitude AND latitude <= 90) NOT NULL,
    longitude FLOAT CHECK (-180 <= longitude AND longitude <= 180) NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    rating DECIMAL(10, 1) CHECK (rating >= 0 AND rating <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    photos_url TEXT DEFAULT '[]' NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Trigger for place.updated_at
CREATE TRIGGER IF NOT EXISTS update_place_timestamp
AFTER UPDATE ON place
FOR EACH ROW
BEGIN
    UPDATE place SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- A script to create table amenity for HBnB
CREATE TABLE IF NOT EXISTS amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Trigger for amenity.updated_at
CREATE TRIGGER IF NOT EXISTS update_amenity_timestamp
AFTER UPDATE ON amenity
FOR EACH ROW
BEGIN
    UPDATE amenity SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- A script to create relationship table place_amenity for HBnB
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (amenity_id) REFERENCES amenity(id)
);

-- A script to create table reviews for HBnB
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    comment VARCHAR(2000) NOT NULL,
    rating DECIMAL(10, 1) CHECK (rating >= 0 AND rating <= 5) NOT NULL,
    place VARCHAR(36) NOT NULL,
    user_ide VARCHAR(36) NOT NULL,
    user_first_name VARCHAR(50) NOT NULL,
    user_last_name VARCHAR(50) NOT NULL,
    booking VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (place) REFERENCES place(id),
    FOREIGN KEY (user_ide) REFERENCES user(id),
    FOREIGN KEY (booking) REFERENCES booking(id)
);

-- Trigger for reviews.updated_at
CREATE TRIGGER IF NOT EXISTS update_reviews_timestamp
AFTER UPDATE ON reviews
FOR EACH ROW
BEGIN
    UPDATE reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Create an admin
INSERT INTO user (
	id, first_name, last_name, email, hashed_password,
	is_active, is_admin, created_at, updated_at)
	VALUES (
		'36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Test', 'Admin', 'ta@mail.com',
		'$argon2id$v=19$m=62500,t=2,p=2$0tnvcK7OXJghDSOlMeu19A$v+q44IHr2ctzwfdYn57g/U8VjNkBKnNb', 1, 1, '2025-06-30 14:43:50.268972',
		'2025-06-30 14:43:50.268972');

-- Create an user
INSERT INTO user (
    id, first_name, last_name, email, hashed_password,
    is_active, is_admin, created_at, updated_at)
    VALUES (
        '36b9050e-ddd3-4c3b-9731-9f487208bbc2', 'Test', 'User', 'tu@mail.com',
        '$argon2id$v=19$m=62500,t=2,p=2$/PWsZ7eOGqoqWehTtaIhHw$WN4njIDMhpZC8c2LVJwFaB0rz7hPTS/G', 1, 0, '2025-05-21 13:31:52.268972',
        '2025-05-21 13:31:52.268972');

-- Update a user
UPDATE user
SET email = "mail@example.com"
WHERE id = '36b9050e-ddd3-4c3b-9731-9f487208bbc2';

-- Create a place
INSERT INTO place(
    id, title, description, price, latitude, longitude, owner_id, created_at, updated_at,
    photos_url)
    VALUES(
        '361c87e3-8b6c-480c-8115-b81bda8f7116', 'Place testing', 'A place to test post route', 3.14,
        -2, 3.5746, '36b9050e-ddd3-4c3b-9731-9f487208bbc2', '2025-05-21 13:31:52.268972',
        '2025-05-21 13:31:52.268972', 'https://www.psdstack.com/wp-content/uploads/2019/08/copyright-free-images-750x420.jpg'
    );