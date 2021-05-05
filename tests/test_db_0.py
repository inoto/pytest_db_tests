import pytest


@pytest.mark.parametrize('part_name', ['weapon', 'hull', 'engine'])
def test_db_0(use_db, randomize_some_db_values, part_name):
    source_db = use_db
    randomized_db = randomize_some_db_values

    c = source_db.cursor()
    c.execute(f'SELECT ship FROM Ships')
    ships = c.fetchall()
    for ship in ships:
        print(f'ship: {ship[0]}')
        # берём значение из source
        cs = source_db.cursor()
        cs.execute(f'SELECT "{part_name}" FROM Ships WHERE ship = "{ship[0]}"')
        part_source = cs.fetchall()
        # берём значение из randomized
        cr = randomized_db.cursor()
        cr.execute(f'SELECT "{part_name}" FROM Ships WHERE ship = "{ship[0]}"')
        part_randomized = cr.fetchall()

        print(f'{part_source[0]} -> {part_randomized[0]}')

    # print(df.to_string())
    pass
