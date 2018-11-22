import pytest
import yetiserver.dao as DAO

@pytest.fixture
def dao():
    DAO.set_redis_connection_parameters("localhost", 14321, "")
    # If anything is in the database, don't use it for testing!! Because the tests clear the database after each run,
    # any data in the database probably is not from tests, and therefore shouldn't be wiped.
    if DAO._get_redis_connection().keys('*') != []:
        raise ValueError("unexpected values in Redis server running on port 14321.")
    DAO.__redis_conn = None

    yield DAO

    rconn = DAO.__redis_conn
    if rconn:
        for key in rconn.keys('*'):
            rconn.delete(key)
    DAO.__redis_conn = None
