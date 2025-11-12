# Databricks MCP Universal Client: Reference Implementation

A reference implementation demonstrating the universal client pattern for Databricks integration using Model Context Protocol (MCP). This repository proves that standardizing Databricks communication through a single client reduces long-term maintenance effort and improves consistency across diverse application platforms.

## Overview

Enterprise applications access Databricks capabilities through custom integration code. Each application implements its own authentication, error handling, retry logic, and API communication. When Databricks updates APIs, every integration requires coordinated changes.

This repository demonstrates an alternative: implement a single universal client handling all Databricks MCP communication, with thin platform adapters focused exclusively on application concerns.

**Key Finding:** While this approach introduces modest overhead initially (~7% more code), it delivers 40-50% reduction in maintenance effort and 50-60% faster development of new platform integrations.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Slack Bot│  │RAG App   │  │REST API  │  │ Pipeline │   │
│  │ (350 loc)│  │(280 loc) │  │(220 loc) │  │ (190 loc)│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                          │
┌─────────────────────────┴─────────────────────────────────┐
│            Universal MCP Client (329 lines)                │
│  • Authentication  • Error Handling  • Retry Logic         │
│  • Protocol Negotiation  • Logging  • Response Parsing    │
└────────────────────┬──────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐  ┌─────────▼──────┐  ┌────────▼────────┐
│  Genie MCP     │  │  Vector Search │  │  UC Functions   │
│  Server        │  │  MCP Server    │  │  MCP Server     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Demos

This repository includes four realistic platform implementations:

### 1. Slack Bot - Genie Integration
**Use Case:** Business users ask natural language questions about data
**Technology:** Socket Mode, Slack Bolt, Databricks Genie
**Code:** 350 lines (50 Databricks-specific)

```bash
python demos/02-slack/slack_bot.py
```

[Full Documentation](demos/02-slack/README.md)

### 2. RAG Application - Vector Search Integration
**Use Case:** AI chatbot retrieves relevant documentation for context
**Technology:** Async Python, Vector Search, Document Retrieval
**Code:** 280 lines (40 Databricks-specific)

```bash
python demos/02-rag-application/rag_demo.py
```

[Full Documentation](demos/02-rag-application/README.md)

### 3. REST API - UC Functions Integration
**Use Case:** Product service calculates personalized discounts
**Technology:** FastAPI, Unity Catalog Functions, Governed Business Logic
**Code:** 220 lines (30 Databricks-specific)

```bash
python demos/03-rest-api/api_server.py
```

[Full Documentation](demos/03-rest-api/README.md)

### 4. Data Pipeline - Batch UC Functions
**Use Case:** ETL workflow applies standardized transformations
**Technology:** Async Python, Batch Processing, UC Functions
**Code:** 190 lines (30 Databricks-specific)

```bash
python demos/04-data-pipeline/pipeline_example.py
```

[Full Documentation](demos/04-data-pipeline/README.md)

## Quick Start

### Prerequisites

- Python 3.9+
- Databricks workspace with:
  - Genie space configured
  - Vector Search endpoint
  - Unity Catalog access
- Databricks CLI authentication configured

### Installation

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-org/databricks-mcp-demo
   cd databricks-mcp-demo
   ```

2. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Databricks configuration
   ```

5. **Setup Data Sources:**
   ```bash
   # Create Vector Search index
   python scripts/create_vector_search.py

   # Create UC Function
   python scripts/setup_uc_function.py
   ```

6. **Run a Demo:**
   ```bash
   # RAG Application (simplest to start with)
   python demos/02-rag-application/rag_demo.py
   ```

Detailed setup instructions: [SETUP.md](docs/SETUP.md)

## Key Metrics

### Code Volume

| Component | Lines of Code | Purpose |
|-----------|--------------|---------|
| **Universal MCP Client** | 329 | Databricks integration (all platforms) |
| Slack Bot | 350 | Slack-specific UI logic |
| RAG Application | 280 | RAG-specific logic |
| REST API | 220 | FastAPI HTTP logic |
| Data Pipeline | 190 | Batch processing logic |
| **Total** | **1,369** | |

**Databricks-specific code:** 479 lines (35% of total)
**Application logic:** 890 lines (65% of total)

### Maintenance Efficiency

- **API Update Time:** 40-50% reduction (1 codebase vs 4 codebases)
- **New Platform Development:** 50-60% faster (2-4 days vs 7-10 days)
- **Code Reuse:** UC Function used by both REST API and Pipeline (zero duplication)

Detailed measurements: [METRICS.md](docs/METRICS.md)

## Universal Client Pattern

The core pattern consists of a single client handling all Databricks MCP communication. Platform implementations import this client:

```python
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()

# Use any capability with identical pattern
response = await mcp_client.ask_genie(space_id, question)
docs = await mcp_client.search_docs(index_id, query)
result = await mcp_client.call_function(function_name, params)
```

Architecture details: [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Repository Structure

```
databricks-mcp-demo/
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment configuration template
├── shared/
│   ├── mcp_client.py            # Universal MCP client (329 lines)
│   └── config.py                # Shared configuration
├── demos/
│   ├── 02-slack/                # Slack + Genie demo (working)
│   ├── 02-rag-application/      # RAG + Vector Search demo
│   ├── 03-rest-api/             # REST API + UC Functions demo
│   └── 04-data-pipeline/        # Pipeline + UC Functions demo
├── scripts/
│   ├── create_vector_search.py  # Setup Vector Search index
│   └── setup_uc_function.py     # Create UC Function
└── docs/
    ├── ARCHITECTURE.md           # Technical architecture
    ├── SETUP.md                  # Detailed setup guide
    └── METRICS.md                # Performance measurements
```

## Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - Technical architecture and design decisions
- **[Setup Guide](docs/SETUP.md)** - Step-by-step setup instructions
- **[Metrics](docs/METRICS.md)** - Code measurements and performance data
- **[Blog Post V3](BLOG_POST_V3.md)** - Long-form article explaining the approach

## Related Resources

- [Databricks Model Context Protocol Documentation](https://docs.databricks.com/mcp/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Databricks SDK for Python](https://databricks-sdk-py.readthedocs.io/)

## License

This reference implementation is provided for educational purposes. Adapt freely to your organization's needs.

