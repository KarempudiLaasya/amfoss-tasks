## approach:

### setting up the bot

i created the discord bot using discord.py. i turned on the message content intent so that the bot can read commands such as `!bounty`, `!shop`, etc. and i have added `on_ready()` event to check if bot got connected properly.

### planning the database

before implementing the commands, i decided what information needed to be stored permanently. i used sqlite since it is lightweight and doesn't require a separate database server.

i then created four tables to store data

- `users` – to store discord id, berry balance and daily reward date.
- `shop` – this stores the available items, their costs and effects.
- `inventory` – stores the items owned by each user.
- `history` – stores berry-related actions and their timestamps.

### making database functions

i kept the sql operations in `database.py` instead of putting them directly inside the discord commands. functions like `get_user()`, `get_balance()`, `claim_daily()` and `buy_item()` handle the database operations.

i also made `get_user()` create a new user with the default 500 berries if they use the bot for the first time.

### building the economy

i implemented the basic commands first: `!bounty` to check the balance, `!setsail` to claim the daily reward, and `!trade` to transfer berries between users.

for the daily reward, i stored the date of the last claim and compared it with the current date so that the reward cannot be claimed twice on the same day.

### adding the shop and inventory

i stored the shop items in the database rather than hardcoding them in the command. when a user buys an item, the bot checks if the item exists and if the user has enough berries. if the purchase is successful, then the balance gets reduced and item is added to the inventory, and the purchase is added to the history.

### adding raids and leaderboard

for `!raid`, i used a random success or failure outcome.if it is a successful raid then part of berries of victim would be added to the attacker otherwise they would lose some.

for `!worstgeneration`, i used an sql query to sort users by their berry balance and return the top five.

### adding the one piece api

for `!logpose`, i used the requests library to get character data from the one piece api. i randomly select a character from the response and display information such as their name, bounty, crew and devil fruit.

### keeping track of activity

i added the history table so that important economy actions don't just disappear after they happen. the `!history` command retrieves the user's recent transactions and displays the action, amount and timestamp.

### testing

i tested the commands in discord and also tried cases where things should fail, like claiming the daily reward twice, buying an item without enough berries, trading with myself, and trying to raid myself.
