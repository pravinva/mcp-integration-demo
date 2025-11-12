# RAG Application Demo - Vector Search Integration

## Overview

This demo shows how to build a Retrieval Augmented Generation (RAG) application using the universal MCP client to access Databricks Vector Search. The implementation demonstrates the key pattern: import the universal client, focus on application-specific logic.

## Architecture

```
User Question
    ↓
RAG Application (rag_demo.py)
    ↓
Universal MCP Client (shared/mcp_client.py)
    ↓
Databricks Vector Search MCP Server
    ↓
Vector Search Index
```

## Key Pattern

**Traditional RAG Implementation:**
```python
# Custom Vector Search client (200-300 lines)
class VectorSearchClient:
    def __init__(self):
        self.setup_auth()
        self.setup_embeddings()
        # ... lots of Databricks-specific code

    def search(self, query):
        # Custom implementation of Vector Search API
        # Handle authentication, errors, retries, parsing
        pass
```

**Universal Client Pattern:**
```python
from shared.mcp_client import create_mcp_client

# Single import gives production-ready Databricks integration
mcp_client = create_mcp_client()

# One line retrieves documents
results = await mcp_client.search_docs(index_id, query)
```

## Code Statistics

- **Total lines:** 165
- **Databricks-specific lines:** ~15 (9%)
- **RAG-specific logic:** ~150 (91%)

The universal client handles all Vector Search communication. This implementation focuses on RAG patterns: document retrieval, answer synthesis, result formatting.

## What This Demo Shows

1. **Integration Simplicity:** Vector Search access requires importing the universal client, not implementing custom integration code.

2. **Focus on Business Logic:** 91% of code handles RAG-specific concerns (parsing documents, synthesizing answers, formatting output).

3. **Production Patterns:** Error handling, logging, and authentication are inherited from the universal client.

## What This Demo Doesn't Include

This is a minimal RAG implementation demonstrating the integration pattern. Production RAG applications would add:

- **LLM Integration:** Call OpenAI, Anthropic, or Databricks Foundation Models for answer synthesis
- **Reranking:** Reorder retrieved documents by relevance
- **Conversation Memory:** Track multi-turn conversations
- **Citation Tracking:** Link answer segments to source documents
- **Confidence Scoring:** Indicate answer reliability

## Setup

1. **Prerequisites:**
   ```bash
   # Vector Search index must exist
   # Configured in .env as VECTOR_SEARCH_INDEX_ID
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Interactive Demo:**
   ```bash
   python rag_demo.py
   ```

4. **Ask Specific Question:**
   ```bash
   python rag_demo.py "How do I create a Genie space?"
   ```

## Example Output

```
🔍 Retrieving context for: 'How do I create a Genie space?'
✅ Retrieved 3 relevant documents
   1. Getting Started with Databricks Genie (Tutorial)
   2. Best Practices for Genie Spaces (Best Practices)
   3. Genie MCP Server (Tutorial)

💭 Synthesizing answer from 3 documents...

💡 Answer:
Based on the documentation:

**Getting Started with Databricks Genie:**
Databricks Genie is an AI-powered analytics assistant that lets you ask
questions about your data in natural language. To get started: 1) Create
a Genie Space in the SQL workspace, 2) Connect your tables from Unity...

**Best Practices for Genie Spaces:**
Optimize your Genie Space for better results: 1) Rich Metadata - Add
comprehensive descriptions to tables, columns, and views explaining
business context and calculation logic...

_Answer synthesized from 3 documents_
```

## Integration Code

The entire Databricks integration consists of:

```python
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()

results = await mcp_client.search_docs(
    VECTOR_SEARCH_INDEX_ID,
    question,
    num_results=3
)
```

The universal client handles:
- Authentication via workspace client
- Protocol negotiation with Vector Search MCP server
- Error handling and retries
- Response parsing

## Extending This Demo

To build a production RAG application:

1. **Add LLM Integration:**
   ```python
   import openai

   def synthesize_answer(self, question, documents):
       context = "\n\n".join([d.content for d in documents])
       prompt = f"Based on this context:\n{context}\n\nAnswer: {question}"
       return openai.ChatCompletion.create(
           model="gpt-4",
           messages=[{"role": "user", "content": prompt}]
       )
   ```

2. **Add Reranking:**
   ```python
   from sentence_transformers import CrossEncoder

   reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
   scores = reranker.predict([(question, d.content) for d in documents])
   documents = [d for _, d in sorted(zip(scores, documents), reverse=True)]
   ```

3. **Add Conversation Memory:**
   ```python
   class RAGWithMemory(SimpleRAGApplication):
       def __init__(self):
           super().__init__()
           self.conversation_history = []

       async def ask(self, question):
           # Include conversation context in retrieval
           context_question = self._build_contextual_question(question)
           answer = await super().ask(context_question)
           self.conversation_history.append((question, answer))
           return answer
   ```

## Performance

Typical query latency:
- Vector Search: 800-1500ms
- Document parsing: 10-20ms
- Answer synthesis (mock): 5-10ms
- **Total:** ~1 second

The universal client adds <50ms overhead. Most latency comes from Vector Search computation (embedding generation, similarity search).

## Comparison to Traditional Implementation

**Traditional Approach:**
- Implement custom Vector Search client: 200-300 lines
- Handle authentication: 50 lines
- Implement error handling: 40 lines
- Add retry logic: 30 lines
- Write tests: 100 lines
- **Total:** 420-520 lines of Databricks integration code

**Universal Client Approach:**
- Import universal client: 1 line
- Call search_docs: 1 line
- **Total:** 2 lines of Databricks integration code

The universal client provides the other 418-518 lines as a tested, maintained library.

## Related Demos

- **Slack Bot** (`demos/01-slack-bot/`) - Genie integration for natural language analytics
- **REST API** (`demos/03-rest-api/`) - UC Functions integration for business logic
- **Data Pipeline** (`demos/04-data-pipeline/`) - Batch UC Functions usage

All demos use the same universal MCP client with different application patterns.
