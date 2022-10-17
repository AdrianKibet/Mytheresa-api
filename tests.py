import json
from app import app

# tests for results expected under given constraints
def test_category_filter():
    response = app.test_client().get('/product?category=sandals')
    res = json.loads(response.data.decode('utf-8'))[0]
    assert type(res) is dict
    assert res['category'] == 'sandals'
    assert response.status_code == 200

def test_price_filter():
    response = app.test_client().get('/product?priceLessThan=75000')
    res = json.loads(response.data.decode('utf-8'))[0]
    assert type(res) is dict
    assert res['name'] == 'Ashlington leather ankle boots'
    assert response.status_code == 200

def test_max_results():
    response = app.test_client().get('/product')
    res = json.loads(response.data.decode('utf-8'))
    assert len(res) == 5
    assert type(res[0]) is dict
    assert response.status_code == 200
