**Description:**
This project is a Django backend integrated with the Stripe API to facilitate online payment functionality. 
The project includes a product model (Item) and provides an API to obtain a Stripe Session Id for the payment of the selected item. 
Pages for viewing product information and making payments through Stripe Checkout are also implemented.

Launching the application using docker-compose:

> docker-compose up

To access the admin panel:

> docker exec -it pay_market sh
> python3 manage.py createsuperuser

Upon project startup, the database is automatically populated with test data using Faker.

Fill in the .env file with your data, following the example in the .env.example file.

Application Features:
1) Purchase a single item and pay using Stripe.
2) Add items to the cart, from where you can create an order and pay for it through Stripe.
3) The application also includes a basic implementation of Tax and Discount models - based on these data, the total order price is calculated.

