# Rhombus Assessment

This application was designed to fulfil the requirements of the RhombusAI take-home assessment. It is a web application that processes and presents data. Under the hood, it imports the provided data into a Pandas data frame while performing type inference. Additionally, it offers users the capability to manually override the inferred types.

## Installation

### Docker (Recommended)

To set up the application using Docker, follow these steps:

1. Make sure you have Docker installed on your system.
2. Navigate to the root directory of the project.
3. Run the following command to build and start the containers:
   ```
   docker-compose up --build
   ```
4. Once the containers are up and running, you can access the application at `http://localhost:3000`.

### Manual

To manually set up the application, follow these steps:

#### Backend

1. Navigate to the `backend` directory of the project.
2. Install Poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python -
   ```
3. Set up the Poetry environment:
   ```
   poetry install
   ```
4. Activate the virtual environment:
   ```
   poetry shell
   ```
5. Run the Django development server:
   ```
   python manage.py runserver
   ```

#### Frontend

1. Navigate to the `frontend` directory of the project.
2. Make sure you have npm installed on your system.
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```
5. The frontend will be accessible at `http://localhost:3000`.



## API documentation

This document outlines the endpoints and functionalities provided by the API. The API allows users to interact with sheets and columns, perform operations such as creating sheets, fetching sheets by ID, updating column types, and retrieving supported data types.

### Endpoints

#### Create Sheet

`POST /api/sheets/`

**Description:**  
This endpoint allows users to create a new sheet. The body expects a file that is either a CSV or in excel format. It responses with the files metadata and each of columns in the dataset with its infered type. 

**Parameters:**  
None

**Request Body:**  
- **file**: The file to be uploaded. This parameter should contain the file data.

**Response:**  
- `id`: The unique identifier for the uploaded file.
- `file`: The file data.
- `file_name`: The name of the uploaded file.
- `number_of_records`: The number of records in the uploaded file.
- `uploaded_at`: The timestamp indicating when the file was uploaded.
- `columns`: Information about the columns associated with the uploaded file. Including the column name, id and data type



#### Get Sheet by ID  
`GET /api/sheets/<int:sheet_id>/`

**Description:**  
Fetches a sheet by its ID and enables server side pagination of the sheet data.

**Request Body:**  
- `start_index`: The starting index of the required records.
- `num_records`: The total number of records wanted.

**Parameters:**  
- `sheet_id`: Integer representing the ID of the sheet.

**Response:**  
- `id`: The unique identifier for the uploaded file.
- `file`: The file data.
- `file_name`: The name of the uploaded file.
- `number_of_records`: The number of records in the uploaded file.
- `uploaded_at`: The timestamp indicating when the file was uploaded.
- `columns`: Information about the columns associated with the uploaded file. Including the column name, id and data type
- `rows`: The rows associated with the sheet and the pagination range is specified in the request body.

#### Update Column Type  
 
`PUT /api/columns/<int:column_id>/`

**Description:**  
Updates the type of a column.

**Parameters:**  
- `column_id`: Integer representing the ID of the column to be updated.

**Request Body:**  
- `data_type`: The new data type that column wants to be converted to.

**Response:**
- `id`: The id of the column
- `file`: The id of the file the column belongs to.
- `name`: The name of the column
- `data_type`: The type of the column.

4. Get Supported Data Types  

**Endpoint:**  
`GET /api/supported-types/`

**Description:**  
Retrieves the list of supported data types for columns.

**Parameters:**  
None

**Response:**  
- `supported_types`: A list of supported data types.
## Testing

### Frontend test suite

To run the frontend test suite, follow these steps:

1. Navigate to the `frontend` directory of the project.
2. Run the following command to execute the tests using Jest:
   ```
   npm test
   ```

### Backend test suite

To run the backend test suite, follow these steps:

1. Navigate to the `backend` directory of the project.
2. Run the following command to execute the tests using Django's unit test framework:
   ```
   python manage.py test
   ```

## Supported types

The conversion functions are tested in the order supplied when they are registered. A column's type is inferred by applying these conversion functions sequentially until one successfully converts all values in the Series.


The following types are currently supported for conversion along with their order:

1. `bool`: Convert to boolean type.
2. `category`: Convert to categorical type if uniqueness ratio is less than a specified threshold.
3. `int8`: Convert to int8 type.
4. `int16`: Convert to int16 type.
5. `int32`: Convert to int32 type.
6. `int64`: Convert to int64 type.
7. `float32`: Convert to float32 type.
8. `float64`: Convert to float64 type.
9. `complex128`: Convert to complex numbers.
10. `timedelta64[ns]`: Convert to timedelta type.
11. `datetime64[ns]`: Convert to datetime type.
12. `object`: Convert the values in the column to object type.



## Supported None Types

The following None types are supported:

- `nan`
- `na`
- `n/a`
- `none`
- `null`
- `missing`
- `miss`
- `unknown`
- `unk`
- `-999`
- `not available`

All None types registered as supported work regardless of capitalization.


## Registering new types

To add support for a new type in the project, follow the steps outlined below:

### 1. Define Conversion Function

First, define a conversion function that either raises an exception if the conversion fails or successfully converts the pandas Series to the desired type.

Example:
```python
import pandas as pd

def convert_to_new_type(series: pd.Series) -> pd.Series:
    # Your conversion logic here
    pass
```


### 2. Register the function with the decorator 

Wrap the conversion function in a decorator @register_conversion, specifying the order at which point the conversion will be attempted. The order determines the priority of the conversion, with lower values being attempted first. Also, specify the name of the type using the type_name parameter.

```python
@register_conversion(order=11, type_name="object")
def convert_to_new_type(series: pd.Series) -> pd.Series:
    # Your conversion logic here
    pass
```


## Linting

This project has been linted with the black formatter for python and ES linter set to standard for javascript.
