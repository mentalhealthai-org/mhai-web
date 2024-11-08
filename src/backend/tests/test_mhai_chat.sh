#!/bin/bash

# Set token and API base URL
TOKEN="f7b5563b753a35ce370650b4465fb19e18f9efb7"
BASE_URL="http://localhost:8000/api/chat"

# Generate a unique chat room name
ROOM_NAME="example_room_$(date +%s)"

# Create a new chat room with a unique name
echo "Creating a new chat room with name $ROOM_NAME..."
CREATE_ROOM_RESPONSE=$(curl -s -X POST "$BASE_URL/create-room/" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$ROOM_NAME\"}")

# Capture the room ID, or exit if creation failed
ROOM_ID=$(echo $CREATE_ROOM_RESPONSE | jq -r '.id')
if [ "$ROOM_ID" == "null" ]; then
  echo "Failed to create chat room. Response:"
  echo "$CREATE_ROOM_RESPONSE" | jq .
  exit 1
fi
echo "Chat room created with ID: $ROOM_ID"

# Send a user message to the chat room
echo "Sending a user message to the chat room..."
USER_MESSAGE_RESPONSE=$(curl -s -X POST "$BASE_URL/send-message/" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"chat_room\": $ROOM_ID, \"content\": \"Hello, this is a test message!\", \"message_type\": \"USER\"}")

echo "User message sent:"
echo "$USER_MESSAGE_RESPONSE" | jq .

# Send an AI message to the chat room
echo "Sending an AI message to the chat room..."
AI_MESSAGE_RESPONSE=$(curl -s -X POST "$BASE_URL/send-message/" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"chat_room\": $ROOM_ID, \"content\": \"Hello, this is an AI response!\", \"message_type\": \"AI\"}")

echo "AI message sent:"
echo "$AI_MESSAGE_RESPONSE" | jq .

# Retrieve messages from the chat room
echo "Retrieving messages from the chat room..."
MESSAGES_RESPONSE=$(curl -s -X GET "$BASE_URL/messages/$ROOM_ID/" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json")

echo "Messages in chat room $ROOM_ID:"
echo "$MESSAGES_RESPONSE" | jq .

# List all chat rooms
echo "Listing all chat rooms..."
ROOMS_LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/rooms/" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json")

echo "All chat rooms:"
echo "$ROOMS_LIST_RESPONSE" | jq .

echo "All tests completed!"
