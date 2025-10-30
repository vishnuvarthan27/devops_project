import sys, os
import pytest

# ensure repo root (where app.py is) is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, bookings


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        # clear bookings before each test
        bookings.clear()
        yield c

def test_index_get(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Welcome to Smart Bus Ticket Booking System" in resp.data

def test_booking_post(client):
    # initial no bookings
    assert bookings == []
    resp = client.post('/', data={'name': 'Test User', 'bus_id': '1', 'seats': '2'}, follow_redirects=True)
    assert resp.status_code == 200
    assert len(bookings) == 1
    assert bookings[0]['name'] == 'Test User'
    assert bookings[0]['seats'] == 2
    assert bookings[0]['total'] == 2 * 550
