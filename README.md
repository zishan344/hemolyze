# Hemolyze - Blood Donation Management System

## Overview

Hemolyze is a Django REST API-based blood donation management system that connects blood donors with recipients. The platform facilitates blood donation requests and manages donor availability efficiently.

## Features

- **User Management**

  - User registration and authentication
  - Profile management with blood group and donation history
  - Donor availability status tracking

- **Blood Donation Features**

  - Create and manage blood donation requests
  - Search available donors by blood group
  - Track donation history
  - Accept/manage blood donation requests

- **Dashboard**
  - View personal donation history (given/received)
  - List available donors with filters
  - Track request status

## API Endpoints

### User Management

- `/api/v1/auth/users/` - User profile management
- `/api/v1/auth/` - Authentication endpoints

### Blood Request Management

- `/api/v1/blood-requests/` - Create and list blood requests
- `/api/v1/blood-requests/<id>/` - Manage specific requests
- `/api/v1/blood-request/<id>/accept-blood-request/` - Handle request acceptance when accept donor for donation

### Dashboard

- `/api/v1/donation-history/` - View donation history
- `/api/v1/donar-list/",` - List available donors

## Technology Stack

- Django REST Framework
- PostgreSQL Database
- JWT Authentication
- Swagger/OpenAPI Documentation
- supabase for database hosting
- vercel for project hosting

## Installation

1. Clone the repository:

```bash
git clone https://github.com/zishan344/hemolyze.git
cd hemolyze
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env
# Edit .env with your database and secret key settings
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Start development server:

```bash
python manage.py runserver
```

## Project Structure

```
hemolyze/
├── api/               # manage all api routes
├── blood_requests/    # Blood request management
├── dashboard/         # Dashboard views
├── hemolyze/          # Project settings
└── user/              # User management app
```

## API Documentation

The API documentation is available at `docs/` and `swagger/` when running the server. It provides detailed information about all endpoints, request/response formats, and authentication requirements.

## Testing

Run the test suite:

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
