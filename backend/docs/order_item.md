# OrderItem Management in fast-commerce

The "OrderItem" section of the application focuses on managing individual order items associated with customer orders. Each order item represents a specific product within an order.

**Table of Contents**
- [Introduction](#introduction)
- [Model: OrderItem](#model-orderitem)
- [Enums](#enums)
- [Repository](#repository)
  - [Create Order Items](#create-order-items)
  - [Set Order Item as Delivering](#set-order-item-as-delivering)
  - [Set Order Item as Delivered](#set-order-item-as-delivered)
- [Controller](#controller)
  - [OrderItemController](#orderitemcontroller)
- [API Routes](#api-routes)
  - [GET /orderitems/preparing](#get-orderitemsp_preparing)
  - [GET /orderitems/delivering](#get-orderitemsdelivering)
  - [PUT /orderitems/status/{order_item_uuid}](#put-orderitemsstatusorder_item_uuid)
  - [GET /orderitems/{order_item_uuid}](#get-orderitemsorder_item_uuid)
- [Conclusion](#conclusion)

## Introduction

The "OrderItem" section of the application is responsible for managing individual order items within customer orders. It allows vendors and administrators to track and update the status of order items as they move through the order fulfillment process.

## Model: OrderItem

The `OrderItem` model represents an order item entity and includes the following fields:

- `id` (int) - A unique identifier for the order item.
- `uuid` (UUID) - A universally unique identifier for the order item.
- `quantity` (int) - The quantity of the product in the order item.
- `created_at` (datetime) - The date and time when the order item was created.
- `total_price` (int) - The total price of the order item.
- `status` (enum) - The status of the order item (e.g., PREPARING, DELIVERING, DELIVERED).
- `order_id` (int) - The ID of the order to which the order item belongs.
- `product_id` (int) - The ID of the product associated with the order item.

## Enums

### OrderItemStatusEnum

- `PREPARING` - The order item is being prepared for delivery.
- `DELIVERING` - The order item is in the process of being delivered.
- `DELIVERED` - The order item has been delivered.

## Repository

### OrderItemRepository

The `OrderItemRepository` class, which inherits from `BaseRepository`, is responsible for order item-related database operations, including creating, updating, deleting, retrieving, and searching for order items.

#### Create Order Items

- **Description**: This method bulk creates order items for an order based on the contents of a user's cart.
- **Parameters**: Order entity, user's cart, and a product controller.
- **Steps**:
    1. Retrieve product data based on product UUIDs from the cart.
    2. Create a dictionary with product UUIDs and quantities.
    3. Bulk insert the order items associated with the order.
- **Returns**: A list of newly created order items.

#### Set Order Item as Delivering

- **Description**: This method sets the status of an order item to "DELIVERING," but only if the request user is the vendor who owns the product associated with the order item.
- **Parameters**: Order item entity and the request user.
- **Steps**:
    1. Check if the request user is the owner of the product. If not, raise a `VendorRequiredException`.
    2. Check if the order item status is "PREPARING." If not, raise an `InappropriateOrderStatus` exception.
    3. Update the order item status to "DELIVERING."
- **Returns**: The updated order item.

#### Set Order Item as Delivered

- **Description**: This method sets the status of an order item to "DELIVERED," but only if the request user is an administrator.
- **Parameters**: Order item entity and the request user.
- **Steps**:
    1. Check if the request user is an administrator. If not, raise an `AdminRequiredException`.
    2. Check if the order item status is "DELIVERING." If not, raise an `InappropriateOrderStatus` exception.
    3. Update the order item status to "DELIVERED."
- **Returns**: The updated order item.

## Controller

### OrderItemController

The `OrderItemController` class, which inherits from `BaseController`, provides access to order item-related methods.

## API Routes

### GET /orderitems/preparing

- **Description**: Retrieve a list of order items that are preparing for delivery for a specific vendor.
- **Method**: GET
- **Status Code**: 200 OK

### GET /orderitems/delivering

- **Description**: Retrieve a list of order items that are currently being delivered.
- **Method**: GET
- **Status Code**: 200 OK

### PUT /orderitems/status/{order_item_uuid}

- **Description**: Update the status of an order item by its UUID.
- **Method**: PUT
- **Status Code**: 200 OK

### GET /orderitems/{order_item_uuid}

- **Description**: Retrieve an order item by its UUID. Only accessible to administrators, the vendor of the product, and the user who placed the order.
- **Method**: GET
- **Status Code**: 200 OK

## Conclusion

The "OrderItem" section of the application allows for the management of individual order items within customer orders. It enables vendors to track and update the status of order items as they progress through the order fulfillment process, and it provides administrators with the ability to mark order items as delivered. This functionality enhances the overall order management process in the fast-commerce application.