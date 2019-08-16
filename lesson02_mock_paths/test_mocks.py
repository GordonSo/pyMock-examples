from lesson02_mock_paths.outter_handler import hander


# Here is an example of pytest mock patch path
# Notice the path of the object being patch is an absolute path to the object
# When you are trying to patch a third party library, this can be difficult to work out;
# One way would be to use an IDE to debug into the line of code using F8 (Step over) or F7 (Step into)
# once you are in the function of the object, the IDE will show you the path of the object in the navigation bar
def test_a_creation(mocker):

    subAMock = mocker.patch('a.subA.do_a_shit')
    subAMock.return_value = {"value": 321}

    result = hander()
    assert result["value"] == 321
