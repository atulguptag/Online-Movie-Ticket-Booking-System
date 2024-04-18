# Online Movie Ticket Booking System

## Introduction

This is an API backend for an online movie ticket booking system. The system allows users to browse available movies, view showtimes, reserve seats, and purchase tickets.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/atulguptag/Online-Movie-Ticket-Booking-System
```

2. Navigate to the project directory:

```bash
cd movie_api
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations to create the database schema:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## API Endpoints

### Movies

- **GET /api/movies/**: Retrieve a list of available movies.
- **GET /api/movies/{movie_id}/**: View details of a specific movie.
- **POST /api/movies/**: Create a new movie.
- **PUT /api/movies/{movie_id}/**: Update details of a specific movie.
- **DELETE /api/movies/{movie_id}/**: Delete a specific movie.

### Theaters

- **GET /api/theaters/**: Retrieve a list of available theaters.
- **GET /api/theaters/{theater_id}/**: View details of a specific theater.
- **POST /api/theaters/**: Create a new theater.
- **PUT /api/theaters/{theater_id}/**: Update details of a specific theater.
- **DELETE /api/theaters/{theater_id}/**: Delete a specific theater.

### Showtimes

- **GET /api/showtimes/**: Retrieve a list of available showtimes.
- **GET /api/showtimes/{showtime_id}/**: View details of a specific showtime.
- **POST /api/showtimes/**: Create a new showtime.
- **PUT /api/showtimes/{showtime_id}/**: Update details of a specific showtime.
- **DELETE /api/showtimes/{showtime_id}/**: Delete a specific showtime.

### Reservations

- **GET /api/reservations/**: Retrieve a list of reservations.
- **GET /api/reservations/{reservation_id}/**: View details of a specific reservation.
- **POST /api/reservations/**: Create a new reservation.
- **PUT /api/reservations/{reservation_id}/**: Update details of a specific reservation.
- **DELETE /api/reservations/{reservation_id}/**: Delete a specific reservation.

## Authentication

The API does not require authentication for accessing movie and theater information. However, authentication may be required for creating reservations and purchasing tickets depending on the system's implementation.

## Testing

1. Run unit tests to ensure the correctness of API endpoints.
2. Test various scenarios including edge cases and error handling.

## Security

1. Authentication mechanisms are implemented to prevent unauthorized access to sensitive endpoints.
2. Authorization mechanisms are implemented to restrict access to certain endpoints based on user roles and permissions.

## Data Persistence

1. The system uses a relational database SQLite to persist movie, theater, showtime, and reservation data.
2. ORM (Object-Relational Mapping) is used for database operations to avoid raw SQL queries.
3. The database schema is designed to efficiently store and retrieve information related to movies, theaters, showtimes, and reservations.

## Contributors

- [Atul Gupta](https://github.com/atulguptag)

## License

This project is licensed under the [MIT License](LICENSE).