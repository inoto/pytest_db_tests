import pytest


@pytest.mark.parametrize('dummy1', [(1,2,3), (4,5,6), (7,8,9)])
@pytest.mark.parametrize('dummy2', [(1,2,3), (4,5,6), (7,8,9)])
def test_dummy(dummy1, dummy2):
    pass
