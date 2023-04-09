# File suf

This is a simple file storage web app built with [FastAPI](https://fastapi.tiangolo.com/) and [SQLite](https://www.sqlite.org/index.html). Users can upload files, and the app saves them to disk and records their metadata (original file name, upload time, etc.) in a SQLite database. Users can also download files they've uploaded by clicking on a link.

## Requirements

To run this app, you'll need:

* Python 3.9 or higher
* [Docker](https://www.docker.com/) (optional)

## Installation

1. Clone this repository to your local machine.

    ```git clone https://github.com/Vangardo/suf.git```

2. Navigate to the project directory.

    ```cd suf```

3. Create a virtual environment and activate it.

    ```python3 -m venv venv```
    ```source venv/bin/activate```

4. Install the dependencies.

    ```pip install -r requirements.txt```

## Usage

### Running the app locally

1. Activate your virtual environment.

    ```source venv/bin/activate```

2. Run the app.

    ```uvicorn main:app --reload```

3. Open your web browser and go to `http://localhost:8000`.

### Running the app with Docker

1. Build the Docker image.

    ```docker build -t suf.```

2. Run the Docker container.

    ```docker run -p 8000:80 file-storage-app```

3. Open your web browser and go to `http://localhost:8000`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)


