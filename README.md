# Docker Searching Movie Service

## Introduction
This project implements a movie search service using Elasticsearch, Redis, and a backup API, all deployed locally with Docker Compose.

---

## Project Components

### 1. Elasticsearch
- Used for storing and quickly searching movie-related data.
- Data from top IMDB movies is preloaded into Elasticsearch.

### 2. Redis
- Acts as a cache to store frequently accessed search results for faster responses.

### 3. Backup API Service
- If no result is found in Redis and Elasticsearch, this service queries a movie search API (suggested: one from [RapidAPI](https://rapidapi.com)).

---

## Search Flow
- The search request is first sent to Redis.
- If not found, it proceeds to Elasticsearch.
- If still no result, the backup API is queried.
- At any point, if a result is found, the process stops and returns the response.
- If no result is found in all three stages, an appropriate message is returned.

---

## How to Run

### Prerequisites
- Docker and Docker Compose

### Run the Project
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2. Run Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The search service will be available at `http://localhost:5000/search`.

---

## Tools and Resources
- Elasticsearch
- Redis
- Kibana
- RapidAPI
- Docker and Docker Compose




