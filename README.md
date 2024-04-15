# Fast Commerce

## Table of Contents
1. [Introduction](#introduction)
2. [Scenario](#scenario)
3. [Backend](#backend)
4. [Frontend](#frontend)
5. [How to Run With Docker](#how-to-run)
6. [How to Run With Kubernetes](#how-to-run-with-kubernetes)
7. [How to Run Tests](#how-to-run-tests)

## Introduction
Fast Commerce is a comprehensive e-commerce system designed for exceptional performance, extensibility, and maintainability. This repository houses both the backend and frontend components of the system, offering a complete solution for online shopping.
It uses Fastapi as the backend framework and React as the frontend framework.

## Scenario
> FastPicture a thriving e-commerce ecosystem where tech giants like Apple and Microsoft have joined forces with Fast Commerce. Aspiring company owners embark on their journey by registering as users, gaining the opportunity to become recognized vendors upon approval. These vendors seamlessly introduce their world-class products to our platform. When a user places an order, vendors take charge of delivering the items to our central hub. Fast Commerce acts as the catalyst, orchestrating the entire order fulfillment process, ensuring prompt delivery to end-users. This collaborative synergy empowers businesses to effortlessly expand their reach, while customers relish unhindered access to premium products.

## Backend
The **backend** of Fast Commerce is a robust system organized into several key components, each responsible for specific functionalities:

- **Authentication (Auth):** Manages user registration, verification, and login.
- **User Management (User):** Handles user profile retrieval and updates.
- **Vendor Management (Vendor):** Allows users to enroll as vendors and add products.
- **Product Management (Products):** After vendor approval, users can add and manage products.
- **Order Management (Order):** Enables users to create orders and manage their status.
- **Payment Processing (Payment):** Handles payments for orders.

The backend leverages cutting-edge technologies like Docker, Alembic, SQLAlchemy, Celery, and Redis to provide a solid foundation for the e-commerce platform.

For detailed documentation on the backend components and how to set up and run the backend system, please refer to the [Backend README](backend/README.md).

## Frontend

> The Frontend Is Not Yet Available. We regret any inconvenience this may cause. If you are interested in contributing to the development of the frontend, please feel free to reach out.
Please refer to the [Frontend README](frontend/README.md) for more information.

## How to Run With Docker
To get Fast Commerce up and running on your local environment, follow these steps:

1. **Clone the Repository:** `git clone https://github.com/mohamad-liyaghi/fast-commerce.git`
2. **Cd into the Backend Directory:** `cd fast-commerce/`
3. **Build the Backend Docker Image:** `Make build`
4. **Run the Backend Docker Container:** `Make run`

**You can run tests by running `Make test`.**


You can now access the backend server at `http://localhost:8000/`.

## How to Run With Kubernetes
To run Fast Commerce backend with Kubernetes, follow these steps:

1. **Install Minikube:** Follow the instructions [here](https://minikube.sigs.k8s.io/docs/start/).
2. **Start Minikube:** `minikube start`
3. **Clone the Repository:** `git clone https://github.com/mohamad-liyaghi/fast-commerce.git`
4. **Cd into the Backend Directory:** `cd fast-commerce/`
5. **Create a Confmap:** `make confmap`
6. **Run the Kubernetes Deployment:** `kubectl apply -f kubernetes/`
7. **Get external ip from minikube:** `minikube service backend`


## How to Run Tests
The backend of Fast Commerce is equipped with a comprehensive test suite to ensure its reliability and robustness.
<br>

To run tests, you can run the following command on the backend directory:
```bash
make test
```

If you are running the project with kubernetes, you can run tests by running the following command:
```bash
  make test_k8s
```

