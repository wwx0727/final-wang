# COSC 516 Final Exam

**This is an individual take home exam. No communication with others is allowed. You may use course and Internet resources.**

**The exam is available from Saturday, December 17th at 8 a.m. until Sunday, December 18th at 8 p.m. (36 hours).**

**Submit the exam by pushing to your GitHub repository and submitting your repository URL on Canvas.**

## Problem Statement

Our company is creating the next top mobile game with the goal of supporting millions of users and making billions of dollars. Although the game may start off small, the system should scale to support millions of customers. Your goal is to design the database to support this mobile game.

Our designers are currently working on the game itself, but here is an overview of what is expected for the database and how it works with the game.

1) Each user has a `GameState` that tracks their current status in the game. When the mobile game app is launched, the app immediately queries the database to retrieve this game state. The `GameState` has the following structure:
  - `id` - integer, unique for each player (may be auto-assigned)
  - `statetime` - timestamp, the last time the game state was changed
  - `region` - integer, players are divided into regions to make it possible to scale to many players. A player stays in their region for the entire game.
  - `name` - string (user may change at any time)
  - `email` - user contact email
  - `gold` - integer, gold is a measure of currency in the game
  - `power` - integer, power is a measure of player strength in the game
  - `level` - integer, level is a measure of player progress in the game
  
2) When the user interacts with the game, an event is generated. The event is sent from the app to the server. The server processes the event to make sure it is valid. If it is valid, it updates the game state and returns it to the app. The server stores the updated game state and the `GameEvent` in the database. Game events will not be changed once they are stored in the database. A `GameEvent` has the following structure:
  - `eventid` - integer, unique number (may be auto-assigned)
  - `userid` - integer, unique for each player
  - `eventtime` - timestamp, the time the game event was generated
  - `type` - integer, event type is a number representing a game event type such as 1 - buy power, 2 - get gold, 3 - level up
  - `diffgold` - integer, positive or negative number indicating change of gold
  - `diffpower` - integer, positive or negative number indicating change of power
  - `difflevel` - integer, number indicating change of level

3) The most important database operation is extremely fast read of the game state to send it to the player when requested. The database must also process game state updates and game event inserts quickly.

4) One common query is to show the top 10 players in a region. This should be near real-time but does not always have to reflect the most recent information.

5) For marketing to players, the system will periodically execute queries to determine players that have high activity (lots of events) in a given time. This information will be used to market bundles for players to purchase. This query does not have to be as fast as it does not effect the immediate game play for users.


## Part I: Describe Possibilities and Your Solution (10 marks)

Create a document consisting of no more than **4 pages** that describes at least 3 different database systems and how they may apply to the problem. Provide benefits and challenges with each system. Select a particular database system and argue why it is the best choice for this problem. Note: The database system chosen does not have to be the same database system that you implement in the second part. Relational databases are valid for comparison and to select as the best choice.

### Marking Guide

- +2 marks for explaining some of the considerations of the problem (data size, queries, consistency, etc.).
- +3 marks for providing benefits/challenges with at least 3 potential database systems
- +2 marks for arguing why you would select a particular database
- +3 marks for writing style, organization, and grammar

## Part II: Implement a Solution (20 marks)

Implement a database system that solves the problem statement. Create unit tests that verify that the data is loaded and queried properly. You may select any database except a traditional relational database such as MySQL/PostgreSQL/Azure SQL Server. Submit your code and a screenshot of the tests passing within your repository.

### Marking Guide

- +2 marks - Write a method `create()` to create structures in the database to store data.

- +3 marks - Write a method `load()` to load two data sets: `GameState` stores current game state for each player and `GameEvent` that stores information on each game event that changes a player's state.

- +2 marks - Write a method `update()` that updates the current game state for a player.

- +2 marks - Write a method `query1()` that returns the game state for a player given the player `id`. Return a string with the state information in any format. **Test for id=`1` and id=`949`.**

- +3 marks - Write a method `query2()` that returns the top 10 players by level in a given region. **Test for region `1` and region `9`.**

- +3 marks - Write a method `query3()` that returns the top 5 most active players between time X and Y in a given region. Active players are determined based on the number of game events that they have in the time range. **Test for region `2` between `2022-12-17 05:30:00` and `2022-12-17 15:00:00` and for region `7` between `2022-12-18 00:00:00` and `2022-12-19 11:00:00`.**

- +5 marks - Write unit tests to demonstrate that your previously constructed methods are working properly.

