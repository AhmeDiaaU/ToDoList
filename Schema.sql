CREATE DATABASE IF NOT EXISTS todo;
USE todo;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    complete BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    c_id int  NOT Null ,
    FOREIGN KEY (user_id) REFERENCES  user(id) ON DELETE CASCADE,
    FOREIGN KEY (c_id) REFERENCES category(category_id) ON DELETE CASCADE,
    UNIQUE (user_id, title)
);
CREATE TABLE user_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NULL,
    address VARCHAR(255)  NULL,
    date_of_birth DATE NOT NULL,
    profile_picture VARCHAR(255) NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
CREATE TABLE tasks_Schedule(
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    end_time TIME NOT NULL,
    repeat_task BOOLEAN DEFAULT FALSE,
    repeat_interval ENUM('Daily', 'Weekly', 'Monthly') DEFAULT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);