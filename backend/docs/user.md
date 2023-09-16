# User Management in fast-commerce

The "User" section of the application is responsible for managing user accounts, including retrieve and update operations.

**Table of Contents**
- [Introduction](#introduction)
- [User Model](#user-model)
- [Repository](#repository)
- [UserRepository](#userrepository)
  - [Create User](#create-user)
  - [Update User](#update-user)
  - [Retrieve User](#retrieve-user)
- [Controller](#controller)
    - [UserController](#usercontroller)
- [Exceptions](#exceptions)
    - [UserAlreadyExistError](#useralreadyexisterror)
- [API Routes](#api-routes)
    - [GET /users/{user_uuid}](#get-usersuser_uuid)
    - [PUT /users/{user_uuid}](#put-usersuser_uuid)
- [Conclusion](#conclusion)

## Introduction

The "User" section of the application focuses on user account management.
It allows users to retrieve other users' information and update their own information.

## User Model

The `User` model represents the user entity and includes the following fields:

- `id` (int) - A unique identifier for the user.
- `uuid` (UUID) - A universally unique identifier for the user.
- `email` (str) - The user's email address (unique).
- `first_name` (str) - The user's first name.
- `last_name` (str, optional) - The user's last name.
- `is_admin` (bool) - A flag indicating whether the user has administrator privileges.
- `date_joined` (datetime) - The date and time when the user account was created.
- `password` (str) - A hashed version of the user's password.

## Repository

### UserRepository

The `UserRepository` class, which inherits from `BaseRepository`, is responsible for user-related database operations, including creating, updating, and retrieving user information.

#### Create User

- **Description**: This method creates a new user in the database, hashing their password before storage.
- **Parameters**: User registration data.
- **Steps**:
    1. Check if a user with the given email already exists in the database. If found, raise a `UserAlreadyExistError`.
    2. Hash the user's password for secure storage.
    3. Create a new user record in the database.
- **Returns**: The newly created user.

#### Update User

- **Description**: This method updates user information, including password hashing if changed.
- **Parameters**: User data for updating.
- **Steps**:
    1. Check if the password has changed and re-hash it if necessary.
    2. Update the user's information in the database.
- **Returns**: The updated user.

#### Retrieve User

- **Description**: This method retrieves a user's information by their UUID.
- **Parameters**: User UUID.
- **Returns**: The user's information.

## Controller

### UserController

The `UserController` class, which inherits from `BaseController`, provides access to user-related methods.

## Exceptions

### UserAlreadyExistError

- **Description**: This exception is raised when a user with the given email already exists in the database.

## API Routes

### GET /users/{user_uuid}

- **Description**: Retrieve a user's information by their UUID.
- **Method**: GET
- **Status Code**: 200 OK

### PUT /users/{user_uuid}

- **Description**: Update a user's information by their UUID (for the user themselves).
- **Method**: PUT
- **Status Code**: 200 OK

## Conclusion

The "User" section of the application is responsible for managing user accounts, including retrieve and update operations.