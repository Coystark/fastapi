import pytest

from app.adapters.sum import sum_numbers


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (2, 2, 4),
        (3, 2, 5),
    ],
)
def test_sum_numbers(a: int, b: int, expected: int):
    assert sum_numbers(a, b) == expected
