-- Initialize an admin in the testing database

INSERT INTO user (
    id, first_name, last_name, email, hashed_password, is_active, is_admin,
    created_at, updated_at, photo_url
    )
    VALUES (
        "057ee079-a4b5-4de1-af12-b14fff8e90b3", "Admin", "Admin", "admin@hbnb.com",
        "$argon2id$v=19$m=62500,t=2,p=2$0tnvcK7OXJghDSOlMeu19A$v+q44IHr2ctzwfdYn57g/U8VjNkBKnNb",
        1, 1, "2025-06-27 09:49:42.825168", "2025-06-27 09:49:42.825168",
        "https://hubfi.fr/wp-content/uploads/2023/09/sites-obtenir-images-libres-droits-gratuitement-1160x680.jpg"
    );