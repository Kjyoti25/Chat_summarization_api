Chat Summarization and Insights API Documentation

Overview
This API provides a comprehensive solution for processing, storing, and analyzing chat conversations. It offers real-time chat ingestion, conversation retrieval, and advanced LLM-powered summarization and insights generation.
Features
•	Real-time chat storage: Efficiently store chat messages with high write throughput
•	Conversation retrieval: Flexible querying by user, conversation, or time period
•	AI-powered summarization: Generate concise summaries using large language models
•	Conversation insights: Extract sentiment, keywords, and other analytics
•	Scalable architecture: Designed for heavy CRUD operations with optimized queries

API Endpoints
1. Store Chat Messages
Endpoint: POST /chats
Description: Stores one or multiple chat messages in the database
Request Body:
json
{
  "conversation_id": "string",
  "user_id": "string",
  "messages": [
    {
      "content": "string",
      "timestamp": "datetime",
      "metadata": {}
    }
  ]
}
Response:
json
{
  "status": "success",
  "inserted_count": 3,
  "conversation_id": "conv_12345"
}

2. Retrieve Conversation
Endpoint: GET /chats/{conversation_id}
Description: Retrieves all messages from a specific conversation
Parameters:
•	page (optional): Pagination page number
•	limit (optional): Number of items per page
Response:
json
{
  "conversation_id": "conv_12345",
  "messages": [
    {
      "content": "Hello there!",
      "timestamp": "2023-01-01T12:00:00",
      "user_id": "user_1"
    }
  ],
  "page": 1,
  "total_pages": 3
}

3. Generate Summary
Endpoint: POST /chats/summarize
Description: Generates an AI-powered summary of a conversation
Request Body:
json
{
  "conversation_id": "string",
  "summary_type": "brief|detailed" 
}
Response:
json
{
  "conversation_id": "conv_12345",
  "summary": "The conversation began with greetings...",
  "insights": {
    "sentiment": "positive",
    "keywords": ["hello", "meeting", "project"],
    "action_items": ["Schedule follow-up"]
  },
  "generated_at": "2023-01-01T12:05:00"
}

4. Get User History
Endpoint: GET /users/{user_id}/chats
Description: Retrieves chat history for a specific user
Parameters:
•	page: Page number (default: 1)
•	limit: Items per page (default: 10)
•	start_date: Filter conversations from this date
•	end_date: Filter conversations until this date
Response:
json
{
  "user_id": "user_1",
  "conversations": [
    {
      "conversation_id": "conv_12345",
      "last_message": "Hello there!",
      "timestamp": "2023-01-01T12:00:00"
    }
  ],
  "total_conversations": 15,
  "page": 1
}

Setup Instructions
Prerequisites
•	Python 3.9+
•	MongoDB 5.0+
•	Redis (optional, for caching)
•	OpenAI API key (for LLM features)

Installation
1.	Clone the repository:
bash
git clone https://github.com/yourusername/chat-summarization-api.git
cd chat-summarization-api
2.	Create and activate virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.	Install dependencies:
bash
pip install -r requirements.txt
4.	Set up environment variables:
bash
cp .env.example .env
# Edit .env with your configuration

Running the API
bash
uvicorn main:app --reload
The API will be available at http://localhost:8000
Docker Deployment
1.	Build the image:
bash
docker-compose build
2.	Start the services:
bash
docker-compose up


Usage Examples
Storing Chats
python
import requests

url = "http://localhost:8000/chats"
data = {
    "conversation_id": "meeting_123",
    "user_id": "john_doe",
    "messages": [
        {"content": "Hello team!", "timestamp": "2023-01-01T09:00:00"},
        {"content": "Let's discuss the project", "timestamp": "2023-01-01T09:01:00"}
    ]
}

response = requests.post(url, json=data)
print(response.json())


Generating Summary
python
url = "http://localhost:8000/chats/summarize"
data = {
    "conversation_id": "meeting_123",
    "summary_type": "detailed"
}

response = requests.post(url, json=data)
print(response.json())


Error Handling
The API returns standard HTTP status codes with detailed error messages:
•	400 Bad Request: Invalid input data
•	404 Not Found: Resource not found
•	429 Too Many Requests: Rate limit exceeded
•	500 Internal Server Error: Server-side error




Error response format:
json
{
  "detail": {
    "error": "Error description",
    "code": "error_code",
    "timestamp": "2023-01-01T12:00:00"
  }
}

Rate Limiting
The API implements rate limiting to prevent abuse:
•	100 requests/minute for authenticated users
•	10 requests/minute for anonymous users

Monitoring
The API includes built-in Prometheus metrics at /metrics for:
•	Request counts
•	Response times
•	Error rates
•	Database query performance




Advanced Features
WebSocket Endpoint
Endpoint: ws://localhost:8000/ws/summarize
Description: Real-time summarization of ongoing conversations
Protocol:
1.	Client connects with conversation_id
2.	Server sends periodic summary updates
3.	Connection closes when conversation ends

Troubleshooting
1.	Database connection issues:
o	Verify MongoDB is running
o	Check connection string in .env
2.	LLM API errors:
o	Verify OpenAI API key is valid
o	Check rate limits on your account
3.	Performance problems:
o	Ensure proper indexing in MongoDB
o	Consider scaling with more API instances






