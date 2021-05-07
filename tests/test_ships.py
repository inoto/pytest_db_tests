import pytest


def test_ships(use_source_db, use_randomized_db, parametrize_ships):
    errors = []

    source_db = use_source_db
    randomized_db = use_randomized_db

    ship_name = parametrize_ships[0]
    part_column_name = parametrize_ships[1]
    part_name = parametrize_ships[2]

    # check part

    cs = source_db.cursor()
    cs.execute(f'SELECT "{part_column_name}" FROM Ships WHERE ship = "{ship_name}"')
    data = cs.fetchone()

    cr = randomized_db.cursor()
    cr.execute(f'SELECT "{part_column_name}" FROM Ships WHERE ship = "{ship_name}"')
    data_rand = cr.fetchone()

    part_source = data[0]
    part_randomized = data_rand[0]

    try:
        assert part_source == part_randomized
    except AssertionError as e:
        errors.append(f'expected {part_source}, was {part_randomized}')

    # check components of the part

    c_read_columns = source_db.cursor()
    c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("{part_column_name}s")')
    part_table_columns = c_read_columns.fetchall()
    part_table_columns = [x for t in part_table_columns for x in t]
    del part_table_columns[0]

    cs = source_db.cursor()
    cs.execute(f'SELECT * FROM "{part_column_name}s" WHERE "{part_column_name}" = "{part_name}"')
    value_source = cs.fetchall()

    cr = randomized_db.cursor()
    cr.execute(f'SELECT * FROM "{part_column_name}s" WHERE "{part_column_name}" = "{part_name}"')
    value_randomized = cr.fetchall()

    for i in range(1, len(value_source[0])):
        try:
            assert value_source[0][i] == value_randomized[0][i]
        except AssertionError as e:
            errors.append(f'{part_table_columns[i - 1]}: expected {value_source[0][i]}, was {value_randomized[0][i]}')

    assert len(errors) == 0, f'{ship_name}, {part_randomized} - {errors}'
