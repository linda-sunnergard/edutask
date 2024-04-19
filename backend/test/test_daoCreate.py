import pytest
from unittest.mock import patch
from src.util.dao import DAO
import json

# Instead of having all the relevant data in the parametrization, I have put it in
# variables to hopefully make it more readable.
compliant_data_task = {
    'title': 'Test title', # Unique
    'description': 'Test description'
}

incompliant_data_task = {
    'title': 123,
    'description': ['1', '2', '3']
}

compliant_data_todo = {
    'description': 'Test description', # Unique
    'done': False
    }

incompliant_data_todo = {
    'description': 123,
    'done': False
    }

compliant_data_user = {
    'firstName': 'John',
    'lastName': 'Doe',
    'email': 'john@doe' # Unique
}

incompliant_data_user = {
    'firstName': ['John'],
    'lastName': 1,
    'email': 2
}

compliant_data_video = {
    'url': 'www.testvideo.com'
}

incompliant_data_video = {
    'url': ['www.testvideo.com']
}

no_data = {}

@pytest.fixture
def get_validator(collection_name: str):
    with open(f'./backend/src/static/validators/{collection_name}.json', 'r') as f:
        yield json.load(f)

@pytest.fixture
def sut(collection_name: str, get_validator: dict):
    
    with patch('src.util.dao.getValidator') as mockValidator:
        mockValidator.return_value = get_validator
        dao = DAO (collection_name= collection_name)
        
        yield dao
    
    dao.collection.drop()

@pytest.mark.integration
@pytest.mark.parametrize('collection_name, compliant_data, key, value', 
                         [('task', compliant_data_task, 'title', 'Test title'), 
                          ('todo', compliant_data_todo, 'description', 'Test description'), 
                          ('user', compliant_data_user, 'firstName', 'John'), 
                          ('video', compliant_data_video, 'url', 'www.testvideo.com')])
def test_daoCreate_compliantData(sut, compliant_data, key, value):
    result = sut.create(compliant_data)
    assert (key, value) in result.items()

@pytest.mark.integration
@pytest.mark.parametrize('collection_name, compliant_data', 
                         [('task', compliant_data_task), 
                          ('todo', compliant_data_todo), 
                          ('user', compliant_data_user)])
def test_daoCreate_doubleData(sut, compliant_data):
    sut.create(compliant_data)
    with pytest.raises(Exception):
        sut.create(compliant_data)

@pytest.mark.integration
@pytest.mark.parametrize('collection_name, incompliant_data', 
                         [('task', incompliant_data_task), 
                          ('todo', incompliant_data_todo), 
                          ('user', incompliant_data_user), 
                          ('video', incompliant_data_video)])
def test_daoCreate_inCompliantData(sut, incompliant_data):
    with pytest.raises(Exception):
        sut.create(incompliant_data)

@pytest.mark.integration
@pytest.mark.parametrize('collection_name, no_data', 
                         [('task', no_data), 
                          ('todo', no_data), 
                          ('user', no_data), 
                          ('video', no_data)])
def test_daoCreate_noData(sut, no_data):
    with pytest.raises(Exception):
        sut.create(no_data)

"""
Suggested test cases:
    - Successful Insert
        - Parameterize: 'collection_name, collection_data'
        - Collection data would be huge if you throw it straight in, 
          consider defining variables for each dictionary and pass them in
    - Failed insert (garbage data)
    - Failed insert (empty data)
    - Reapeat insert failure (unique constraint)
"""