
# - Display people and their phone numbers

SELECT * FROM users JOIN phone_numbers ON u_id = u_id;

# - Display people and their addresses
SELECT * FROM users JOIN addresses ON u_id = u_id;


# - Display people and their addresses only if they are in the state of California

# for query below, depends on how state is stored and if there is room for typos.
# example 1:
SELECT * FROM users JOIN addresses a ON u_id = a.u_id WHERE a.state = 'CA';
SELECT * FROM users JOIN addresses a ON u_id = a.u_id WHERE a.state IN ('CA', 'ca', 'Ca', 'cA');

# - Show how many people have addresses in each state
SELECT a.state, COUNT(a.state) FROM addresses a GROUP BY a.state;

# - Show the % of people that have multiple addresses
SELECT round(100.0 * 
	(SELECT COUNT(*) FROM
		(SELECT user_id, COUNT(addresses.a_id) FROM addresses GROUP BY user_id HAVING COUNT(addresses.a_id) > 1) AS x)
	 / COUNT(*))
	FROM users;


# First goal is normalization, avoid repeating data, have every piece of information live in exactly one place.
# To achieve that goal, store phone numbers and addresses in separate tables from user information, so that
# user information does not need to be repeated.

# Second goal is referential integrity, which will prevent a) storing invalid data and b) deleting data that is
# still referenced in another table.


# I added an email field that is required and must be unique to avoid (as much as possible) duplicate entries.
# This could also be achieved through a username which must be unique.

CREATE TABLE users (
		u_id SERIAL PRIMARY KEY,
		first_name VARCHAR(64),
		last_name VARCHAR(64),
		email VARCHAR(128) NOT NULL UNIQUE
	);


# A big decision here is in what format to store the phone numbers, and depends on how the phone number is retrieved
# from the user. For example, if it is an online form that already goes through validation before submitting, and
# will always return in a specific format, it could make sense to store as an integer. Alternatively, if it is based
# on user input, storing as a string will allow for more flexibility.

# The phone_numbers table has a foreign key relationship to the users table based on the user_id.
# Here also, I thought about adding a UNIQUE constraint to the phone number but opted not to because some
# users might list a business phone number, which could be the same for employees of the same business.

CREATE TABLE phone_numbers (
		p_id SERIAL PRIMARY KEY,
		phone VARCHAR(64) NOT NULL,
		u_id INTEGER REFERENCES users
	);

# The addresses table has a foreign key relationship to the users table based on the user_id.

CREATE TABLE addresses (
		a_id SERIAL PRIMARY KEY,
		street VARCHAR(128),
		street2 VARCHAR(128),
		city VARCHAR(64),
		state VARCHAR(64) NOT NULL,
		zipcode VARCHAR(64) NOT NULL,
		u_id INTEGER REFERENCES users
	);

# If these users will only be from the United States, I might create a seed table for referential integrity
# that stores the valid states that could be added to the addresses table.
# If implemented, I would add "REFERENCES states" to the 'state' field in the addresses table.

CREATE TABLE states (
		s_id SERIAL PRIMARY KEY,
		state VARCHAR(32)
	);