CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(11) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    age INTEGER,
    password VARCHAR(255)
)

CREATE TABLE supports(
    support_id INTEGER REFERENCES users(user_id),
    email VARCHAR(50) NOT NULL UNIQUE,
    job_description TEXT
)

CREATE TABLE currencies(
    currency_id SERIAL PRIMARY KEY,
    is_item BOOLEAN NOT NULL,
    is_service BOOLEAN NOT NULL,
    name VARCHAR(30),
    description TEXT
)

CREATE TABLE offers(
    offer_id SERIAL PRIMARY KEY,
    offerd_by INTEGER REFERENCES users(user_id),
    accepted_by INTEGER REFERENCES users(user_id),
    to_get INTEGER REFERENCES currencies(currency_id),
    to_give INTEGER REFERENCES currencies(currency_id),
    date DATE,
    type VARCHAR(30)
)

CREATE TABLE messages(
    message_id SERIAL PRIMARY KEY,
    sender INTEGER REFERENCES users(user_id),
    receiver INTEGER REFERENCES users(user_id),
    text TEXT,
    date DATE
)

CREATE TABLE offer_proposal(
    proposer_id INTEGER NOT NULL REFERENCES users(user_id),
    offer_id INTEGER NOT NULL REFERENCES offers(offer_id),
    proposed_currency INTEGER REFERENCES currencies(currency_id),
    created_at DATE

)

ALTER TABLE supports ALTER COLUMN support_id SET NOT NULL

ALTER TABLE messages ALTER COLUMN message_id SET NOT NULL

ALTER TABLE messages ALTER COLUMN sender SET NOT NULL

ALTER TABLE messages ALTER COLUMN receiver SET NOT NULL

ALTER TABLE currencies ALTER COLUMN description SET NOT NULL

ALTER TABLE users ALTER COLUMN password SET NOT NULL


CREATE TABLE comments(
    comment_id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(user_id),
    parent_id INTEGER REFERENCES comments(comment_id),
    created_at DATE,
    text TEXT
)


CREATE TABLE categories(
    category_id SERIAL PRIMARY KEY,
    title VARCHAR(30),
    description TEXT
)

CREATE TABLE comments_offers(
    comment_id INTEGER NOT NULL REFERENCES comments(comment_id),
    offer_id INTEGER NOT NULL REFERENCES offers(offer_id)
)

CREATE TABLE currencies_categories(
    currency_id INTEGER REFERENCES currencies(currency_id),
    category_id INTEGER REFERENCES categories(category_id)
)

ALTER TABLE comments ADD COLUMN offer_id INTEGER REFERENCES offers(offer_id)

ALTER TABLE comments ALTER COLUMN offer_id SET NOT NULL 