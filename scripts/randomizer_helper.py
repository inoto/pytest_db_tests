import random


def randomize_ship_part(randomized_db):
    c = randomized_db.cursor()
    part_names = ['weapon', 'hull', 'engine']

    # получается все названия кораблей
    c_ships_read = randomized_db.cursor()
    c_ships_read.execute(f'SELECT ship FROM Ships')
    ships = c_ships_read.fetchall()
    # print(f'ships: {ships}')

    # получаем новое значение
    parts = fetch_parts(randomized_db, part_names)
    # print(f'parts: {parts}')
    # part_value = get_random_part_value(dest, part_name)

    # применяем новое значение
    for i in range(0, len(ships)):
        part_name = random.choice(part_names)

        new_value = random.choice(parts[part_name])[0]
        query = f'UPDATE Ships SET "{part_name}" = "{new_value}" WHERE ship = "{ships[i][0]}"'
        # print(f'query: {query}')
        c.execute(query)


def fetch_parts(dest, part_names):
    parts = {}
    for part_name in part_names:
        c = dest.cursor()
        query = f'SELECT {part_name} FROM {part_name}s'
        c.execute(query)
        parts[part_name] = c.fetchall()
    return parts


def get_random_part_value(dest, part_name):
    c = dest.cursor()
    query = f'SELECT {part_name} FROM {part_name}s'
    c.execute(query)
    data = c.fetchall()
    # print(f'data: {data}')


def randomize_parts_value(randomized_db):
    c = randomized_db.cursor()
    part_tables = ['weapons', 'hulls', 'engines']
    part_names = ['weapon', 'hull', 'engine']

    # для каждой таблицы частей корабля
    for part_table in part_tables:
        # print(f'part_table: {part_table}')

        c_read_columns = randomized_db.cursor()
        c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("{part_table}")')
        columns = c_read_columns.fetchall()
        # print(f'columns: {columns}')

        c_ships_read = randomized_db.cursor()
        c_ships_read.execute(f'SELECT * FROM "{part_table}"')
        data = c_ships_read.fetchall()
        # print(f'data: {data}')

        # для каждой части корабля
        for data_entry in data:
            # print(f'data_entry: {data_entry}')

            for index in range(1, len(data_entry)):
                rand_value = random.randint(1, 20)
                # print(f'component name: {columns[index][0]}, value: {data_entry[index]}')
                c_part_read = randomized_db.cursor()
                query = f'UPDATE "{part_table}" SET "{columns[index][0]}" = "{rand_value}" WHERE "{columns[0][0]}" = "{data_entry[0]}"'
                # print(f'query: {query}')
                c_part_read.execute(query)

    randomized_db.commit()
