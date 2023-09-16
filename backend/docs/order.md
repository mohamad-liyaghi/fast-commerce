# Order Management in fast-commerce

The "Order" section of the application is responsible for handling customer orders after a vendor has added a new product. Users can place orders for products, and these orders are represented as order items. Each order item is associated with a single order and contains essential information about the recipient.

**Table of Contents**
- [Introduction](#introduction)
- [Model: Order](#model-order)
- [Repository](#repository)
- [OrderRepository](#orderrepository)
  - [Create Order](#create-order)
  - [Set Order as Paid](#set-order-as-paid)
  - [Set Order as Delivering](#set-order-as-delivering)
  - [Set Order as Delivered](#set-order-as-delivered)
- [Controller](#controller)
  - [OrderController](#ordercontroller)
- [Exceptions](#exceptions)
  - [CartEmptyException](#cartemptyexception)
  - [OrderAlreadyPaid](#orderalreadypaid)
  - [OrderInvalidStatus](#orderinvalidstatus)
- [API Routes](#api-routes)
  - [POST /orders/](#post-orders)
  - [GET /orders/](#get-orders)
  - [GET /orders/{order_uuid}](#get-ordersorder_uuid)
  - [PUT /orders/{order_uuid}](#put-ordersorder_uuid)
- [Conclusion](#conclusion)

## Introduction

The "Order" section of the application handles customer orders for products added by vendors. It manages the creation of orders, updating their statuses, and ensuring orders are delivered to customers.

## Model: Order

The `Order` model represents an order entity and includes the following fields:

- `id` (int) - A unique identifier for the order.
- `uuid` (UUID) - A universally unique identifier for the order.
- `delivery_address` (str) - The address where the order will be delivered.
- `total_price` (int) - The total price of the order.
- `created_at` (datetime) - The date and time when the order was created.
- `status` (enum) - The status of the order (e.g., PENDING_PAYMENT, PREPARING, DELIVERING, DELIVERED).
- `user_id` (int) - The ID of the user who placed the order.

## Repository

### OrderRepository

The `OrderRepository` class, which inherits from `BaseRepository`, is responsible for order-related database operations, including creating, updating, deleting, retrieving, and searching for orders.

#### Create Order

- **Description**: This method creates a new order in the database with associated order items.
- **Parameters**: Order data and the user's cart.
- **Steps**:
    1. Check if the cart is empty. If empty, raise a `CartEmptyException`.
    2. Create a new order record in the database with an initial total price of 0.
    3. Create order items based on the cart contents.
    4. Delete the user's cart after creating the order.
    5. Calculate the total price based on order items and update the order with the calculated total price.
- **Returns**: The newly created order.

#### Set Order as Paid

- **Description**: This method sets the status of an order to "PREPARING" if the order is in "PENDING_PAYMENT" status.
- **Parameters**: Order entity.
- **Steps**:
    1. Check if the order status is "PENDING_PAYMENT." If not, raise an `OrderAlreadyPaid` exception.
    2. Update the order status to "PREPARING."
- **Returns**: The updated order.

#### Set Order as Delivering

- **Description**: This method sets the status of an order to "DELIVERING" if the order is in "PREPARING" status.
- **Parameters**: Order entity.
- **Steps**:
    1. Check if the order status is "PREPARING." If not, raise an `OrderInvalidStatus` exception.
    2. Update the order status to "DELIVERING."
- **Returns**: The updated order.

#### Set Order as Delivered

- **Description**: This method sets the status of an order to "DELIVERED" if the order is in "DELIVERING" status.
- **Parameters**: Order entity.
- **Steps**:
    1. Check if the order status is "DELIVERING." If not, raise an `OrderInvalidStatus` exception.
    2. Update the order status to "DELIVERED."
- **Returns**: The updated order.

## Controller

### OrderController

The `OrderController` class, which inherits from `BaseController`, provides access to order-related methods.

## Exceptions

### CartEmptyException

- **Description**: This exception is raised when a user tries to create an order with an empty cart.

### OrderAlreadyPaid

- **Description**: This exception is raised when an attempt is made to set an order as paid when it is not in "PENDING_PAYMENT" status.

### OrderInvalidStatus

- **Description**: This exception is raised when an order's status is incompatible with the requested operation.

## API Routes

### POST /orders/

- **Description**: Create a new order with associated order items.
- **Method**: POST
- **Status Code**: 201 Created

### GET /orders/

- **Description**: Get a list of orders for the authenticated user.
- **Method**: GET
- **Status Code**: 200 OK

### GET /orders/{order_uuid}

- **Description**: Retrieve an order by its UUID for the authenticated user.
- **Method**: GET
- **Status Code**: 200 OK

### PUT /orders/{order_uuid}

- **Description**: Update the status of an order by its UUID.
- **Method**: PUT
- **Status Code**: 200 OK

## Conclusion

The "Order" section of the application manages customer orders for products added by vendors. It ensures that orders are created with valid data, tracks their status through the order lifecycle, and allows customers to retrieve order information.