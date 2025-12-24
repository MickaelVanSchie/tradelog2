import datetime
from uuid import UUID

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


@pytest.fixture
def test_position() -> Position:
    pos = Position(
        id=UUID("7c0ca90e-6359-4b62-9117-bfd24548505c"),
        pair_id=UUID('4f2eaaf3-4cd7-4b1f-a0e5-2328f6f0689d'),
        type="long",
        entry=100,
        stop_loss=90,
        take_profit=110,
        exit_price=None,
        position_size=1,
        opening_reason="manual",
        created=datetime.now(),
        updated=datetime.now(),
        status="open"
    )

    return pos