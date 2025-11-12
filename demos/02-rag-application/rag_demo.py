"""
RAG Application Demo - Vector Search Integration

This demonstrates using the universal MCP client to build a Retrieval
Augmented Generation (RAG) application. The pattern shows how Vector Search
provides semantic document retrieval while the universal client handles all
Databricks communication.

Key Pattern: Import universal client, focus on RAG-specific logic.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import VECTOR_SEARCH_INDEX_ID


class Document:
    """Represents a retrieved document."""
    def __init__(self, title: str, content: str, category: str):
        self.title = title
        self.content = content
        self.category = category

    def __repr__(self):
        return f"Document(title='{self.title}', category='{self.category}')"


class SimpleRAGApplication:
    """
    Minimal RAG application demonstrating the universal client pattern.

    This focuses on the integration architecture, not production RAG features.
    In production, you would add:
    - Reranking of retrieved documents
    - Conversation memory
    - Citation tracking
    - Answer confidence scoring
    """

    def __init__(self):
        # Universal MCP client - handles ALL Databricks communication
        self.mcp_client = create_mcp_client()
        print("✅ RAG Application initialized with universal MCP client")

    async def retrieve_context(self, question: str, num_results: int = 3) -> List[Document]:
        """
        Retrieve relevant documents using Vector Search.

        Notice: Single line for Databricks integration.
        The universal client handles authentication, protocol negotiation,
        error handling, and response parsing.
        """
        print(f"\n🔍 Retrieving context for: '{question}'")

        # Universal client handles Vector Search communication
        raw_results = await self.mcp_client.search_docs(
            VECTOR_SEARCH_INDEX_ID,
            question,
            num_results=num_results
        )

        # Parse results into Document objects
        documents = self._parse_results(raw_results)

        print(f"✅ Retrieved {len(documents)} relevant documents")
        for i, doc in enumerate(documents, 1):
            print(f"   {i}. {doc.title} ({doc.category})")

        return documents

    def _parse_results(self, raw_results: str) -> List[Document]:
        """Parse JSON results from Vector Search into Document objects."""
        import json

        try:
            if raw_results.strip().startswith('['):
                results = json.loads(raw_results)
            else:
                data = json.loads(raw_results)
                results = data.get('results', data.get('data', []))

            documents = []
            for result in results:
                if isinstance(result, dict):
                    doc = Document(
                        title=result.get('title', 'Untitled'),
                        content=result.get('content', ''),
                        category=result.get('category', 'Unknown')
                    )
                    documents.append(doc)

            return documents
        except json.JSONDecodeError:
            print(f"⚠️ Could not parse results: {raw_results[:100]}")
            return []

    def synthesize_answer(self, question: str, documents: List[Document]) -> str:
        """
        Synthesize answer from retrieved documents.

        In production, this would call an LLM (OpenAI, Anthropic, etc.)
        For this demo, we use simple text extraction to show the pattern.
        """
        print(f"\n💭 Synthesizing answer from {len(documents)} documents...")

        if not documents:
            return "I couldn't find relevant information to answer that question."

        # Simple extraction-based answer (production would use LLM)
        answer_parts = []
        answer_parts.append(f"Based on the documentation:\n")

        for i, doc in enumerate(documents[:2], 1):  # Use top 2 documents
            # Extract first 200 chars as relevant excerpt
            excerpt = doc.content[:200].strip()
            if len(doc.content) > 200:
                excerpt += "..."

            answer_parts.append(f"\n**{doc.title}:**")
            answer_parts.append(excerpt)

        answer_parts.append(f"\n\n_Answer synthesized from {len(documents)} documents_")

        return "\n".join(answer_parts)

    async def ask(self, question: str) -> str:
        """
        Main RAG pipeline: retrieve context, synthesize answer.

        This is the full RAG pattern:
        1. Retrieve relevant documents via Vector Search
        2. Synthesize answer using retrieved context
        """
        # Step 1: Retrieve context (Vector Search via universal client)
        documents = await self.retrieve_context(question, num_results=3)

        # Step 2: Synthesize answer (application-specific logic)
        answer = self.synthesize_answer(question, documents)

        return answer


async def interactive_demo():
    """Run interactive RAG demo."""
    print("=" * 70)
    print("RAG Application Demo - Universal MCP Client Pattern")
    print("=" * 70)
    print()
    print("This demo shows how to build a RAG application using the universal")
    print("MCP client. Notice how Databricks integration is a single import.")
    print()

    rag = SimpleRAGApplication()

    # Example questions
    questions = [
        "How do I create a Genie space?",
        "What is Vector Search used for?",
        "How do I set up OAuth authentication?"
    ]

    print("\n" + "=" * 70)
    print("Running Example Queries")
    print("=" * 70)

    for question in questions:
        print(f"\n{'─' * 70}")
        print(f"❓ Question: {question}")
        print('─' * 70)

        answer = await rag.ask(question)

        print(f"\n💡 Answer:")
        print(answer)
        print()

    print("=" * 70)
    print("Demo Complete")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  • Universal MCP client handles all Databricks communication")
    print("  • Application code focuses on RAG-specific logic")
    print("  • Adding new platforms requires only importing the client")
    print("  • No custom Vector Search integration code needed")


async def single_question_demo(question: str):
    """Answer a single question (useful for testing)."""
    rag = SimpleRAGApplication()
    answer = await rag.ask(question)
    print(answer)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line mode: python rag_demo.py "your question here"
        question = " ".join(sys.argv[1:])
        asyncio.run(single_question_demo(question))
    else:
        # Interactive demo mode
        asyncio.run(interactive_demo())
