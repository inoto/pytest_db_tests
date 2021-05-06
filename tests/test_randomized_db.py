import pytest


def test_randomized_db(use_source_db, use_randomized_db, par_db):
    source_db = use_source_db
    randomized_db = use_randomized_db

    # print(f'par_db: {par_db}')

    cs = source_db.cursor()
    cs.execute(f'SELECT "{par_db[1]}" FROM Ships WHERE ship = "{par_db[0]}"')
    data = cs.fetchone()
    # print(f'data: {data}')

    cr = randomized_db.cursor()
    cr.execute(f'SELECT "{par_db[1]}" FROM Ships WHERE ship = "{par_db[0]}"')
    data_rand = cr.fetchone()
    # print(f'data rand: {data_rand}')

    part_source = data[0]
    part_randomized = data_rand[0]
    # print(f'{part_source} -> {part_randomized}')
    assert part_source == part_randomized, f'{part_source} -> {part_randomized}'
