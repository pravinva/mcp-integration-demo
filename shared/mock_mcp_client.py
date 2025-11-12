"""
Mock MCP client for testing without Databricks connection.
Useful for development and demos when offline.

Simulates responses from Genie, Vector Search, and UC Functions.
"""

import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class MockMCPClient:
    """
    Fake MCP client that returns canned responses.
    Same interface as UniversalMCPClient - perfect for testing!
    """
    
    def __init__(self):
        logger.info("🧪 Mock MCP Client initialized (no real Databricks connection)")
        
        # Mock responses for Genie
        self.genie_responses = {
            "revenue": """📊 **Q4 2024 Revenue Analysis**

• Total Revenue: $1.2M (↑15% from Q3)
• Top Region: North America ($600K, 50%)
• Growth Rate: 15% quarter-over-quarter
• Top Customer: Acme Corporation ($200K)

**SQL Query:**
SELECT
SUM(total_amount) as total_revenue,
COUNT(DISTINCT customer_id) as unique_customers
FROM orders
WHERE quarter = 'Q4' AND year = 2024


**Key Insights:**
- Enterprise segment grew 25%
- Product mix shifted toward higher-margin software
- Customer retention at 95%""",
            
            "customer": """👥 **Top 5 Customers by Revenue**

1. **Acme Corporation** - $200,000
   - Segment: Enterprise
   - Growth: +30% YoY
   
2. **TechStart Inc** - $180,000
   - Segment: SMB
   - Growth: +45% YoY
   
3. **Global Systems Ltd** - $150,000
   - Segment: Enterprise
   - Growth: +10% YoY
   
4. **DataWorks GmbH** - $140,000
   - Segment: Mid-Market
   - Growth: +20% YoY
   
5. **CloudFirst SAS** - $130,000
   - Segment: SMB
   - Growth: +35% YoY

**SQL Query:**

SELECT
c.customer_name,
SUM(o.total_amount) as total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.year = 2024
GROUP BY c.customer_name
ORDER BY total_revenue DESC
LIMIT 5

            
            "default": """**Analysis Result**

This is a mock response for your question: "{question}"

In a production environment, this would query your actual Databricks tables and return real insights.

**Sample Data:**
- Metric A: 42%
- Metric B: $1.5M
- Metric C: 1,234 units

**SQL Query:**


SELECT * FROM your_table WHERE condition = true

        }
        
        # Mock documentation for Vector Search
        self.documentation = [
            {
                "title": "Getting Started with Databricks Genie",
                "content": "Databricks Genie is an AI-powered analytics assistant. Create a space, add tables, and start asking questions in natural language.",
                "category": "Tutorial"
            },
            {
                "title": "Model Context Protocol (MCP) Overview",
                "content": "MCP is a standard for connecting AI applications to data sources. Reduces M×N integration problem to M+N through protocol standardization.",
                "category": "Concepts"
            },
            {
                "title": "Unity Catalog Functions Guide",
                "content": "Register Python, SQL, or Scala functions in Unity Catalog. Governed with standard GRANT/REVOKE permissions.",
                "category": "How-To"
            },
            {
                "title": "Vector Search for RAG Applications",
                "content": "Enable similarity search for Retrieval Augmented Generation. Automatically handles embedding generation and scoring.",
                "category": "How-To"
            },
            {
                "title": "Deploying Databricks Apps",
                "content": "Deploy web applications, APIs, and bots on Databricks infrastructure. Automatic scaling and Unity Catalog integration.",
                "category": "Tutorial"
            }
        ]
    
    async def query(self, server_url: str, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Mock query - returns canned responses"""
        await asyncio.sleep(0.3)  # Simulate network delay
        
        # Determine which service based on URL
        # Updated to match new URL formats:
        # - Vector Search: /api/2.0/mcp/vector-search/{catalog}/{schema}
        # - UC Functions: /api/2.0/mcp/functions/{catalog}/{schema}
        if "/mcp/genie/" in server_url:
            return self._mock_genie(arguments)
        elif "/mcp/vector-search/" in server_url:
            return self._mock_vector_search(arguments)
        elif "/mcp/functions/" in server_url:
            return self._mock_uc_function(arguments)
        
        return "Mock MCP Server: Unknown endpoint"
    
    def _mock_genie(self, arguments: Dict) -> str:
        """Mock Genie responses"""
        question = arguments.get("question", "").lower()
        
        # Match keywords to responses
        for keyword, response in self.genie_responses.items():
            if keyword in question:
                return response
        
        # Default response
        return self.genie_responses["default"].format(question=arguments.get("question"))
    
    def _mock_vector_search(self, arguments: Dict) -> str:
        """Mock Vector Search responses"""
        query = arguments.get("query", "").lower()
        num_results = arguments.get("num_results", 3)
        
        # Simple keyword matching
        results = []
        for doc in self.documentation:
            if any(word in doc["title"].lower() or word in doc["content"].lower() 
                   for word in query.split() if len(word) > 3):
                results.append(doc)
        
        # Limit results
        results = results[:num_results]
        
        if not results:
            results = self.documentation[:num_results]  # Return first N as fallback
        
        # Format response
        output = f"📚 **Found {len(results)} relevant documents:**\n\n"
        for i, doc in enumerate(results, 1):
            output += f"**{i}. {doc['title']}** ({doc['category']})\n"
            output += f"{doc['content'][:150]}...\n\n"
        
        return output
    
    def _mock_uc_function(self, arguments: Dict) -> str:
        """Mock Unity Catalog Function execution"""
        # Mock calculate_discount function
        amount = arguments.get("order_amount", 0)
        segment = arguments.get("customer_segment", "SMB")
        
        # Calculate discount based on segment
        if segment == "Enterprise":
            discount_pct = 15
        elif segment == "Mid-Market":
            discount_pct = 10
        else:
            discount_pct = 5
        
        discount_amount = amount * (discount_pct / 100)
        
        return f"""💰 **Discount Calculation Result**

• Order Amount: ${amount:,.2f}
• Customer Segment: {segment}
• Discount Rate: {discount_pct}%
• Discount Amount: ${discount_amount:,.2f}
• Final Price: ${amount - discount_amount:,.2f}

**Function:** `demo_retail.ecommerce.calculate_discount`
**Executed by:** Mock MCP Server"""
    
    # Convenience methods (same as UniversalMCPClient)
    
    async def ask_genie(self, space_id: str, question: str, conversation_id: str = None):
        """Mock Genie query"""
        response = await self.query("mock/genie/", "ask_question", {"question": question})
        return response, f"mock-conv-{hash(question)}"
    
    async def search_docs(self, index_id: str, query: str, num_results: int = 3):
        """Mock Vector Search"""
        # Extract catalog.schema from index_id for URL matching
        return await self.query("mock/vector-search/", "similarity_search", 
                               {"query": query, "num_results": num_results})
    
    async def call_function(self, function_name: str, parameters: Dict[str, Any]):
        """Mock UC Function"""
        # Updated URL pattern: /mcp/functions/ instead of /mcp/uc-functions/
        return await self.query("mock/functions/", "execute", parameters)

