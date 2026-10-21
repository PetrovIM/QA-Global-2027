CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT
);

INSERT INTO users (username, email, age)
VALUES ('TESTOVY', 'testtestovich@test.test', 54);