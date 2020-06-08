DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS dogs;
DROP TABLE IF EXISTS dog_habbits;
DROP TABLE IF EXISTS dog_last;
DROP TABLE IF EXISTS dog_owners;
DROP TABLE IF EXISTS dog_weights;
DROP TABLE IF EXISTS dog_guides;
DROP TABLE IF EXISTS dog_walks;
DROP TABLE IF EXISTS dog_commands;
DROP TABLE IF EXISTS dog_training_link;
DROP TABLE IF EXISTS dog_training;
DROP TABLE IF EXISTS dog_training_progress;
DROP TABLE IF EXISTS loo_breaks;



CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NULL,
  first_name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE dogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NULL,
    dob DATE NULL,
    bread TEXT NULL,
    gender TEXT NULL
);

CREATE TABLE dog_habbits (
    dog_id INTEGER UNIQUE NOT NULL,
    daily_feeds INTEGER NULL,
    food_intervals INTEGER NULL,
    loo_intervals INTEGER NULL,
    daily_walks INTEGER NULL,
    walk_intervals INTEGER NULL,
    alone_intervals INTEGER null
);

CREATE TABLE dog_last (
    dog_id INTEGER NOT NULL,
    last_loo_break TIMESTAMP NULL,
    last_fed TIMESTAMP NULL,
    last_weighed TIMESTAMP NULL
);

CREATE TABLE loo_breaks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    break_time TIMESTAMP NOT NULL,
    loo_type TEXT NOT NULL
);

CREATE TABLE dog_owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL
);

CREATE TABLE dog_weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    measured_by INTEGER NOT NULL,
    weight REAL NOT NULL,
    date_measured DATE NULL
);

CREATE TABLE dog_guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE dog_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT UNIQUE NOT NULL,
    level TEXT NOT NULL,
    description BLOB NULL
);

CREATE TABLE dog_training (
    dog_id INTEGER NOT NULL,
    command_id INTEGER NOT NULL,
    score INTEGER NOT NULL
);

CREATE TABLE dog_training_link (
    dog_id INTEGER NOT NULL,
    command_id INTEGER NOT NULL
);

CREATE TABLE dog_training_progress (
    dog_id INTEGER NOT NULL,
    command_id INTEGER NOT NULL,
    command_progress INTEGER NOT NULL,
    rec_date TIMESTAMP NOT NULL
);

CREATE TABLE dog_walks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    behaviour_score INTEGER NULL,
    callback_score INTEGER NULL,
    socialised_score INTEGER NULL,
    total_score INTEGER NULL,
    loc TEXT NULL,
    notes TEXT NULL,
    walked_date TIMESTAMP NULL
);


-- Add a user
INSERT INTO users (first_name, surname, email, password) VALUES
    ('Craig', 'Attwood', 'admin@admin', 'pbkdf2:sha256:150000$gel9CvHW$ff526d0db176b2a91023afaecd31fa92f00625444f5c5f9a314f04bf5bc43499');

-- Add a dog
INSERT INTO dogs (name, dob, gender, bread) VALUES
    ('Tiggie', '2020-04-13', 'F', 'CockerSpaniel'),
    ('Milo', '2020-10-1', 'M', 'CockerPoo');

INSERT INTO dog_last (dog_id, last_loo_break, last_fed, last_weighed) VALUES
    (1, null, null, null),
    (2, null, null, null);

-- assign dogs to users
INSERT INTO dog_owners (dog_id, user_id) VALUES
    (1,1),
    (2,1);

-- add dummy data for weight graphs
INSERT INTO dog_weights (dog_id, measured_by, weight, date_measured) VALUES
    (1, 1, 1.6, "2020-04-28"),
    (1, 1, 2.0, "2020-05-01"),
    (1, 1, 2.1, "2020-05-13"),
    (1, 1, 2.7, "2020-05-20"),
    (1, 1, 3.0, "2020-05-27"),
    (2, 1, 3.0, "2020-03-27"),
    (2, 1, 3.0, "2020-03-31");

-- add dog commands
INSERT INTO dog_commands (command, level) VALUES
    ('Sit', 'Easy'),
    ('Down', 'Easy'),
    ('Road Trip', 'Hard');

-- Link dogs to commands
INSERT INTO dog_training_link (dog_id, command_id) VALUES
    (1,1), (1,2), (1,3);

INSERT INTO dog_training_progress (dog_id, command_id, command_progress, rec_date) VALUES
    (1, 1, 1, "2020-06-03 12:44:11.598258"), (1, 1, 2, "2020-06-03 12:44:11.598258"), (1, 1, 3, "2020-06-03 12:44:11.598258"), (1, 1, 4,"2020-06-03 12:44:11.598258");

