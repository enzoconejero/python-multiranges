import pytest

from multiranges import MultiRange, arg_to_range
from multiranges.exceptions import NoRangeableObjectError


@pytest.mark.parametrize('arg, _range', [
    (1, range(1)),
    ((5, 9), range(5, 9)),
    (['1', 2, '1234'], ['1', 2, '1234']),
    (range(41), range(41)),
    ((1, 2, 3, 4), [1, 2, 3, 4]),
    ({1, 2, 3}, [1, 2, 3])
])
def test_arg_to_range(arg, _range):
    assert arg_to_range(arg) == _range


def test_arg_to_range_error():
    with pytest.raises(NoRangeableObjectError):
        arg_to_range(object())


def test_single_int_mr_gives_list_of_ints():
    mr = MultiRange(5)
    assert list(mr) == [0, 1, 2, 3, 4]


def test_string_mr_gives_list_of_chars():
    mr = MultiRange('iamatest')
    assert list(mr) == ['i', 'a', 'm', 'a', 't', 'e', 's', 't']


def test_empty_mr_give_empty_list():
    mr = MultiRange()
    assert list(mr) == []


@pytest.mark.parametrize('ranges, lenght', [
    ([1, 5], 5),
    ([115], 115),
    ([['+', '-'], range(5, 9), 10], 2 * 4 * 10),
    ([], 0)
])
def test_lenghts(ranges, lenght):
    mr = MultiRange(*ranges)
    assert len(mr) == lenght


def test_mr_returns():
    mr = MultiRange(['+', '-'], range(2), 'e', range(3))
    expecs = [
        ('+', 0, 'e', 0), ('+', 0, 'e', 1), ('+', 0, 'e', 2),
        ('+', 1, 'e', 0), ('+', 1, 'e', 1), ('+', 1, 'e', 2),
        ('-', 0, 'e', 0), ('-', 0, 'e', 1), ('-', 0, 'e', 2),
        ('-', 1, 'e', 0), ('-', 1, 'e', 1), ('-', 1, 'e', 2),
    ]
    for i, t in enumerate(mr):
        assert expecs[i] == t


def test_high_index_raises_index_error():
    mr = MultiRange(2, 3)
    with pytest.raises(IndexError):
        _ = mr[144]


def test_indexes():
    mr = MultiRange(12, 21)
    assert mr[0] == (0, 0)
    assert mr[21] == (1, 0)
    assert mr[len(mr) - 1] == (11, 20)


def test_nested_mr():
    mr1 = MultiRange(['+', '-'], 3)
    mr2 = MultiRange(5, mr1)
    assert mr1[0] == ('+', 0)
    assert list(mr2)[0] == (0, ('+', 0))


def test_indexes_with_nested_mr():
    mr = MultiRange(3, MultiRange('hello', range(2, 4)), 'world')
    assert mr[0] == (0, ('h', 2), 'w')
    assert mr[4] == (0, ('h', 2), 'd')
    assert mr[5] == (0, ('h', 3), 'w')
    assert mr[9] == (0, ('h', 3), 'd')
    assert mr[10] == (0, ('e', 2), 'w')
