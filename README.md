# REST API JOOBA.AI Demo 
## Firebase Product Management

This project is a Flask-based API that integrates with Firebase Authentication and Realtime Database to manage user registration, login, and product-related functionalities. It allows users to upload, view, update, delete, and search for products in the database. Authentication is handled via Firebase and requires users to be authorized before performing certain actions.

## Features

- **User Registration:** Users can register by providing an email and password.
- **User Login:** Users can log in using their email and password, which returns a Firebase token.
- **Upload Product:** Authenticated users can upload product details (name, description, category, price).
- **View User Products:** Authenticated users can view their own uploaded products.
- **Delete Product:** Authenticated users can delete their own products.
- **Update Product:** Authenticated users can update the details of their products.
- **Search Products:** Allows searching for products by name.
- **View Products by Category:** Users can filter products by category.
- **View Product Details:** Allows viewing detailed information about a specific product.
- **View All Products:** Displays all products in the database.

## Prerequisites
- Python 3.x installed

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

### User Authentication

- **Register User:**  
  `POST /register`  
  Registers a new user with email and password.

  **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- **Login User:**  
  `POST /login`  
  Logs in a user and returns a Firebase token.

  **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### Product Management

- **Upload Product:**  
  `POST /upload_product`  
  Uploads a product for the authenticated user. Requires a Firebase token in the `Authorization` header.

  **Request Body:**
  ```json
  {
    "name": "Product Name",
    "description": "Product Description",
    "category": "Product Category",
    "price": 100
  }
  ```

- **View User Products:**  
  `GET /user_products`  
  Retrieves all products uploaded by the authenticated user.

- **Delete Product:**  
  `DELETE /delete_product/<product_id>`  
  Deletes a product by its ID. Only the user who uploaded the product can delete it.

- **Update Product:**  
  `PUT /update_product/<product_id>`  
  Updates a product by its ID. Only the user who uploaded the product can update it.

- **Search Products:**  
  `GET /search_products?query=<search_query>`  
  Searches for products by their name.

- **View Products by Category:**  
  `GET /products_by_category/<category_name>`  
  Retrieves products by category.

- **View All Products:**  
  `GET /all_products`  
  Retrieves all products in the database.

- **View Product Info:**  
  `GET /product_info/<product_id>`  
  Retrieves detailed information about a specific product.

## Environment Variables

This project uses the following environment variables stored in a `.env` file:

- `FIREBASE_WEB_API_KEY`: The Firebase Web API key for authentication.

## Running the Application

To run the application locally, use the following command:

```bash
python main.py
```

By default, the app runs in `debug` mode.
