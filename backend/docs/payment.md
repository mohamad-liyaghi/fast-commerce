# Payment Management in fast-commerce

The "Payment" section of the application is responsible for managing payments made by users for their orders. This section ensures a seamless and secure payment process for orders.

**Table of Contents**
- [Introduction](#introduction)
- [Model: Payment](#model-payment)
- [Repository](#repository)
- [Controller](#controller)
- [API Routes](#api-routes)
  - [POST /payment/{order_uuid}](#post-paymentorder_uuid)
  - [GET /payments/](#get-payments)
  - [GET /payments/{payment_uuid}](#get-paymentspayment_uuid)
- [Conclusion](#conclusion)

## Introduction

The "Payment" section of the application is crucial for processing and recording payments for customer orders. It allows users to pay for their orders, records payment details, and updates the order status accordingly.

## Model: Payment

The `Payment` model represents a payment entity and includes the following fields:

- `id` (int) - A unique identifier for the payment.
- `uuid` (UUID) - A universally unique identifier for the payment.
- `created_at` (datetime) - The date and time when the payment was created.
- `amount` (int) - The amount of the payment.
- `user_id` (int) - The ID of the user who made the payment.
- `order_id` (int) - The ID of the order for which the payment is made.

## Repository

### PaymentRepository

The `PaymentRepository` class, which inherits from `BaseRepository`, is responsible for payment-related database operations, including creating and retrieving payments.

## Controller

### PaymentController

The `PaymentController` class, which inherits from `BaseController`, provides access to payment-related methods.

### pay_order

- **Description**: This method handles the payment of an order. It creates a payment record, associates it with the user and order, and updates the order status to "PREPARING."
- **Parameters**: Request user, order UUID, and order controller.
- **Steps**:
    1. Retrieve the order based on the order UUID and the user making the payment.
    2. Create a payment record with the user, order, and the order's total price.
    3. Update the order status to "PREPARING."
- **Returns**: The payment record.

## API Routes

### POST /payment/{order_uuid}

- **Description**: Process a payment for a specific order.
- **Method**: POST
- **Status Code**: 200 OK

### GET /payments/

- **Description**: Retrieve a list of payment records for the current user.
- **Method**: GET
- **Status Code**: 200 OK

### GET /payments/{payment_uuid}

- **Description**: Retrieve details of a specific payment record for the current user.
- **Method**: GET
- **Status Code**: 200 OK

## Conclusion

The "Payment" section of the application streamlines the payment process for customer orders. It ensures that payments are securely processed, recorded, and associated with the corresponding orders. Users can view their payment history, and orders are updated to the "PREPARING" status upon successful payment. This functionality enhances the overall order management and payment experience in the fast-commerce application.