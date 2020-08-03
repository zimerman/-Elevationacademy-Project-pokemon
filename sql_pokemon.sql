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

CREATE TABLE pokemontype(
    id_pokemon INT,
    name_type VARCHAR(20),
    PRIMARY KEY(name_type,id_pokemon),
    FOREIGN KEY(id_pokemon) REFERENCES pokemon(id)
);

CREATE TABLE ownedby(
    id_pokemon INT,
    name_trainer VARCHAR(20),
    PRIMARY KEY(id_pokemon,name_trainer),
    FOREIGN KEY(id_pokemon) REFERENCES pokemon(id),
    FOREIGN KEY(name_trainer) REFERENCES trainers(name)

);
