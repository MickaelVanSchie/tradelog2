import uuid
from unittest.mock import Mock, patch

import pytest
from flask import url_for

from blueprints.app.positions import store_position
from blueprints.exceptions.position_store import PositionStoreException
from models import Position


@pytest.fixture
def valid_position_data():
    return {
        'entry': '100.0',
        'take_profit': '150.0',
        'stop_loss': '90.0',
        'pair': str(uuid.uuid4()),
        'reason': 'Test reason',
        'size': '1.0'
    }


def test_store_position_success(test_client):
    entry = 100.0
    take_profit = 150.0
    stop_loss = 90.0
    pair = uuid.uuid4()
    reason = "Test reason"
    size = "1.0"

    position = store_position(entry, take_profit, stop_loss, pair, reason, size)
    assert position is not None
    assert position.type == "long"
    assert position.entry == entry
    assert position.take_profit == take_profit
    assert position.stop_loss == stop_loss
    assert position.position_size == float(size)
    assert position.pair_id == pair
    assert position.opening_reason == reason


def test_create_position_success(test_client, valid_position_data):
    response = test_client.post('/create-position', data=valid_position_data)
    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_create_position_invalid_input(test_client):
    invalid_data = {
        'entry': 'invalid',
        'take_profit': '150.0',
        'stop_loss': '90.0',
        'pair': str(uuid.uuid4()),
        'reason': 'Test reason',
        'size': '1.0'
    }
    response = test_client.post('/create-position', data=invalid_data)
    assert response.status_code == 302


def test_create_position_store_exception(test_client, valid_position_data):
    with patch('blueprints.app.positions.store_position', side_effect=PositionStoreException):
        response = test_client.post('/create-position', data=valid_position_data)
        assert response.status_code == 302
