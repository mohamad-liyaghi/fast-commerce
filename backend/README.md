# Fast Commerce [Backend]

## Table of Contents
1. [Introduction](#introduction)
2. [Components](#components)
    - [Authentication (Auth)](#authentication-auth)
    - [User Management (User)](#user-management-user)
    - [Vendor Management (Vendor)](#vendor-management-vendor)
    - [Product Management (Products)](#product-management-products)
    - [Order Management (Order)](#order-management-order)
    - [Payment Processing (Payment)](#payment-processing-payment)

## Introduction
Fast Commerce is a robust e-commerce system built on the FastAPI framework, designed for exceptional performance, extensibility, and maintainability. Leveraging cutting-edge technologies like Docker, Alembic, SQLAlchemy, Celery, and Redis, it offers a comprehensive solution for online shopping.

## Components
Fast Commerce is organized into several key components, each responsible for specific functionalities:

### Authentication (Auth)
The **Authentication** section, manages user registration, verification, and login. When a user registers, their data is temporarily cached, and an OTP is sent for verification. After registration, users have a brief window to verify their account, after which their data is permanently saved in the database. This section ensures secure user management. [**Documentation**](docs/auth.md)

### User Management (User)
The **User** section, deals with retrieving and updating user information. It provides endpoints for users to manage their profiles efficiently. [**Documentation**](docs/user.md)

### Vendor Management (Vendor)
In the **Vendor** section, users can enroll as vendors and add products to the platform. Vendor status starts as 'pending' and is subject to approval by administrators. [**Documentation**](docs/vendor.md)

### Product Management (Products)
After vendor approval, users can add products to the website. This section handles product creation, editing, and listing, providing an extensive range of features for vendors. [**Documentation**](docs/products.md)

### Order Management (Order)
The **Order** section allows users to create orders from the available products. Each product forms an order item, and all order items are grouped into an order, which includes user information, status, and delivery address. [**Documentation**](docs/order.md)

### Payment Processing (Payment)
The **Payment** section is responsible for handling payments for orders. Users must make payments to confirm and proceed with their orders, ensuring a secure and efficient payment process. [**Documentation**](docs/payment.md)

