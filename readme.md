
# Flask Web Scraper API

This project is a backend API service built with Flask. It provides a platform to scrape websites, extract content, and generate a digest and analysis using OpenAI. The project uses:

- **Flask-SQLAlchemy** to interact with a PostgreSQL database.
- **Auth0** for authentication.
- **Selenium** and **BeautifulSoup4** for web scraping and content extraction.
- **OpenAI API** to analyze and generate summaries for the scraped content.

## Setup

### 1. Setup Virtual Environment
Create and activate a Python virtual environment:

```zsh
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Chrome for Selenium
This project requires Google Chrome for Selenium to run properly.

- **Option 1**: Install Chrome from the [official website](https://www.google.com/chrome/).
- **Option 2**: Install Chrome via terminal (Debian-based Linux):

  ```zsh
  sudo apt update
  sudo apt install -y wget
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo dpkg -i google-chrome-stable_current_amd64.deb
  sudo apt --fix-broken install -y
  ```

### 3. Setup Environment Variables
Copy the `.env.example` file to `.env`

```zsh
cp .env.example .env
```
Configure the following variables:

```zsh
# Flask
FLASK_APP=api
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_TESTING=True
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=5011

# Auth0
CLIENT_ORIGIN_URL=http://localhost:3000
AUTH0_AUDIENCE=
AUTH0_DOMAIN=

# OpenAI
OPENAI_API_KEY=

# Database
DATABASE_USER=admin
DATABASE_PWD=admin
DATABASE_NAME=webscraper
DATABASE_URL="postgresql://${DATABASE_USER}:${DATABASE_PWD}@localhost:5432/${DATABASE_NAME}"
```

### 4. Initialize the Database
To initialize the PostgreSQL database, you have two options to do first:

- **Option 1**: Start a local database with Docker Compose:

  ```zsh
  docker-compose up -d
  ```

- **Option 2**: Using remote database as AWS RDS:



After that, update the `DATABASE_URL` in the .env file, 
- Then, Initialize the database by the command below:

  ```zsh
  flask init-db
  ```

### 5. Run the Application
To start the Flask application, use the following command:

```zsh
flask run
```

## Project Structure

- `api`: Main application code and endpoints.
- `.env.example`: Environment variable template.
- `requirements.txt`: Project dependencies.

## Additional Information

- **Auth0**: Make sure to configure `AUTH0_AUDIENCE` and `AUTH0_DOMAIN` for your Auth0 application.
- **Database**: Ensure PostgreSQL is running and accessible at the configured `DATABASE_URL`.
