import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.controllers.taskcontroller import TaskController

@pytest.fixture
def mock_populate_task():
    taskAfter = [{'title': 'TestTask', 'description': 'TestDescription', 'video': 'www.url.com', 'todos': 'Watch'}]
    return taskAfter

# @pytest.fixture
# def basic_sut():
#     mockedTasksDao = mock.MagicMock()
#     mockedVideosDao = mock.MagicMock()
#     mockedTodosDao = mock.MagicMock()
#     mockedUsersDao = mock.MagicMock()
#     mockedSUT = TaskController(mockedTasksDao, mockedVideosDao, mockedTodosDao, mockedUsersDao)
#     return mockedSUT

@pytest.fixture
def success_sut(task, mock_populate_task):
        mockedTasksDao = mock.MagicMock()
        mockedVideosDao = mock.MagicMock()
        mockedTodosDao = mock.MagicMock()
        mockedUsersDao = mock.MagicMock()
        mockedTasksDao.find.return_value = task

        with patch('src.controllers.taskcontroller.TaskController.populate_task') as mockPopulateTask:
            mockPopulateTask.return_value = mock_populate_task
            mockedSUT = TaskController(mockedTasksDao, mockedVideosDao, mockedTodosDao, mockedUsersDao)
            return mockedSUT

# @pytest.fixture
# def error_sut():
#     mockedTasksDao = mock.MagicMock()
#     mockedVideosDao = mock.MagicMock()
#     mockedTodosDao = mock.MagicMock()
#     mockedUsersDao = mock.MagicMock()
#     mockedTasksDao.find.side_effect = Exception
#     mockedSUT = TaskController(mockedTasksDao, mockedVideosDao, mockedTodosDao, mockedUsersDao)
#     return mockedSUT

@pytest.mark.examPrep
@pytest.mark.parametrize('task, expected',
                         [([{'title': 'TestTask', 'description': 'TestDescription', 'video': '234', 'todos': ['345', '456']}], 
                           [{'title': 'TestTask', 'description': 'TestDescription', 'video': 'www.url.com', 'todos': 'Watch'}])]
                         )
def test_getTasksOfUser_allOK(success_sut, expected):
    result = success_sut.get_tasks_of_user(id='123')
    assert result == expected