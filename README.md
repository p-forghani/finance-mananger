# Finance Manager Application

The **Finance Manager** application is a robust web-based tool designed to help users manage their finances effectively. This project showcases a wide range of technical skills and backend development expertise, utilizing modern web technologies and best practices.

## Features

### User Management
- **User Registration**: Allows new users to create accounts securely.
- **Login & Logout**: Provides secure authentication using Flask's session management.
- **Forgot Password**: Implements email-based password recovery with token validation for enhanced security.

### Expense Management
- **CRUD Operations**: Users can create, read, update, and delete their expenses.
- **Search Functionality**: Implements case-insensitive search to filter expenses by title.
- **Pagination**: Efficiently displays expenses across multiple pages, ensuring scalability for large datasets.

### Email Integration
- **Email Sending**: Configured with SendGrid to send transactional emails (e.g., password recovery).

## Technologies Used

### Backend
- **Flask**: Provides the framework for routing, request handling, and templates.
- **Flask-WTF**: Manages forms and CSRF protection for secure data submission.
- **SQLAlchemy**: Acts as the ORM layer for database interactions.
- **Flask-Migrate**: Handles database migrations with Alembic.

### Frontend
- **Jinja2 Templates**: Dynamically generates HTML pages with Bootstrap for styling.

### Utilities
- **SendGrid**: For transactional email services.
- **URLSafeTimedSerializer**: Securely serializes and deserializes tokens for password recovery.

## Highlights

- **Secure User Authentication**: Implements salted password hashing with Werkzeug.
- **Dynamic Pagination**: Uses SQLAlchemy and Flask's pagination utilities to efficiently handle large datasets.
- **Advanced Querying**: Combines filtering and ordering with SQLAlchemy for search and sorting.
- **Email Tokenization**: Protects sensitive actions with time-sensitive, signed tokens.
- **Custom Error Handling**: Ensures users receive meaningful feedback on issues like invalid tokens or expired sessions.

## Skills Demonstrated

- Proficiency in Python and Flask for backend development.
- Expertise in form handling and validation with Flask-WTF.
- Advanced SQL and ORM knowledge using SQLAlchemy.
- Implementing secure and scalable user authentication systems.
- Integrating third-party services like SendGrid for email functionalities.
- Writing clean, modular, and reusable code using Flask's blueprint structure.
- Handling user sessions, cookies, and CSRF protection.
- Designing user-friendly interfaces with Jinja2 and Bootstrap.
- Managing and version-controlling database schemas with Flask-Migrate.

## Future Scope

- Adding advanced analytics for expense tracking.
- Integration with external APIs for currency conversion.
- Support for exporting data in various formats (CSV, Excel).
- Mobile-friendly responsive design improvements.

This project demonstrates a strong foundation in backend development and an ability to build real-world, full-stack web applications.
