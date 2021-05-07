import random
from helpers import random_helper


def randomize_ship_part(randomized_db):
    c = randomized_db.cursor()
    part_names = ['weapon', 'hull', 'engine']  # TODO: заменить тоже на запрос

    # get all ship names
    c_ships_read = randomized_db.cursor()
    c_ships_read.execute(f'SELECT ship FROM Ships')
    ships = c_ships_read.fetchall()

    parts = fetch_parts(randomized_db, part_names)

    # update to new value
    for i in range(0, len(ships)):
        part_name = random.choice(part_names)

        new_value = random.choice(parts[part_name])[0]
        query = f'UPDATE Ships SET "{part_name}" = "{new_value}" WHERE ship = "{ships[i][0]}"'
        c.execute(query)


def fetch_parts(randomized_db, part_names):
    parts = {}
    for part_name in part_names:
        c = randomized_db.cursor()
        query = f'SELECT {part_name} FROM {part_name}s'
        c.execute(query)
        parts[part_name] = c.fetchall()
    return parts


def randomize_parts_value(randomized_db):
    # get tables names
    c_read_columns = randomized_db.cursor()
    c_read_columns.execute(f'SELECT name FROM sqlite_master WHERE type = "table"')
    tables_names = c_read_columns.fetchall()
    tables_names = [x for t in tables_names for x in t]
    del tables_names[0]

    # for each part table
    for table_name in tables_names:
        # get part table columns
        c_read_columns = randomized_db.cursor()
        c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("{table_name}")')
        columns = c_read_columns.fetchall()

        # get all data of part table
        c_ships_read = randomized_db.cursor()
        c_ships_read.execute(f'SELECT * FROM "{table_name}"')
        data = c_ships_read.fetchall()

        # for each part of ship
        for data_entry in data:
            random_component_index = random.randint(1, len(data_entry)-1)

            # update with random value
            rand_value = random_helper.randint_component()
            c_part_read = randomized_db.cursor()
            query = f'UPDATE "{table_name}" SET "{columns[random_component_index][0]}" = "{rand_value}" WHERE "{columns[0][0]}" = "{data_entry[0]}"'
            c_part_read.execute(query)
