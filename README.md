# VIL Data Ingestion API

A high-performance FastAPI application designed to receive, process, and store data dumps from VIL JSON export. It provides a generic and scalable architecture for ingesting data for multiple database tables.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9+
- Docker & Docker Compose
- Git

## 1. Setup and Installation

Follow these steps to set up your local development environment.

**1. Install Dependencies**
```bash
pip install -r requirement.txt
```

**2. Configure Environment Variables**
Copy the example environment file and update it with your database credentials.
```bash
cp .env.example .env
```
Now, open the `.env` file and set the values for `DB_USER`, `DB_PASSWORD`, and `DB_NAME`. The `DATABASE_URL` will be constructed from these values.

## 2. Running the Application

The application consists of two main components: the PostgreSQL database and the FastAPI server.

### Starting the PostgreSQL Server

The database runs in a Docker container, managed by Docker Compose.

**1. Start the Database Container**
Run this command from the project root directory:
```bash
sudo docker compose --env-file /env/file/path/.env up --build
```

**2. Verify the Database is Running**
```bash
sudo docker ps
```
You should see the `VIL_API` service with the status `Up`.

**3. Stop the Database**
To stop the container when you are done:
```bash
docker compose down
```

### Starting the FastAPI Application

Once the database is running, you can start the API server.

```bash
uvicorn main:app --host 0.0.0.0 --port 8024
```

The API will now be running and accessible at `http://localhost:8024`.

## 3. How It Works

### Logging

The application uses two forms of logging:
- **Console Logs:** Uvicorn prints real-time access logs and application errors to your terminal. This is useful for immediate debugging.
- **Transaction Logs:** For every upload request, a detailed transaction log is generated in the `logs/` directory.
    - **Purpose:** To provide a permanent, auditable record of each data dump.
    - **Naming:** Each file is uniquely named with a timestamp (e.g., `upload_articles_20251015_175310_123456.txt`).
    - **Content:** The log details the success or failure of each individual item in the payload, along with the specific reason for any failures, and concludes with a summary of the entire operation.

### Storage

The application follows a hybrid storage approach:
- **Database (PostgreSQL):** Stores all the structured metadata for each record (e.g., dates, authors, subjects).
- **File System (`storage/` directory):** For each successfully processed record, the original JSON object for that item is saved as a separate `.json` file.
    - **Purpose:** Creates a "source of truth" backup for every record, allowing for easy re-processing or auditing.
    - **Location:** Files are organized into subdirectories based on the entity type (e.g., `storage/articles/`, `storage/ce/`).
    - **Naming:** Files are named using their database primary key (e.g., `1_article.json`, `15_ce.json`).
    - **Link:** The `file_storage_path` column in each database table contains the absolute path to its corresponding JSON file on the server.

### API Endpoints

The API is built around a generic, factory-based routing system. Each data type has its own dedicated upload endpoint.

- **Pattern:** `POST /<entity_name>/upload`
- **Examples:**
    - `POST /articles/upload`
    - `POST /budgets_union/upload`
    - `POST /ce/upload`
- **Request Body:** The endpoint expects the full, raw JSON array exported from PHPMyAdmin.
- **Response:** Upon success, the API returns a simple JSON message confirming how many items were processed, along with a list of success strings.

#### Example Usage with `curl`

To test an endpoint, use `curl` from your terminal. Make sure you have a `sample_payload.json` file in your directory.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data "@sample_payload.json" \
  http://localhost:8024/articles/upload
```
- **Note:** The `@` symbol before the filename is crucial. It tells `curl` to send the *content* of the file, not the filename itself.

A successful response will look like this:
```json
{
  "message": "Successfully processed 1 article(s).",
  "processed_items": [
    "'data/articles/article221124.htm' has been successfully added to the LKS X VIL data dump"
  ]
}
```
