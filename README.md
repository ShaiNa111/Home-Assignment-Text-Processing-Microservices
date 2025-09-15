# Home-Assignment-Text-Processing-Microservices

## Table of Contents
- [Download Project](#download--running-project)
- [Health Check](#health-check)
- [Running Commands](#test-commands)

### Download & Running Project
1. Download docker-compose.yml file.
2. Login: Use the command `docker login ghcr.io -u shaina111 -p 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` to login the GitHub ghcr.io server.<br>
You should see `Login Succeeded` message. 
3. Open Terminal and cd to get path where the docker-compose.yml file is locate.
4. Run `docker-compose up -d` to run the docker-compose and auto pulling all the images.

### Health Check
1. Open terminal and run `curl -X GET "http://0.0.0.0:8000/health" -H "Content-Type: application/json" -d '{}'`<br>
This should return {"status": "ok"} if everting running well.

### Test Commands
Open terminal and run `curl -X POST "http://0.0.0.0:8000/summarize" -H "Content-Type: application/json" -d '{"text": "I love this service. It works great!"}'`


