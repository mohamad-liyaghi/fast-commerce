# Product Management in fast-commerce

The "Product" section of the application is responsible for managing product listings, including creation, retrieval, update, and deletion.

**Table of Contents**
- [Introduction](#introduction)
- [Model: Product](#model-product)
- [Repository](#repository)
- [ProductRepository](#productrepository)
  - [Create Product](#create-product)
  - [Update Product](#update-product)
  - [Delete Product](#delete-product)
  - [Retrieve or Search Products](#retrieve-or-search-products)
- [Controller](#controller)
    - [ProductController](#productcontroller)
- [Exceptions](#exceptions)
    - [ProductOwnerRequired](#productownerrequired)
    - [AcceptedVendorRequired](#acceptedvendorrequired)
- [API Routes](#api-routes)
    - [POST /products/](#post-products)
    - [GET /products/](#get-products)
    - [GET /products/{product_uuid}](#get-productsproduct_uuid)
    - [PUT /products/{product_uuid}](#put-productsproduct_uuid)
    - [DELETE /products/{product_uuid}](#delete-productsproduct_uuid)
- [Conclusion](#conclusion)

## Introduction

The "Product" section of the application focuses on managing product listings. It allows vendors to create, retrieve, update, and delete products.

## Model: Product

The `Product` model represents a product entity and includes the following fields:

- `id` (int) - A unique identifier for the product.
- `uuid` (UUID) - A universally unique identifier for the product.
- `title` (str) - The title of the product.
- `description` (str) - A description of the product.
- `price` (int) - The price of the product.
- `specs` (JSON) - Product specifications.
- `created_at` (datetime) - The date and time when the product listing was created.

## Repository

### ProductRepository

The `ProductRepository` class, which inherits from `BaseRepository`, is responsible for product-related database operations, including creating, updating, deleting, retrieving, and searching for products.

#### Create Product

- **Description**: This method creates a new product in the database.
- **Parameters**: Product data.
- **Steps**:
    1. Check if the vendor is an accepted vendor. If not, raise an `AcceptedVendorRequired` exception.
    2. Create a new product record in the database.
- **Returns**: The newly created product.

#### Update Product

- **Description**: This method updates a product's information.
- **Parameters**: Product UUID and data for updating.
- **Steps**:
    1. Check if the request user is the owner of the product. If not, raise a `ProductOwnerRequired` exception.
    2. Update the product's information in the database.
- **Returns**: The updated product.

#### Delete Product

- **Description**: This method deletes a product.
- **Parameters**: Product UUID.
- **Steps**:
    1. Check if the request user is the owner of the product. If not, raise a `ProductOwnerRequired` exception.
    2. Delete the product record from the database.
- **Returns**: None.

#### Retrieve or Search Products

- **Description**: This method retrieves a list of products or searches for products by title.
- **Parameters**: Optional title filter and other search parameters.
- **Returns**: A list of products.

## Controller

### ProductController

The `ProductController` class, which inherits from `BaseController`, provides access to product-related methods.

## Exceptions

### ProductOwnerRequired

- **Description**: This exception is raised when a user tries to perform an action on a product they do not own.

### AcceptedVendorRequired

- **Description**: This exception is raised when a non-accepted vendor attempts to create a product.

## API Routes

### POST /products/

- **Description**: Create a new product.
- **Method**: POST
- **Status Code**: 201 Created

### GET /products/

- **Description**: Get a list of products.
- **Method**: GET
- **Status Code**: 200 OK

### GET /products/{product_uuid}

- **Description**: Retrieve a product by its UUID.
- **Method**: GET
- **Status Code**: 200 OK

### PUT /products/{product_uuid}

- **Description**: Update a product by its UUID.
- **Method**: PUT
- **Status Code**: 200 OK

### DELETE /products/{product_uuid}

- **Description**: Delete a product by its UUID.
- **Method**: DELETE
- **Status Code**: 204 No Content

## Conclusion

The "Product" section of the application is responsible for managing product listings, including creation, retrieval, update, and deletion. It ensures that only accepted vendors can create products and that product owners can perform actions on their own products.