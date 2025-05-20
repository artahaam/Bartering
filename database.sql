CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(11) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    age INTEGER,
    password NOT NULL VARCHAR(255)
)

CREATE TABLE supports(
    id INTEGER NOT NULL REFERENCES users(id),
    email VARCHAR(50) NOT NULL UNIQUE,
    job_description TEXT
)

CREATE TABLE currencies(
    id SERIAL PRIMARY KEY,
    is_item BOOLEAN NOT NULL,
    is_service BOOLEAN NOT NULL,
    name VARCHAR(30),
    description TEXT
)

CREATE TABLE offers(
    id SERIAL PRIMARY KEY,
    offerd_by INTEGER REFERENCES users(id),
    accepted_by INTEGER REFERENCES users(id),
    to_get INTEGER REFERENCES currencies(id),
    to_give INTEGER REFERENCES currencies(id),
    date DATE,
    type VARCHAR(30)
)

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    sender INTEGER NOT NULL REFERENCES users(id),
    receiver INTEGER NOT NULL REFERENCES users(id),
    text TEXT,
    date DATE
)

CREATE TABLE offer_proposal(
    id SERIAL PRIMARY KEY,
    proposer_id INTEGER NOT NULL REFERENCES users(id),
    offer_id INTEGER NOT NULL REFERENCES offers(id),
    proposed_currency INTEGER REFERENCES currencies(id),
    created_at DATE

)

CREATE TABLE comments(
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id),
    parent_id INTEGER REFERENCES comments(id),
    created_at DATE,
    text TEXT
)


CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    title VARCHAR(30),
    description TEXT
)

CREATE TABLE comments_offers(
    id SERIAL PRIMARY KEY,
    comment_id INTEGER NOT NULL REFERENCES comments(id),
    offer_id INTEGER NOT NULL REFERENCES offers(id)
)

CREATE TABLE currencies_categories(
    id SERIAL PRIMARY KEY,
    id INTEGER REFERENCES currencies(id),
    category_id INTEGER REFERENCES categories(id)
)