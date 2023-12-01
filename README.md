# Дипломная работа «API Сервис заказа товаров для розничных сетей».

**API запросы проекта:**

- POST запрос для регистрации пользователя /user/register
  {
  "username": "Ivan",
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "email": "IvanovI@mail.ru",
  "password": "123456qasw",
  "company": "Company",
  "position": "meneger",
  "type": "shop"
  }
- POST запрос для авторизации пользователя /user/login
  {
  "username": "Ivan",
  "password": "123456qasw"  
  }
-  информации о пользователе /user/details
- POST запрос для изменение информации о пользователе /user/details
  {
  "username": "Ivan",
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "email": "IvanovI@mail.ru",
  "password": "123456qasw",
  "company": "Company",
  "position": "meneger",
  "type": "shop"
  }
- POST запрос для обновления прайса товаров /partner/update
-  товаров /products
- GET запрос для получения информации по конкретному товару /product/1
- GET запрос для получения списка категорий /categories
- GET запрос для получения списка магазинов /shops
- PUT запрос для добавление товара в корзину /basket
  {
  "items": [{"id": 3,
             "quantity": 1,
             "product_info": 3}]
  }
- GET запрос для получения списка товаров в корзине /basket
