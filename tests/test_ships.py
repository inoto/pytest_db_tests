import logging
import pytest


def test_ships(use_source_db, use_randomized_db, parametrize_ships):
    errors = []

    source_db = use_source_db
    randomized_db = use_randomized_db

    # print(f'par_db: {par_db}')

    cs = source_db.cursor()
    cs.execute(f'SELECT "{parametrize_ships[1]}" FROM Ships WHERE ship = "{parametrize_ships[0]}"')
    data = cs.fetchone()
    # print(f'data: {data}')

    cr = randomized_db.cursor()
    cr.execute(f'SELECT "{parametrize_ships[1]}" FROM Ships WHERE ship = "{parametrize_ships[0]}"')
    data_rand = cr.fetchone()
    # print(f'data rand: {data_rand}')

    part_source = data[0]
    part_randomized = data_rand[0]
    # print(f'{part_source} -> {part_randomized}')

    # if part_source != part_randomized:
    #     errors.append(f'expected {part_source}, was {part_randomized}')
    try:
        assert part_source == part_randomized
    except AssertionError as e:
        errors.append(f'expected {part_source}, was {part_randomized}')

    # print(f'argvalue: {par_db[0]}, {par_db[1]}, {par_db[2]}')

    part = parametrize_ships[1]

    c_read_columns = source_db.cursor()
    c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("{part}s")')
    part_table_columns = c_read_columns.fetchall()
    part_table_columns = [x for t in part_table_columns for x in t]
    del part_table_columns[0]

    cs = source_db.cursor()
    cs.execute(f'SELECT * FROM "{part}s" WHERE "{part}" = "{parametrize_ships[2]}"')
    value_source = cs.fetchall()
    # print(f'value_source: {value_source}')

    cr = randomized_db.cursor()
    cr.execute(f'SELECT * FROM "{part}s" WHERE "{part}" = "{parametrize_ships[2]}"')
    value_randomized = cr.fetchall()
    # print(f'value_randomized: {value_randomized}')

    for i in range(1, len(value_source[0])):
        # if value_source[0][i] != value_randomized[0][i]:
        #     errors.append(f'{part_table_columns[i-1]}: expected {value_source[0][i]}, was {value_randomized[0][i]}')
        try:
            assert value_source[0][i] == value_randomized[0][i]
        except AssertionError as e:
            errors.append(f'{part_table_columns[i - 1]}: expected {value_source[0][i]}, was {value_randomized[0][i]}')

    assert len(errors) == 0, f'{parametrize_ships[0]}, {part_randomized} - {errors}'
