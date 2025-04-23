# Spices Project

The **Spices Project** is a Django REST API that facilitates user registration, authentication, connection management, and notifications. Built with Django REST Framework (DRF), the platform enables users to connect with each other through connection requests and receive notifications about connection request updates through an asynchronous processing system.

## Features

### Registration

- Register users with comprehensive profile information:
  - Full Name
  - Email
  - Contact Number
  - Company Name
  - Address
  - Industry
  - Username
  - Password
- Automatic generation of unique user IDs

### Authentication

- JWT-based authentication system
- Login using username and password
- 15-minute token expiry for enhanced security
- Token refresh mechanism

### Connections

- Search for other users by name, company name, email, or contact number
- Send connection requests to other users
- Accept or reject incoming connection requests
- View connection history and status

### Notifications

- Receive real-time notifications for connection request updates
- Asynchronous notification processing using Celery
- Complete notification management (read, unread, delete)
- CRUD operations for handling notifications

## Technology Stack

- **Backend Framework**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Asynchronous Processing**: Celery
- **Message Broker**: Redis
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## Project Structure

```
spices_project/
├── manage.py
├── spices_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── celery.py
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── connections/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── notifications/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── urls.py
│   ├── views.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## Installation & Setup

### Prerequisites

- Docker and Docker Compose installed on your machine
- Git for cloning the repository
- Postman or similar API testing tool (for testing endpoints)

### Getting Started

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd spices_project //set .env referencing .env.example or convert .env.example to .env file
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   This command starts all required services:

   - Django application server on port 8000
   - PostgreSQL database on port 5432
   - Redis message broker on port 6379
   - Celery worker for asynchronous tasks

3. **Access the application**
   - API base URL: http://localhost:8000/api/
   - Admin interface: http://localhost:8000/admin/ (if enabled)

## API Endpoints

### User Management

#### Register a User

- **Endpoint**: `POST /api/register/`
- **Description**: Creates a new user account
- **Request Body**:
  ```json
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "contact_number": "+1234567890",
    "company_name": "Example Corp",
    "address": "123 Main St, City",
    "industry": "Technology",
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response**: `201 Created` with user details and unique ID

#### User Login

- **Endpoint**: `POST /api/login/`
- **Description**: Authenticates user and returns JWT tokens
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
  ```

### Connection Management

#### Search Users

- **Endpoint**: `GET /api/connections/search/?query=<search_term>`
- **Description**: Search for users by name, company, email, or contact
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with list of matching users

#### Send Connection Request

- **Endpoint**: `POST /api/connections/connect/`
- **Description**: Send a connection request to another user
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "to_user": 2
  }
  ```
- **Response**: `201 Created` with connection request details

#### Respond to Connection Request

- **Endpoint**: `POST /api/connections/respond/<request_id>/`
- **Description**: Accept or reject a connection request
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "status": "A" // "A" for Accept, "R" for Reject
  }
  ```
- **Response**: `200 OK` with updated status

#### List Connection Requests

- **Endpoint**: `GET /api/connections/requests/`
- **Description**: Get list of incoming/outgoing connection requests
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with list of requests

### Notification Management

#### List Notifications

- **Endpoint**: `GET /api/notifications/`
- **Description**: Get all notifications for the authenticated user
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with list of notifications

#### Mark Notification as Read

- **Endpoint**: `POST /api/notifications/<notification_id>/mark_as_read/`
- **Description**: Mark a specific notification as read
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with updated status

#### Delete Notification

- **Endpoint**: `DELETE /api/notifications/<notification_id>/`
- **Description**: Delete a specific notification
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `204 No Content`

## Database Models

### User Model

- Full Name
- Email (unique)
- Contact Number
- Company Name
- Address
- Industry
- Username (unique)
- Password (hashed)
- Unique User ID

### Connection Request Model

- From User (ForeignKey to User)
- To User (ForeignKey to User)
- Status (Pending, Accepted, Rejected)
- Created At
- Updated At
- Unique constraint to prevent duplicate requests

### Notification Model

- Recipient (ForeignKey to User)
- Connection Request (ForeignKey to ConnectionRequest)
- Message
- Created At
- Is Read (Boolean)

## Asynchronous Tasks

The project uses Celery to handle asynchronous tasks:

1. **Connection Request Notifications**:
   - When a connection request is accepted or rejected, a notification is created asynchronously
   - The task is queued in Redis and processed by Celery workers

## Development Guidelines

### Adding New Features

1. Create migrations: `docker-compose exec django python manage.py makemigrations`
2. Apply migrations: `docker-compose exec django python manage.py migrate`
3. Create a superuser: `docker-compose exec django python manage.py createsuperuser`

### Testing

- Run tests: `docker-compose exec django python manage.py test`

### Security Best Practices

- Environment variables for sensitive information
- CORS configuration for API access
- Field-level validation across all models
- JWT token expiration after 15 minutes

## Troubleshooting

### Common Issues

#### Docker Setup

- **Issue**: Services not starting properly
- **Solution**: Check Docker logs: `docker-compose logs <service_name>`

#### Database Connection

- **Issue**: Django can't connect to PostgreSQL
- **Solution**: Ensure database service is running and credentials are correct

#### Celery Tasks

- **Issue**: Notifications not being processed
- **Solution**: Check Celery worker logs: `docker-compose logs celery`
- **Solution**: Verify Redis connection: `docker-compose exec redis redis-cli ping`

## Acknowledgments

- Django REST Framework
- Celery Project
- PostgreSQL
- Redis
