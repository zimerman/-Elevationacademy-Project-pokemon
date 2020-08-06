USE sql_pokemon;

CREATE TABLE pokemon(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20),
    height FLOAT,
    weight FLOAT
);

CREATE TABLE trainers(
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE type(
    name VARCHAR(20) PRIMARY KEY
);

CREATE TABLE pokemontype(
    id_pokemon INT,
    name_type VARCHAR(20),
    PRIMARY KEY(name_type,id_pokemon),
    FOREIGN KEY(id_pokemon) REFERENCES pokemon(id),
    FOREIGN KEY(name_type) REFERENCES type(name)
);

CREATE TABLE ownedby(
    id_pokemon INT,
    name_pokemon VARCHAR(20),
    name_trainer VARCHAR(20),
    PRIMARY KEY(name_pokemon, name_trainer),
    FOREIGN KEY(id_pokemon) REFERENCES pokemon(id),
    FOREIGN KEY(name_trainer) REFERENCES trainers(name)
);

CREATE TABLE food(
    name VARCHAR(20) PRIMARY KEY
)


CREATE TABLE sensitive_food(
    name_food VARCHAR(20),
    name_type VARCHAR(20),
    PRIMARY KEY(name_food, name_type),
    FOREIGN KEY(name_food) REFERENCES food(name),
    FOREIGN KEY(name_type) REFERENCES type(name)
)
