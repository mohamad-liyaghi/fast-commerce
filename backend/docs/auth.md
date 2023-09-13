# Authentication in fast-commerce

The "Authentication" section of the application is responsible for user registration, verification, and login.

**Table of Contents**
1. [Introduction](#introduction)
2. [Repository](#repository)
    1. [AuthRepository](#authrepository)
        1. [register_user](#register_user)
        2. [verify_user](#verify_user)
        3. [login_user](#login_user)
3. [Controller](#controller)
    1. [AuthController](#authcontroller)
4. [Exceptions](#exceptions)
    1. [UserAlreadyExistError](#useralreadyexisterror)
    2. [UserPendingVerificationError](#userpendingverificationerror)
    3. [UserNotFoundError](#usernotfounderror)
    4. [InvalidVerificationCodeError](#invalidverificationcodeerror)
    5. [InvalidCredentialsError](#invalidcredentialserror)
5. [API Paths](#api-paths)
    1. [POST /register](#post-register)
    2. [POST /verify](#post-verify)
    3. [POST /login](#post-login)
6. [Conclusion](#conclusion)

## Introduction

The "Authentication" section of the application is responsible for user registration, verification, and login. Users who register are temporarily stored in a cache along with a one-time password (OTP). After receiving the OTP, users must successfully verify themselves before they can log in. The OTP is valid for 2 minutes, after which the user is removed from the cache.

## Repository

### AuthRepository

The `AuthRepository` class inherits from the `users.UserRepository` class to access relevant methods. It provides essential methods for user registration and verification.

#### `register_user`

- **Description**: This method handles user creation in the cache and ensures that the user does not already exist in the database.
- **Parameters**: `data` (dict) - User registration data.
- **Steps**:
  1. Check if a user with the given email exists in the database. If found, raise a `UserAlreadyExistError`.
  2. Check if a cached user with the given email exists. If found, raise a `UserPendingVerificationError`.
  3. Create an OTP (one-time password) and add it to the user's data.
  4. Create a cached user with the data in the cache.
  5. Send a verification email containing the OTP to the user's email address.
- **Returns**: The user registration data.

#### `verify_user`

- **Description**: This method verifies a user using the OTP.
- **Parameters**:
  - `email` (str) - The user's email address.
  - `otp` (int) - The OTP provided by the user for verification.
- **Steps**:
  1. Check if a user with the given email already exists in the database. If found, raise a `UserAlreadyExistError`.
  2. Check if a cached user with the given email exists. If not found, raise a `UserNotFoundError`.
  3. Verify the OTP provided by the user. If the OTP is invalid, raise an `InvalidVerificationCodeError`.
  4. If the OTP is valid, remove it from the cached user's data and create a user record in the database.

#### `login_user`

- **Description**: This method allows a user to log in using their email and password.
- **Parameters**:
  - `email` (str) - The user's email address.
  - `password` (str) - The user's password.
- **Steps**:
  1. Check if a user with the given email exists in the database. If not found, raise a `UserNotFoundError`.
  2. Verify the user's password. If the password is invalid, raise an `InvalidCredentialsError`.
  3. If the password is valid, create an access token for the user.
- **Returns**: A dictionary containing the access token and token type.

## Controller

### AuthController

The `AuthController` class, which inherits from `users.UserController`, interacts with the repository and handles exceptions using `HTTPException` from FastAPI to provide clear error messages to users.

## Exceptions

### UserAlreadyExistError
- **Description**: This exception is raised when a user with the given email already exists in the database.

### UserPendingVerificationError
- **Description**: This exception is raised when a user with the given email already exists in the cache.

### UserNotFoundError
- **Description**: This exception is raised when a user with the given email does not exist in the database.

### InvalidVerificationCodeError
- **Description**: This exception is raised when the OTP provided by the user is invalid.

### InvalidCredentialsError
- **Description**: This exception is raised when the password provided by the user is invalid.

## API Paths

### `POST /register`

- **Description**: Register a new user.
- **Method**: POST
- **Status Code**: 201 Created

### `POST /verify`

- **Description**: Verify a user using their OTP code.
- **Method**: POST
- **Status Code**: 200 OK

### `POST /login`

- **Description**: Log in a user.
- **Method**: POST
- **Status Code**: 200 OK


## Conclusion

The "Authentication" section of the application is responsible for user registration, verification, and login. Users who register are temporarily stored in a cache along with a one-time password (OTP). After receiving the OTP, users must successfully verify themselves before they can log in. The OTP is valid for 2 minutes, after which the user is removed from the cache.
