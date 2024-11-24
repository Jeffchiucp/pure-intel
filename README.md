# Pure Intel AI: War News & Social Media Summarizer

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io/)

## Overview

Pure Intel is an AI-powered intelligence system designed to analyze real-time war news and social media feeds, providing actionable insights for conflict zones. The system leverages cutting-edge AI tools and APIs to monitor RSS feeds and social media (Twitter/X), filter military-relevant content using domain-specific embeddings, and produce concise, translated summaries.

## Features

### 🔍 Social Media Analysis
- Real-time monitoring of tweets and social media content
- Extraction of key information for trend identification
- Actionable insights generation

### 📰 RSS Feed Processing
- Automated article fetching from multiple RSS feeds
- Translation of non-English content to English
- Detailed summaries generation with comprehensive overview

### 🎯 Military-Specific Intelligence
- Specialized embeddings for conflict-related information
- Domain-focused content filtering
- Actionable military insights

## Tech Stack

- **Backend Framework**: Python, FastAPI
- **Frontend Interface**: Streamlit
- **AI Components**: 
  - Restack AI
  - OpenAI 
  - OpenBabylon API
  - Toolhouse 
- **Data Sources**: 
  - RSS Feeds
  - Twitter/X via Toolhouse
- **Performance**: Asynchronous programming optimization

## Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/pure-intel-ai.git
cd pure-intel-ai
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run main.py
```

## API Configuration

### OpenBabylon API
- **Endpoint**: `http://64.139.222.109:80/v1`
- **Note**: Requires dummy API key (`api_key="openbabylon"`) for OpenAI SDK compatibility
- No authentication required

## Core Components

### `workflow.py`
Core engine implementing modular, multi-step workflows using Restack AI:
- Social media content analysis
- RSS feed scraping and summarization
- Translation and data aggregation
- Robust error handling

### `main.py`
Streamlit-based user interface managing:
- User input collection (Twitter handles, RSS URLs)
- Workflow execution
- Real-time result visualization
- Progress tracking and logging

## Challenges Overcome

1. Seamless integration of multiple AI agents
2. Maintaining unbiased analysis of war-related content
3. Real-time performance optimization
4. Complex data visualization in user-friendly format
5. Twitter/X data parsing and extraction

## Achievements

- ✅ Fully functional AI system with Restack workflows
- ✅ Multi-agent collaboration implementation
- ✅ Intuitive Streamlit interface
- ✅ Robust logging and error handling

## Learning Outcomes

1. Restack workflow implementation for multi-agent systems
2. Domain-specific AI model fine-tuning
3. Asynchronous processing optimization
4. Third-party API integration (OpenBabylon, Toolhouse)
5. Multilingual data processing and summarization

## Future Roadmap

- [ ] User account system with preferences
- [ ] Enhanced Twitter/X analytics
- [ ] Mobile applications (iOS/Android)
- [ ] Extended language support
- [ ] Performance optimization
- [ ] Advanced AI reasoning capabilities



## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Docker (for running Restack services)

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
   ```

2. Open the Web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples/defense_quickstart_news_scraper_summarizer
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry env use 3.12
   ```

   ```bash
   poetry shell
   ```

   ```bash
   poetry install
   ```

   ```bash
   poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
   ```

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your OpenBabylon API URL:

   ```bash
   cp .env.example .env
   # Edit .env and add your:
   # OPENBABYLON_API_URL
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run FastAPI app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run app
   ```

8. In a new terminal, run the Streamlit frontend

   ```bash
   poetry run streamlit run frontend.py
   ```

9. You can test the API endpoint without the Streamlit UI with:

```bash
curl -X POST \
  http://localhost:8000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.pravda.com.ua/rss/", "count": 5}'
```

This will schedule the workflow and return the result.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

[MIT License](LICENSE)

