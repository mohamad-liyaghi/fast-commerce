# Vendor Management in fast-commerce

The "Vendor" section of the application is responsible for managing vendors, including registration, updates, and status changes.

**Table of Contents**
- [Introduction](#introduction)
- [Model: Vendor](#model-vendor)
- [Repository](#repository)
    - [VendorRepository](#vendorrepository)
        - [Create Vendor](#create-vendor)
        - [Update Vendor](#update-vendor)
        - [Retrieve Accepted Vendor](#retrieve-accepted-vendor)
- [Controller](#controller)
    - [VendorController](#vendorcontroller)
- [Exceptions](#exceptions)
    - [PendingVendorExistsException](#pendingvendorexistsexception)
    - [AcceptedVendorExistsException](#acceptedvendorexistsexception)
    - [RejectedVendorExistsException](#rejectedvendorexistsexception)
    - [UpdateVendorStatusDenied](#updatevendorstatusdenied)
    - [VendorInformationUpdateDenied](#vendorinformationupdatedenied)
- [Conclusion](#conclusion)

## Introduction

The "Vendor" section of the application focuses on vendor registration, updates, and status changes. 
It enables users to become vendors, and administrators can review and accept vendor requests. <br>
Each user can have one accepted request as well as rejected requests in the last 10 days.

## Model: Vendor

The `Vendor` model represents a vendor entity and includes the following fields:

- `id` (int) - A unique identifier for the vendor.
- `uuid` (UUID) - A universally unique identifier for the vendor.
- `name` (str) - The vendor's name.
- `description` (str) - A brief description of the vendor.
- `created_at` (datetime) - The date and time when the vendor profile was created.
- `reviewed_at` (datetime, nullable) - The date and time when the vendor registration was reviewed (nullable).
- `domain` (str, nullable) - The vendor's domain (nullable).
- `address` (str) - The vendor's address.
- `status` (enum) - The status of the vendor, which can be "pending," "accepted," or "rejected."

## Repository

### VendorRepository

The `VendorRepository` class, which inherits from `BaseRepository`, is responsible for vendor-related database operations, including creating, updating, and retrieving vendor information.

#### Create Vendor

- **Description**: This method creates a new vendor, considering specific rules for user registrations:
    - A user can have only one pending vendor registration.
    - A user can have only one accepted vendor registration.
    - A user can have only one rejected vendor registration in the last 10 days.
- **Parameters**: User requesting vendor registration and vendor data.
- **Returns**: The newly created vendor.

#### Update Vendor

- **Description**: This method updates vendor information or status. Admins can update vendor status, and users can update their vendor information.
- **Parameters**: Vendor UUID, user requesting the update, and data for updating.
- **Returns**: The updated vendor.

#### Retrieve Accepted Vendor

- **Description**: This method retrieves an accepted vendor for a given user.
- **Parameters**: User requesting the retrieval.
- **Returns**: The accepted vendor associated with the user.

## Controller

### VendorController

The `VendorController` class, which inherits from `BaseController`, provides access to vendor-related methods.

## Exceptions

### PendingVendorExistsException

- **Description**: This exception is raised when a user already has a pending vendor registration.

### AcceptedVendorExistsException

- **Description**: This exception is raised when a user already has an accepted vendor registration.

### RejectedVendorExistsException

- **Description**: This exception is raised when a user already has a rejected vendor registration in the last 10 days.

### UpdateVendorStatusDenied

- **Description**: This exception is raised when a user is not allowed to update the vendor's status.

### VendorInformationUpdateDenied

- **Description**: This exception is raised when a user is not allowed to update the vendor's information.

## Conclusion

The "Vendor" section of the application is responsible for managing vendors, including registration, updates, and status changes. It enforces specific rules for vendor registrations and allows administrators to review and accept vendor requests.