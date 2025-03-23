# AI Travel Planning Assistant

Hugging Face Link
   ```sh
   https://huggingface.co/spaces/RajGMore/aitrip_one
   ```
## Overview
The **AI Travel Planning Assistant** is a Streamlit-based web application that utilizes AI agents to help users plan their trips. The app takes user preferences such as travel type, interests, budget, and duration, then generates an optimized itinerary using Groq's LLaMA model.

## Features
- **City Selection**: Identifies the best cities based on user preferences.
- **Destination Insights**: Provides detailed information about attractions and hidden gems.
- **Itinerary Planning**: Creates a day-by-day travel itinerary.
- **Budget Management**: Estimates costs and suggests budget-friendly options.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Groq LLaMA-3 70B
- **Environment Management**: dotenv
- **Logging**: Python Logging Module

## Installation & Setup
### Prerequisites
- Python 3.8+
- pip
- Groq API Key

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/travel-ai-assistant.git
   cd travel-ai-assistant
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your API key:
   ```sh
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```
4. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

## Usage
1. Select your **travel preferences** from the sidebar.
2. Click **Generate Travel Plan** to get AI-powered recommendations.
3. Review the **city selection, attractions, itinerary, and budget breakdown**.

## Roadmap
- Add **real-time flight & hotel** suggestions.
- Improve **multi-city** itinerary generation.
- Enhance **budget customization** options.

## Contributing
Feel free to fork the repo and submit pull requests with improvements!

## License
This project is licensed under the MIT License.
