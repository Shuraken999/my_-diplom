import pytest
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from prompt_toolkit.validation import ValidationError


from inetshop.tasks import new_user_registered
from inetshop.views import RegisterAccount
from django.test import RequestFactory
from inetshop.models import ConfirmEmailToken, User
from inetshop.views import ConfirmAccount
from inetshop.views import AccountDetails
from inetshop.serializers import UserSerializer
@pytest.fixture
def register_account_view():
    return RegisterAccount()


@pytest.mark.django_db
def test_register_account_success(register_account_view, mocker):
    request_data = {
        'username': 'testuser',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'test@example.com',
        'password': 'Test1234',
        'company': 'Test Company',
        'position': 'Manager',
        'type': 'customer'
    }
    mocker.patch('inetshop.views.validate_password')
    mocker.patch('inetshop.views.UserSerializer')
    mocker.patch('inetshop.views.new_user_registered.send')

    response = register_account_view.post(request_data)

    assert response == JsonResponse({'Status': True})


@pytest.mark.django_db
def test_register_account_missing_fields(register_account_view):
    request_data = {
        'username': 'testuser',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'test@example.com',
        'password': 'Test1234',
        'company': 'Test Company',
        'position': 'Manager'
    }

    response = register_account_view.post(request_data)

    assert response == JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


@pytest.mark.django_db
def test_register_account_invalid_password(register_account_view, mocker):
    request_data = {
        'username': 'testuser',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'test@example.com',
        'password': 'weak',
        'company': 'Test Company',
        'position': 'Manager',
        'type': 'customer'
    }
    mocker.patch('inetshop.views.validate_password', side_effect=ValidationError(['This password is too weak.']))

    response = register_account_view.post(request_data)

    assert response == JsonResponse({'Status': False, 'Errors': {'password': ['This password is too weak.']}})


@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def user():
    return User.objects.create(email='test@example.com')

@pytest.fixture
def token(user):
    return ConfirmEmailToken.objects.create(user=user, key='test_token')


@pytest.mark.django_db
def test_confirm_account_success(factory, user, token):
    view = ConfirmAccount.as_view()
    request = factory.post('/confirm-account/', {'email': 'test@example.com', 'token': 'test_token'})
    response = view(request)

    assert response.status_code == 200
    assert response.data == {'Status': True}
    assert User.objects.get(email='test@example.com').is_active


@pytest.mark.django_db
def test_confirm_account_invalid_token(factory, user):
    view = ConfirmAccount.as_view()
    request = factory.post('/confirm-account/', {'email': 'test@example.com', 'token': 'invalid_token'})
    response = view(request)

    assert response.status_code == 200
    assert response.data == {'Status': False, 'Errors': 'Неправильно указан токен или email'}
    assert not User.objects.get(email='test@example.com').is_active


@pytest.mark.django_db
def test_confirm_account_missing_arguments(factory):
    view = ConfirmAccount.as_view()
    request = factory.post('/confirm-account/', {})
    response = view(request)

    assert response.status_code == 200
    assert response.data == {'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}





@pytest.fixture
def authenticated_request(rf, user):
    request = rf.get('/')
    request.user = user
    return request


@pytest.fixture
def unauthenticated_request(rf):
    return rf.get('/')


@pytest.fixture
def account_details_view():
    return AccountDetails.as_view()

@pytest.mark.django_db
def test_get_authenticated(authenticated_request, account_details_view):
    response = account_details_view(authenticated_request)
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.data == {'username': 'testuser', 'email': 'test@example.com'}

@pytest.mark.django_db
def test_get_unauthenticated(unauthenticated_request, account_details_view):
    response = account_details_view(unauthenticated_request)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 403
    assert response.data == {'Status': False, 'Error': 'Требуется вход в аккаунт/Account login required'}

@pytest.mark.django_db
def test_post_authenticated(authenticated_request, account_details_view):
    data = {'first_name': 'John', 'last_name': 'Doe'}
    response = account_details_view(authenticated_request, data=data)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.data == {'Status': True}

@pytest.mark.django_db
def test_post_unauthenticated(unauthenticated_request, account_details_view):
    response = account_details_view(unauthenticated_request)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 403
    assert response.data == {'Status': False, 'Error': 'Log in required'}

@pytest.mark.django_db
def test_post_with_password(authenticated_request, account_details_view):
    data = {'password': 'newpassword'}
    response = account_details_view(authenticated_request, data=data)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.data == {'Status': True}

@pytest.mark.django_db
def test_post_with_invalid_data(authenticated_request, account_details_view):
    data = {'email': 'invalid_email'}
    response = account_details_view(authenticated_request, data=data)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.data == {'Status': False, 'Errors': {'email': ['Enter a valid email address.']}}