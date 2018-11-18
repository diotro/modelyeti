import json

import pytest
from yetiserver import dao as DAO

@pytest.fixture
def dao():
    #DAO.set_redis_connection_parameters()
    yield DAO
    rconn = DAO._get_redis_connection()
    for key in rconn.keys('*'):
        rconn.delete(key)