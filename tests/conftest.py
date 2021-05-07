import os
import pytest
import definitions
from helpers.db_helper import DBHelper
from helpers.db_randomizer_helper import randomize_ship_part, randomize_parts_value


@pytest.fixture(scope="session")
def use_source_db():
    source_db = DBHelper(definitions.DB_PATH)
    yield source_db.connection
    source_db.close()


@pytest.fixture(scope="session")
def use_randomized_db(use_source_db):
    source_db = use_source_db

    if os.path.exists(definitions.RANDOMIZED_DB_PATH):
        os.remove(definitions.RANDOMIZED_DB_PATH)
    # we can see randomized db for debug purposes if put to the disk
    randomized_db = DBHelper(definitions.RANDOMIZED_DB_PATH)
    source_db.backup(randomized_db.connection)

    randomize_ship_part(randomized_db.connection)
    randomize_parts_value(randomized_db.connection)

    randomized_db.connection.commit()

    yield randomized_db.connection
    randomized_db.close()


def pytest_generate_tests(metafunc):
    # find specific fixture
    if definitions.RANDOMIZED_DB_PARAMETRIZATION_NAME in metafunc.fixturenames:
        source_db = DBHelper(definitions.DB_PATH)

        # get ship names
        c = source_db.connection.cursor()
        c.execute(f'SELECT * FROM Ships')  # TODO: вынести Ships в константу?
        ship_names = c.fetchall()

        # get ships table columns
        c_read_columns = source_db.connection.cursor()
        c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("Ships")')
        ships_table_columns = c_read_columns.fetchall()
        ships_table_columns = [x for t in ships_table_columns for x in t]
        del ships_table_columns[0]

        argvalues = []
        ids = []
        # fill values for parametrization
        for ship_name in ship_names:
            for part_name in ships_table_columns:
                specific_row_index = ships_table_columns.index(part_name)
                argvalues.append((ship_name[0], part_name, ship_name[specific_row_index+1]))
                ids.append(f'{ship_name[0]}, {part_name}')

        source_db.close()

        if not argvalues:
            raise ValueError("Values not loaded")

        return metafunc.parametrize(definitions.RANDOMIZED_DB_PARAMETRIZATION_NAME, argvalues, ids=ids, scope='session')
