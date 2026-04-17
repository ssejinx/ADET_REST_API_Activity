CREATE DATABASE IF NOT EXISTS art_db;
USE art_db;

CREATE TABLE IF NOT EXISTS artists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    bio TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pending_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    bio TEXT NOT NULL
);

INSERT INTO artists (username, bio) VALUES ('Jesslyn', 'Digital Artist'), ('Kirsten', 'Specializes in Painting'), ('Justin', 'Drawing')