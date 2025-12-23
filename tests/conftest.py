import pytest
from models import Position
from models.pair import Pair

from app import create_app


@pytest.fixture
def session(monkeypatch):
    class DummyQuery:
        def __init__(self, result):
            self._result = result

        def order_by(self, *args, **kwargs):
            return self

        def all(self):
            return list(self._result)

    class DummySession:
        def __init__(self):
            self.data = {
                Position: [],
                Pair: []
            }

        def query(self, model):
            return DummyQuery(self.data.get(model, []))

        def add(self, obj):
            return None

        def commit(self):
            return None

    dummy_session = DummySession()

    monkeypatch.setattr('config.database.db', dummy_session)
    monkeypatch.setattr('blueprints.app.db', dummy_session)
    monkeypatch.setattr('blueprints.app.positions.db', dummy_session)

    return dummy_session


@pytest.fixture
def test_client(session):
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client
