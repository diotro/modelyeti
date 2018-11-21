import pytest
import yetiserver.dao as DAO

@pytest.fixture
def dao():
    DAO.set_redis_connection_parameters("localhost", 6379, "")
    yield DAO
    rconn = DAO.__redis_conn
    if rconn:
        for key in rconn.keys('*'):
            rconn.delete(key)
    DAO.__redis_conn = None
