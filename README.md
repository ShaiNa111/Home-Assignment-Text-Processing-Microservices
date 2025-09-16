# Home-Assignment-Text-Processing-Microservices

This project provides text processing microservices (summarization, sentiment analysis, etc.) using FastAPI and gRPC,
packaged with Docker for easy deployment.
In addition, create CI using GitHub Actions

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup & Run](#setup--run)
- [Health Check](#health-check)
- [Test the Service](#test-service)

---

## Prerequisites

Before running the project, make sure you have:

- [Docker](https://www.docker.com/get-started) installed.
- [Docker Compose](https://docs.docker.com/compose/) installed.
- Access to GitHub Container Registry (GHCR) for pulling prebuilt images.

---

## Setup & Run

1. **Download docker-compose.yml file from the GitHub repository.**:
2. **Login: Use the command `docker login ghcr.io -u shaina111 -p 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` to login the
   GitHub ghcr.io server.**:
3. **Open Terminal and cd to get path where the docker-compose.yml file is locate.**
4. **Run `docker-compose up -d` to run the docker-compose and auto pulling all the images.**

---

### Health Check

**Open terminal and run:**
   ```
        curl -X GET "http://0.0.0.0:8000/health" -H "Content-Type: application/json" -d '{}'
   ```
    Expected response: {"status": "ok"} if everting running well.

---

### Test Service

**Open terminal and run:**
   ```
        curl -X POST "http://0.0.0.0:8000/summarize" -H "Content-Type: application/json" -d '{"text": "I love this service. It works great! see you in UK"}'
   ```
    Expected response: 

    {
        "tokens":["I","love","this","service",".","It","works","great","!","see","you","in","UK"],
        "sentences":["I love this service.","It works great!","see you in UK"],
        "sentiment":"Positive",
        "entities":[{"text":"UK","label":"GPE"}]
    }
        

