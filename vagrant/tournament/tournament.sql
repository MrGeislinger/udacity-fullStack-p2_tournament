-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Only  create database if it doesn't exist
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Once registered into a tournament, player keeps the same ID
CREATE TABLE registeredPlayers (
    id SERIAL primary key,
    name TEXT
 );

-- Possibly not needed; could be combined into "tournaments" table
CREATE TABLE playersInTournament (
    player INTEGER references registeredPlayers (id),
    primary key (player)
);

-- Same number of matches for each round
CREATE TABLE rounds (
    matchId SERIAL primary key,
    winner INTEGER references registeredPlayers (id),
    loser INTEGER references registeredPlayers (id),
    tie INTEGER-- 1 for tie and 0 not tie
);
