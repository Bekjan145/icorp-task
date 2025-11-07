# iCorp Task

## Goal

Create a script to interact with the test API:

https://test.icorp.uz/interview.php

Skills being tested:

- HTTP communication
- Data processing
- Working with webhooks and asynchrony

Everything is implemented in a single file (`main.py`).

---

## Technologies

| Component   | Purpose                     |
|-------------|-----------------------------|
| Python 3.12 | Language                    |
| FastAPI     | REST API and webhook server |
| httpx       | Asynchronous HTTP client    |
| uvicorn     | ASGI server                 |
| ngrok       | Tunneling the local server  |

---

## Service Workflow

1. POST request → `interview.php`  
   Payload:
   ```json
   {
     "msg": "Hello iCorp!",
     "url": "https://<your-ngrok>/webhook"
   }

The server sends back part1.

2. Your server receives `part2` at the `/webhook` endpoint.

3. Combine:

   ```
   full_code = part1 + part2
   ```

4. GET request:

   ```
   interview.php?code=full_code
   ```

The server returns the final message.

---

## Running the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
python main.py
```

### 3. Start ngrok

```bash
ngrok http 8000
```

Copy the URL in the format:

```
https://xxxxxx.ngrok-free.dev
```

Create a `.env` file and add::

```
WEBHOOK_URL=https://xxxxxx.ngrok-free.dev/webhook
```

---

## Example Console Output

```
PART 1: abc123
PART 2: def456
FULL CODE: abc123def456
FINAL MESSAGE: Hello iCorp!
```

---

## Author

Bekjigitov Bekjan

Telegram: @bekjan_bekjigitov

---

## requirements.txt

````
fastapi
uvicorn
httpx
python-dotenv
pydantic
````