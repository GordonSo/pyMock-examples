from unittest import mock
import pytest_mock

"""
This tutorial contains a number of test function to demonstrate different ways to mock a function
Each of this function can be run or debug individually and have the following setup:
 - class A with has a function do_something that will to return a given value as-is
Every test will calls the function with an input value 1 
 and will mock the function to get the result to return an hijack value of 2
"""


# Here is our demo setup
class A:
    def do_something(self, _input_value):
        return {"value": _input_value}


input_value = 1
hijack_value = 2


# Let start with running the test end-to-end without mock
def test_without_mock():

    # Given we will create an instance
    a = A()

    # When we call the instance to do something with value X
    result = a.do_something(input_value)

    # Then the result should be value X
    assert result["value"] == input_value


# 1) To mock a function (by forcing your way through)
# Let's hijack the do_something function inside the A class object
def test_hijack_a_function():

    # class an instance
    a = A()

    # We can re-assign the do_something attribute to a 'MagicMock' object with a return value
    # NB: mock.MagicMock is from unittest which comes with built-in python
    mock_a = mock.MagicMock(return_value={"value": hijack_value})
    a.do_something = mock_a

    # do something with value X
    result = a.do_something(input_value)

    # Then we can see that mock_a has been called once
    mock_a.assert_called_once_with(input_value)

    # the result should be overridden to whatever was hijacked to be return
    assert result["value"] == hijack_value


# 2) How to mock a function with a context manager
def test_mock_function_return():

    # Instead of displacing the function, we can patch the object and save the reference for us to assert on later
    with mock.patch.object(A, "do_something", return_value={"value": hijack_value}) as mock_a:

        a = A()
        result = a.do_something(input_value)

    # Then we can see that mock_a has been called once
    mock_a.assert_called_once_with(input_value)

    # And assert that the value has been overridden
    assert result["value"] == hijack_value

    # When we then call the function again outside the context
    result2 = a.do_something(input_value)

    # And assert that the value has been restored to normal
    assert result2["value"] == input_value


# 3) How to mock a function with a context manager
@mock.patch.object(A, "do_something", lambda a,b:{"value": hijack_value})
def test_mock_function_return():

    a = A()
    result = a.do_something(input_value)

    # And assert that the value has been overridden
    assert result["value"] == hijack_value


# 3) Using pytest mock
# Inject a mocker fixture into the test
# NB: mocker is a unchangeable magical keyword recognised by pytest_mock
def test_pytest_mock_function_return(mocker: pytest_mock.MockFixture):

    # We will patch the A class
    # note that we need to specify the path to the function from the source
    # In this particular case, it happens to also be where it is called (we will explain further in lesson 2)
    mock_do_something = mocker.patch("lesson01_mocks.test_function_mock.A.do_something")

    # We will make the displacing object return the hijack value when it is called
    mock_do_something.return_value = {"value": hijack_value}

    # Let's call the method
    a = A()
    result = a.do_something(input_value)

    # Then we can see that mock_a has been called once
    mock_do_something.assert_called_once_with(input_value)

    # And assert that the value has been overridden
    assert result["value"] == hijack_value


# We can further improve the command with the return value inline
def test_pytest_mock_function_return_improver(mocker: pytest_mock.MockFixture):

    # We will patch the A class
    mock_do_something = mocker.patch(
        "lesson01_mocks.test_function_mock.A.do_something",
        return_value={"value": hijack_value},
    )

    # Let's call the class method
    a = A()
    result = a.do_something(input_value)

    # Then we can see that mock_a has been called once
    mock_do_something.assert_called_once_with(input_value)

    # And assert that the value has been overridden
    assert result["value"] == hijack_value
