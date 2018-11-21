import pytest
import yetiserver.dao as DAO

@pytest.fixture
def dao():
    DAO.set_redis_connection_parameters("localhost", 6379, "")
    yield DAO
    rconn = DAO._get_redis_connection()
    for key in rconn.keys('*'):
        rconn.delete(key)
