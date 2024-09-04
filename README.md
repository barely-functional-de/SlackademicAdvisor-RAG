# SlackademicAdvisor-RAG

## Index

1. [Problem Statement](#problem-statement)
2. [About](#about)
3. [Features](#features)
4. [Technologies](#technologies)
5. [Project Structure](#project-structure)
6. [Reproducibility](#reproducibility)
7. [Conclusion](#conclusion)

---

## Problem Statement

The **SlackademicAdvisor-RAG** project aims to solve the problem of efficiently answering student queries by combining FAQ data from the LLM-Zoomcamp course repository and daily discussions from a dedicated Slack channel. This ensures that students have access to a comprehensive and up-to-date knowledge base, helping them find answers quickly and reducing the need for repetitive questions.

## About

**SlackademicAdvisor-RAG** is designed to streamline the onboarding process for students taking the LLM-Zoomcamp course. The LLM-Zoomcamp course repository includes a dedicated FAQ section with numerous subsections per module to address questions, alongside a vibrant Slack channel where daily discussions and queries take place. **SlackademicAdvisor-RAG** leverages these two data sources—FAQ and Slack channel data—to create a vector document that serves as a comprehensive base/ground-truth for answering any questions that new or existing students might have.

## Features

- Integration of FAQ data from the LLM-Zoomcamp course repository.
- Collection of questions and discussions from the Slack channel.
- Creation of a vector document for efficient question-answering.
- Retrieval-Augmented Generation (RAG) to provide accurate responses to student queries.
- Monthly updates and indexing of new data based on DataTalks Club #slack-dump.

## Technologies

- **LLM**: 
  - "ollama/tinyllama"
  - "openai/gpt-3.5-turbo"
  - "openai/gpt-4o-mini"
  
- **Knowledge Base**: 
  - Elasticsearch
  
- **Monitoring**: 
  - Grafana
  
- **Interface**: 
  - Streamlit
  
- **Ingestion Pipeline**: 
  - Mage-ai

## Project Structure

### Pipeline Blocks

The project uses **Mage-ai** for orchestrating the pipeline blocks
![Mage-ai Pipeline](./readme/orchestrator/mageai_pipeline.PNG)
![Mage-ai Pipeline Variables](./readme/orchestrator/mageai_pipeline_runtime_variables.PNG)

1. **Load_llm_zoomcamp_channel_data**:
   - Reads LLM-Zoomcamp channel data from the Slack dump folder specified in the `data_path` pipeline variable. 
   - On refresh, it checks for new files in the data path and reads them.

2. **Load_faq_data**:
   - Reads LLM-Zoomcamp FAQ data from DataTalks Club’s GitHub repository, specified in the `faq_data_path` pipeline variable.
   - On refresh, it checks for new entries in the FAQ data path and reads them.

3. **Chunk_llm_data**:
   - Receives data from the LLM-Zoomcamp channel and FAQ document, chunking the relevant fields (course, question, and answer) into a `chunk` column.

4. **Setup_elasticsearch**:
   - Initializes the Elasticsearch index.

5. **Index_documents**:
   - Reads the chunk data and Elasticsearch status before indexing the combined chunked documents into the LLM-Zoomcamp index set up in the `Setup_elasticsearch` block.

6. **Init_postgres_database**:
   - Initializes the PostgreSQL database with the tables `conversations`, and `user_feedback` and the required schema if it doesn’t exist. 
   - Captures the search conversations used to query the LLM-Zoomcamp Elasticsearch database.

7. **Elasticsearch_query_block**:
   - Tests Elasticsearch by querying the index storing the relevant information.


### Streamlit Interface

The project includes a **Streamlit** interface for the application:
![Streamlit UI](./readme/user_interface/streamlit_ui_feedback.PNG)

- **Sidebar (Settings)**: 
  - Contains course and model selection options for user queries.
  
- **Ask a Question**:
  - Accepts user queries and runs them against a RAG flow. 
  - Queries the knowledge base, builds the prompt, and sends it to the user-selected LLM.
  - Supports "ollama/tinyllama", "openai/gpt-3.5-turbo", and "openai/gpt-4o-mini" models.
  - Returns the answer to the UI along with details like Response time, Model Used, Associated Cost, and Total Tokens used.
  - Stores this information in the PostgreSQL `conversations` table set up with the pipeline execution.

- **Conversation History**:
  - Displays the latest search history for the last 10 conversations.
  - Expander for each conversation includes details like Question, Answer, Relevance, Model, and Timestamp.



### Monitoring with Grafana

For monitoring, the project uses **Grafana**:
![Grafana UI](./readme/monitor/monitoring_grafana_1.PNG)  
![Grafana UI](./readme/monitor/monitoring_grafana_2.PNG)

- **Grafana** is dependent on the PostgreSQL tables `conversations`, and `user_feedback`.
- Creates a dashboard with panels for:
  - Recent Conversations
  - Model Usage
  - Token Usage
  - OpenAI Cost
  - Response Time
  - Feedback Rating Analysis
  - Relevance Distribution 


## Reproducibility

### Requirements

**System Requirements**:  
Project is running on a GitHub Codespace machine with 2-core CPU, 8 GB RAM, and 32 GB storage.

**Docker Installed**:  
Ensure Docker is installed. If not, [follow this link to install Docker](https://docs.docker.com/get-docker/).

### .env Setup

Add a `.env` file in the folder `/rag-project-master` with the following details:

```bash
ENV=development

# Project settings
# If you start the project with ./start.sh, the project name and code path will already be set.
PROJECT_NAME=$PROJECT_NAME
MAGE_CODE_PATH=$MAGE_CODE_PATH

# Load custom files
PYTHONPATH="${MAGE_CODE_PATH}/${PROJECT_NAME}:${PYTHONPATH}"

# Database
POSTGRES_HOST=magic-database
POSTGRES_DB=magic
POSTGRES_PASSWORD=password
POSTGRES_USER=postgres
POSTGRES_PORT=5432
MAGE_DATABASE_CONNECTION_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}"

# Enhancements
export DYNAMIC_BLOCKS_VERSION=2
export KERNEL_MANAGER=magic
export MEMORY_MANAGER_PANDAS_VERSION=2
export MEMORY_MANAGER_POLARS_VERSION=2
export MEMORY_MANAGER_VERSION=2
export VARIABLE_DATA_OUTPUT_META_CACHE=1

# Elasticsearch Configuration
ELASTIC_URL_LOCAL=http://localhost:9200
ELASTIC_URL=http://elasticsearch:9200
ELASTIC_PORT=9200

# Ollama Configuration
OLLAMA_PORT=11434
OLLAMA_URL='http://ollama:11434/v1/'

# Streamlit Configuration
STREAMLIT_PORT=8501

# Other Configuration
MODEL_NAME=multi-qa-MiniLM-L6-cos-v1
INDEX_NAME=llm-course-qa

# OpenAI API Key
OPENAI_API_KEY=<your openai api key>
```

### Project Execution

- From the `/rag-project-master` folder, execute `./scripts/start.sh` to build and start the following services:
  - **Mage-ai**
  - **Magic Postgres**
  - **Elasticsearch**
  - **Streamlit**
  - **Grafana**
  - **Ollama**

- Make sure to do port forwarding for each of the services.

- From **Mage-ai**, running on port `6789`, execute the `llm-orchestration` pipeline. 
   
  ![LLM-Orchestration Pipeline](./readme/orchestrator/llm_orchestration_pipeline.PNG) 
  - The pipeline will set up the index `llm-zoomcamp` in Elasticsearch.
  - Initialize the tables `conversations` and `user_feedback` in the PostgreSQL database.

- Open up the **Streamlit** container running on port `8501` to ask questions.
  - The question-answer details, along with user feedback, are captured in PostgreSQL tables.

- Open up **Grafana** on port `3000` and configure it to use the PostgreSQL database. The details are provided in the `.env` file.

- Use the queries in the file [grafana.md](grafana.md) to recreate the Grafana dashboard for LLM-Zoomcamp.


## Conclusion

**SlackademicAdvisor-RAG** is an end-to-end RAG application that effectively combines Slack discussions and FAQ data to create a powerful and responsive system for assisting LLM-Zoomcamp students. Hence, making it a valuable tool for both students and educators.
