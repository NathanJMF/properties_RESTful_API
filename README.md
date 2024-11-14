# ZD Tech Task - Property Management API

# Prerequisites
- Docker
- Python 3.12
- Pipenv

# Project Setup
1. Clone the repository
    ```
    git clone https://github.com/NathanJMF/ZDTechTask.git
    cd ZDTechTask
    ```
2. Create a ```.env``` file in the root of the project directory with the following structure
    ```
    GLOBAL_TEST_FLAG=true
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    ```
3. Ensure you have the Docker Engine open and start the database
    ```
    # Start the PostgreSQL database
    docker-compose up -d
    ```
4. Set up your virtual environment using pipenv
    ```
    pipenv shell
    pipenv sync
    ```
5. Set up the structure of the database by running the script ```_script_initial_database_setup.py``` 
    ```
    python _script_initial_database_setup.py
    ```
6. Start the API
    ```
    python app.py
    ```

7. *(optional)* Populate the database with dummy data by running the script ```_script_generate_dummy_data.py``` 
    ```
    python _script_generate_dummy_data.py
    ```

The API will be available at http://127.0.0.1:5000.


# API Endpoints
- Get All Property Details
    - GET ```/api/properties```
    - Note: Currently, there is no pagination logic implemented
- Get Single Property Details
    - GET ```/api/properties/<property_id>```
- Create New Property
    - POST ```/api/properties```
    ```
    Create New Property JSON Body:
    {
      "address": "123 Main St",
      "postcode": "ZIP123",
      "city": "Cityville",
      "num_rooms": 3,
      "created_by": 1
    }
    ```
- Delete Property
    - DELETE ```/api/properties/<property_id>```

    ```
    Delete Property Header: 
    User_Id: <user_id>  // User ID of the user making the request
    ```
  
# Running Tests
The unit tests can be run using the following command:

```python -m pytest```

# System Overview
### config_loader.py
Loads and manages environment-specific configurations using a .env file, 
including database credentials and application flags.

### app.py
Initializes and runs the Flask application, setting up primary API routes for property management.

### app_resources.py
Defines the main API resource ```Property``` with methods for creating, retrieving, and deleting properties.

### app_request_parsers.py
Parses and validates incoming ```POST``` requests to ensure data completeness and type correctness.

### helpers.query_helpers.py
Provides reusable query functions for interacting with the property database, streamlining CRUD operations.

### tests.test_api.py
Contains unit tests for API endpoints, ensuring functionality and error handling are correct using ```pytest```.

## Database System:
### core.py
Manages core database operations, including connections, queries, and data insertion/deletion.

### structure.py
Defines the database schema and table structures.

### setup.py
Automates the creation of required schemas and tables on initial setup.

## Dummy Data Factory:
Generates dummy data for ```users``` and ```properties``` using Faker for testing and development purposes.

## Scripts:
### _script_initial_database_setup.py
Sets up the database schema and tables.

### _script_generate_dummy_data.py
Populates the database with dummy data for testing and development.