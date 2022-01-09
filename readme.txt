#Clone git repository
# Docker Up and running
docker-compose up --build
# Access API to make sure it is working
http://localhost:8000/products/search
# Add Product
http://localhost:8000/product/add
# Json input
{
  "posts": [
    {
      "name": "abc",
      "price": 10000,
      "start_date": "06/01/2021"
    },
    {
      "name": "abd",
      "price": 20000,
      "start_date": "05/01/2021"
    }
  ]
}

# Response: Bad request
# Valid Input
{
  "posts": [
    {
      "name": "abc",
      "price": 10000,
      "start_date": "06/01/2022"
    },
    {
      "name": "abd",
      "price": 20000,
      "start_date": "05/01/2022"
    }
  ]
}

# view all added products
http://localhost:8000/products/list
# Search for products added
http://localhost:8000/products/search?keyword=abc&start_date=02/01/2021
#expect a json response with added product

