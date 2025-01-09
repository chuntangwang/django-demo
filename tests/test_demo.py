import pytest


def f():
    return 3


def test_function():
    assert f() == 4, "result of f() should be 4"


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
