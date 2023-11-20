# Football Results App

This is a Python application that displays football results of the 'Ekstraklasa' Polish league. It can be built using Docker or by running the `app.py` file to create a Streamlit app.

## Getting Started

To get started with the project, follow these steps:

### Prerequisites

- Python (preferably newest stable version)
- Docker (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TokarskiPatryk/football-results-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd football-results-app
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create an `.env` file in the project root directory.

2. Add the following parameters to the `.env` file:

   ```plaintext
    API_KEY="<your API_KEY>"
    API_HOST="odds.p.rapidapi.com"
   ```

   Replace `<your API_KEY>` with your API key from rapidapi.com

### Usage

#### Running with Docker

1. Build the Docker image:

   ```bash
   docker build -t football-results-app .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8501:8501 football-results-app
   ```

3. Open your web browser and visit `http://localhost:8501` to access the app.

#### Running without Docker

1. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and visit `http://localhost:8501` to access the app.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
