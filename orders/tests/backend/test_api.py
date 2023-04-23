import pytest
from rest_framework.test import APIClient

from backend.models import User, Product, Shop, Category


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_api(client):
    user_count = User.objects.count()

    response = client.post(f'/api/v1/user/register',
                           data={"first_name": "test", "last_name": "test",
                                 "email": "sidorenko@uralweb.ru", "password": "test_password",
                                 "company": "test", "position": "test"
                                 }
                           )
    data = response.json()
    assert response.status_code == 200
    assert User.objects.count() == user_count + 1

    user = User.objects.get(email='sidorenko@uralweb.ru')
    user.is_active = True
    user.type = 'shop'
    user.save()

    assert User.objects.all()[0].is_active == True

    response = client.post(f'/api/v1/user/login',
                           data={'email': "sidorenko@uralweb.ru",
                                 'password': "test_password"
                                 }
                           )
    data = response.json()

    assert response.status_code == 200
    assert data['Status'] == True
    token = data['Token']

    count_shop = Shop.objects.count()
    count_products = Product.objects.count()
    
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    response = client.post(f'/api/v1/partner/update',
                           data={'url': "https://www.helpanimals.ru/shop1.yaml"}
                           )
    assert response.status_code == 200
    assert Shop.objects.count() == count_shop + 1
    assert Product.objects.count() == count_products + 4

    response = client.get(f'/api/v1/categories')
    data = response.json()
    assert response.status_code == 200
    assert len(data['results']) == Category.objects.count()

    response = client.get(f'/api/v1/product/3')
    assert response.status_code == 200
    