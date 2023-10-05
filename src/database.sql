DROP DATABASE IF EXISTS cmiyc;
CREATE DATABASE cmiyc;

CREATE TABLE problems(
    title VARCHAR(50) PRIMARY KEY NOT NULL,
    difficulty VARCHAR(7) NOT NULL,
    consigns VARCHAR(1000) NOT NULL,
);



INSERT INTO problems (title, difficulty, consigns) VALUES ('Problem1', 'easy', "do it");
INSERT INTO problems (title, difficulty, consigns) VALUES ('Problem2', 'hard', "just do it");


SELECT * FROM problems