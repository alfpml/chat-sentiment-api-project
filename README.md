# chat-sentiment-api-project

**Description:** 
With pymomngo I created two collectionns of messages and users


## APIs Endpoints

- (GET) `/users`
  - **Purpose:** Get all users from all chats
- (GET) `/<username>/usermessages`
  - **Purpose:** Gets user messages
- (GET) `/user/create`
  - **Purpose:** New user creation
- (POST) `/chat/<chat_id>/addmessage` 
  - **Purpose:** Add messages to a given chat and user (creates user if n ot created)
- (POST) `/user/create` 
  - **Purpose:** Create a user and save into DB
- (GET) `/<chat_id>/sentiment` 
  - **Purpose:** Returns sentiment metrics of a given chat
