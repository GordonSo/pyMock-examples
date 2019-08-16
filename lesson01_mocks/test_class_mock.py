from pytest_mock import MockFixture
from unittest import mock
from dataclasses import dataclass


original_value = 1
hijacked_value = 2


@dataclass()
class B:

    value: str = original_value


@dataclass()
class A:

    b: B = B()

    def do_something(self):
        return self.b.value


def test_no_mock():

    a: A = A()
    result = a.do_something()
    assert result == original_value


# How to mock a class
def test_mock_class():

    # Let's hijack the entire class instead of just the function inside
    # We will first create a class mock so we can inject it as a replacement
    b_mock = mock.MagicMock(B)
    # let's make the class's function return a different dictionary value of 3
    b_mock.value = hijacked_value

    # Let's call the class method
    a = A()
    a.b = b_mock
    result = a.do_something()

    # And assert that the value has been overridden
    assert result == hijacked_value


# How to mock a class
def test_pytest_mock_class(mocker: MockFixture):

    # Let's hijack the entire class instead of just the function inside
    # We will first create a class mock so we can inject it as a replacement
    b_mock = mock.MagicMock(B, "do_something", return_value=hijacked_value)

    # We will patch the A class
    mock_do_something_method = mocker.patch('lesson01_mocks.test_class_mock.B', return_value=b_mock)

    # Let's call the class method
    a = A()
    type(a.b)
    result = a.do_something()

    assert mock_do_something_method.is_called_once_with()
    # And assert that the value has been overridden
    assert result == hijacked_value
