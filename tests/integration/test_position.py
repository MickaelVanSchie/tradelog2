import json
from uuid import UUID


def test_create_position_with_form_data(test_client, session, monkeypatch):
    class DummyPosition(dict):
        def __init__(self, **kwargs):
            normalized = {}
            for key, value in kwargs.items():
                normalized[key] = str(value) if isinstance(value, UUID) else value
            super().__init__(normalized)

    monkeypatch.setattr("blueprints.app.positions.Position", DummyPosition)

    pair_id = "4f2eaaf3-4cd7-4b1f-a0e5-2328f6f0689d"
    response = test_client.post("/create-position", data={
        "entry": 10,
        "take_profit": 12.0,
        "stop_loss": 8.0,
        "pair": pair_id,
        "reason": "breakout",
        "size": 2.5,
    })

    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert 'id' in data
    assert data["pair_id"] == pair_id
    assert data["type"] == "long"
    assert data["entry"] == 10.0
    assert data["take_profit"] == 12.0
    assert data["stop_loss"] == 8.0
    assert data["position_size"] == 2.5
    assert data["opening_reason"] == "breakout"
