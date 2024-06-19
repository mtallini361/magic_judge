import neo4j
import pytest
from unittest.mock import Mock

class MockSession:
    def __init__(self):
        pass

    def __enter__(self):
        print("Entering mock session")

    def __exit__(self):
        print("Exiting mock session")


@pytest.fixture
def mock_driver(mocker):
    mock = Mock(spec=neo4j.GraphDatabase.driver(uri="neo4j://", auth=("", "")))
    mocker.patch("neo4j.GraphDatabase.driver", return_value=mock)
    mock.session.return_value = MockSession()
    return mock