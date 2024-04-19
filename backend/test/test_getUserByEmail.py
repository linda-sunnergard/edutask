import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def basic_sut():
    mockedDAO = mock.MagicMock()
    mockedSUT = UserController( dao = mockedDAO )
    return mockedSUT

@pytest.fixture
def success_sut(user: list):
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = user
    mockedSUT = UserController( dao = mockedDAO )
    return mockedSUT

@pytest.fixture
def error_sut():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.side_effect = Exception
    mockedSUT = UserController( dao = mockedDAO )
    return mockedSUT

@pytest.mark.unit
@pytest.mark.parametrize('user, expected', 
                         [([{'name': 'John'}], {'name': 'John'}), 
                          ([{'name': 'John'}, {'name': 'Jane'}], {'name': 'John'}), 
                          ([], None)])
def test_getUserByEmail_NoneOneMultipleObjReturn(success_sut, expected):
    result = success_sut.get_user_by_email(email='test@test')
    assert result == expected

@pytest.mark.unit
def test_getUserByEmail_invalidEmail(basic_sut):
    with pytest.raises(ValueError):
        basic_sut.get_user_by_email(email='invalidEmail')

@pytest.mark.unit
@pytest.mark.parametrize('user', [([{'name': 'John'}])])
def test_getUserByEmail_validEmail(success_sut):
    try:
        success_sut.get_user_by_email(email='valid@email')
        success_sut.dao.find.assert_called_once()

    except ValueError as error:
        raise AssertionError(f"Raised exception {error} when it should not.")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")

@pytest.mark.unit
def test_getUserByEmail_failDAO(error_sut):
    with pytest.raises(Exception):
        error_sut.get_user_by_email('test@test')


@pytest.mark.unit
@pytest.mark.parametrize('user', [([{'name': 'John'}])])
def test_getUserByEmail_successDAO(success_sut):
    try:
        success_sut.get_user_by_email(email='test@test')
        success_sut.dao.find.assert_called_once()

    except Exception as error:
        raise AssertionError(f"Raised exception {error} when it should not.")

@pytest.mark.unit
@pytest.mark.parametrize('user', [([{'name': 'John'}, {'name': 'Jane'}])])
def test_getUserByEmail_warningLog(success_sut, capsys):
    email="test@test"
    warning_log = "Error: more than one user found with mail " + email + "\n"
    success_sut.get_user_by_email(email)

    captured = capsys.readouterr()
    assert captured.out == warning_log

@pytest.mark.unit
@pytest.mark.parametrize('user', [[{'name': 'John'}]])
def test_getUserByEmail_noWarningLog(success_sut, capsys):
    success_sut.get_user_by_email(email='test@test')

    captured = capsys.readouterr()
    assert len(captured.out) == 0