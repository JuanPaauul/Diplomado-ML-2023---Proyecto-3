# Diplomado-ML-2023---Proyecto-3
# Alessandro - Public Figure Information Virtual Assistant

## Description

Alessandro is a virtual assistant designed to provide users with quick and informative details about public figures. Whether you're curious about a celebrity, athlete, or any notable personality, Alessandro is at your service. This project integrates various technologies to create a seamless experience for retrieving information about public figures.

## Key Features

- **Voice Recognition:** Alessandro is always listening for user input, making the interaction natural and hands-free.
  
- **Intent Recognition:** Using Azure's Language SDK, Alessandro identifies the user's intent and focuses on inquiries related to public figures.

- **Content Moderation:** Ensuring a respectful and inclusive environment, Alessandro uses Azure Content Moderator to detect and handle offensive content.

- **Entity Recognition:** Azure's Text Analytics SDK helps Alessandro identify and extract the names of public figures from user queries.

- **Information Retrieval:** The heart of the system, Alessandro retrieves detailed information about the recognized public figure using Google's Knowledge graph API.

- **Speech Synthesis:** Alessandro uses Azure Speech SDK to convert textual responses into natural and spoken language, providing a comprehensive user experience.

## How to Use

1. **Speak to Alessandro:** Start by addressing Alessandro with your question about a public figure.

2. **Intent Recognition:** Alessandro processes your query, identifies the intent, and ensures it's related to public figures.

3. **Content Moderation:** Offensive content is detected and handled appropriately, maintaining a respectful interaction.

4. **Entity Recognition:** Alessandro extracts the public figure's name from your query using Azure Text Analytics SDK.

5. **Information Retrieval:** Alessandro leverages Google's Knowledge graph API to gather detailed information about the recognized public figure.

6. **Spoken Response:** Finally, Alessandro uses Azure Speech SDK to deliver the response in a clear and natural voice.

## Setup

To use Alessandro, follow the installation instructions below. Make sure to configure API keys for Azure services and, for Google's Knowledge graph API 

## Installation and Setup

make sure you have all the keys and endpoints previously set up before this 
```bash
# Clone the Repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install Dependencies
pip install ipykernel
pip install python-dotenv
other if necessary

create a env.txt file in the project root for the API keys.

for any more information or issues don't hesitate on contacting us.
