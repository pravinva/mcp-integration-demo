-- ============================================================================
-- Vector Search Mock Data - Documentation Corpus
-- Creates searchable documentation for RAG demonstrations
-- ============================================================================

USE CATALOG demo_retail;
USE SCHEMA ecommerce;

-- ============================================================================
-- Documentation table for Vector Search
-- ============================================================================
CREATE OR REPLACE TABLE documentation (
    doc_id STRING,
    title STRING,
    content STRING,
    category STRING,
    tags ARRAY<STRING>,
    last_updated DATE,
    views INT,
    helpful_votes INT
) COMMENT 'Documentation corpus for Vector Search demonstrations. Includes guides, tutorials, and reference material.';

-- Insert comprehensive documentation
INSERT INTO documentation VALUES
('doc_001', 
 'Getting Started with Databricks Genie',
 'Databricks Genie is an AI-powered analytics assistant that lets you ask questions about your data in natural language. To get started: 1) Create a Genie Space in the SQL workspace, 2) Connect your tables from Unity Catalog, 3) Provide context by adding descriptions to tables and columns, 4) Start asking questions like "What was revenue last quarter?" Genie uses large language models to understand your questions, generate SQL queries, and return insights with explanations. It maintains conversation context, so you can ask follow-up questions naturally. Best practices: Add rich metadata to your tables, include example questions in your space instructions, and regularly review query logs to improve space performance.',
 'Tutorial',
 ARRAY('genie', 'getting-started', 'ai-bi', 'analytics'),
 '2024-11-01',
 1250,
 342
),

('doc_002',
 'Model Context Protocol (MCP) Overview',
 'Model Context Protocol (MCP) is an open standard for connecting AI applications to data sources. Instead of building M×N custom integrations (M agents × N data sources), MCP provides a universal protocol that collapses complexity to M+N. Key benefits: standardized communication between AI apps and data, protocol-level abstraction protects from API changes, works with any MCP-compatible client (Claude, custom apps), automatic tool discovery. MCP servers expose tools (like ask_question for Genie, similarity_search for Vector Search) that clients can discover and call using a standard format. This enables building once and deploying everywhere - the same integration code works for Teams, Slack, web apps, and CLI tools.',
 'Concepts',
 ARRAY('mcp', 'integration', 'architecture', 'protocol'),
 '2024-10-15',
 2100,
 487
),

('doc_003',
 'Unity Catalog Functions - Creating Custom Functions',
 'Unity Catalog Functions let you register Python, SQL, or Scala functions that can be called across your workspace with governed access control. Creating a Python function example: CREATE FUNCTION calculate_discount(price DOUBLE, customer_segment STRING) RETURNS DOUBLE LANGUAGE PYTHON AS $$ if customer_segment == "Enterprise": return price * 0.15 elif customer_segment == "Mid-Market": return price * 0.10 else: return price * 0.05 $$. Functions are governed by Unity Catalog, so you can control who can execute them with standard GRANT/REVOKE statements. Benefits: Centralized business logic, version control, access governance, reusable across SQL, Python, and Scala workloads. Use cases: Complex calculations, data transformations, ML model scoring, business rule enforcement.',
 'How-To',
 ARRAY('unity-catalog', 'functions', 'python', 'governance'),
 '2024-10-20',
 890,
 256
),

('doc_004',
 'Vector Search for RAG Applications',
 'Databricks Vector Search enables similarity search for Retrieval Augmented Generation (RAG) applications. Setup process: 1) Create an embedding table with your documents and metadata, 2) Create a vector search index specifying the embedding column, 3) Query using natural language or pre-computed embeddings. Example query: results = index.similarity_search(query_text="How do I create a Genie space?", num_results=5). Vector Search automatically handles embedding generation using state-of-the-art models, manages index updates incrementally, scales to billions of vectors, and integrates with Unity Catalog for access control. Common use cases: Documentation search, customer support knowledge bases, semantic code search, product recommendations, content discovery.',
 'How-To',
 ARRAY('vector-search', 'rag', 'embeddings', 'ai'),
 '2024-11-05',
 1567,
 423
),

('doc_005',
 'Deploying Databricks Apps',
 'Databricks Apps let you deploy web applications, APIs, and bots directly on Databricks infrastructure without managing external servers. Deployment steps: 1) Create app.yaml configuration file with command, resources (CPU, memory), and environment variables, 2) Define secrets using Databricks secret scopes, 3) Deploy using databricks apps deploy my-app. Apps get automatic scaling based on load, built-in monitoring and logging, integration with Unity Catalog for authentication, and zero-downtime deployments. Perfect for hosting Slack bots (Socket Mode), REST APIs, web UIs with Streamlit, scheduled jobs, and ML model serving endpoints. Apps run on serverless compute with pay-per-use pricing.',
 'Tutorial',
 ARRAY('apps', 'deployment', 'infrastructure', 'serverless'),
 '2024-10-28',
 945,
 289
),

('doc_006',
 'OAuth Authentication for MCP Servers',
 'Secure your MCP server connections with OAuth 2.0 authentication for per-user access control. Setup in Account Console: 1) Navigate to Settings → App Connections → Add connection, 2) Configure OAuth application with redirect URLs, 3) Select required scopes (e.g., SQL, Genie, Vector Search), 4) Generate client ID and secret, 5) Set token expiration policies. Use OAuth credentials in your MCP client: WorkspaceClient(host=host, client_id=oauth_client_id, client_secret=oauth_client_secret). OAuth ensures per-user authentication (not shared service principals), automatic token refresh, Unity Catalog permission enforcement per actual user, complete audit trail showing which human made which query. Security benefits: Short-lived access tokens (1 hour default), centralized credential management, instant revocation capability, compliance-ready audit logs.',
 'Security',
 ARRAY('oauth', 'authentication', 'security', 'compliance'),
 '2024-10-10',
 1834,
 512
),

('doc_007',
 'Troubleshooting Genie Queries',
 'Common issues when using Genie and how to resolve them. Issue: Genie does not understand my question - Solution: Add comprehensive table and column descriptions in Unity Catalog, provide example queries in Genie Space instructions, use specific table/column names in your questions, avoid ambiguous terms. Issue: Query returns incorrect results - Solution: Check table descriptions match actual data semantics, verify data quality and currency, ask Genie to show the SQL it generated for review, add computed columns or views for complex metrics. Issue: Timeout errors - Solution: Ensure SQL warehouse is running and sized appropriately, check if tables are too large without proper filters, simplify complex questions into smaller parts, consider adding indexes or partitioning. Issue: Missing data - Solution: Verify Unity Catalog permissions, check table refresh schedules, confirm data pipeline health.',
 'Troubleshooting',
 ARRAY('genie', 'debugging', 'help', 'errors'),
 '2024-11-08',
 2345,
 678
),

('doc_008',
 'Best Practices for Genie Spaces',
 'Optimize your Genie Space for better results: 1) Rich Metadata - Add comprehensive descriptions to tables, columns, and views explaining business context and calculation logic. 2) Sample Questions - Include 5-10 example questions in space instructions showing query patterns. 3) Data Governance - Document data refresh schedules, SLAs, and known limitations. 4) Table Selection - Only include relevant tables (not entire catalog) to reduce complexity. 5) Business Context - Explain how key metrics are calculated, what constitutes "revenue" vs "bookings", fiscal calendar details. 6) Regular Review - Analyze query logs weekly to identify common patterns and improve instructions. Example good column description: "revenue_usd: Total revenue in US dollars after discounts and returns. Updated daily at 2 AM UTC. Does not include pending orders." Result: 50% improvement in query accuracy, 30% reduction in follow-up questions.',
 'Best Practices',
 ARRAY('genie', 'optimization', 'metadata', 'governance'),
 '2024-10-25',
 1678,
 445
),

('doc_009',
 'Building Slack Bots with Databricks MCP',
 'Create production-ready Slack bots that connect to Databricks Genie, Vector Search, and Unity Catalog Functions using MCP. Architecture: User messages in Slack → Socket Mode WebSocket → Your bot code (Python) → MCP client → Databricks MCP servers → Response back to Slack. Setup steps: 1) Create Slack app at api.slack.com with Socket Mode enabled, 2) Add bot scopes: app_mentions:read, chat:write, im:history, 3) Install app and save tokens (SLACK_BOT_TOKEN, SLACK_APP_TOKEN), 4) Write bot code using slack-bolt library and shared MCP client, 5) Deploy to Databricks Apps with app.yaml. Key code pattern: @app.event("app_mention") async def handle(event, say): response = await mcp_client.ask_genie(space_id, question); await say(response). Benefits: No ngrok needed (Socket Mode), deploys on Databricks (no external servers), automatic scaling, governed data access.',
 'Tutorial',
 ARRAY('slack', 'bots', 'mcp', 'integration'),
 '2024-11-01',
 567,
 189
),

('doc_010',
 'Microsoft Teams Integration with MCP',
 'Build Microsoft Teams bots that provide natural language analytics, documentation search, and function execution via MCP. Architecture: Teams user → Azure Bot Service → Your bot (Azure Functions or App Service) → MCP client → Databricks → Teams response. Setup: 1) Create Azure Bot resource, 2) Create App Registration for authentication, 3) Deploy bot code to Azure Functions (serverless, cost-effective), 4) Configure messaging endpoint, 5) Enable Teams channel, 6) Generate Teams app package for installation. Key code: BotFrameworkAdapter processes Teams messages, MCP client queries Databricks, responses formatted as Teams adaptive cards. Testing: Use Bot Framework Emulator locally before Azure deployment. Production: Azure Functions Consumption Plan costs ~$5/month for typical usage. Security: OAuth for per-user Databricks access, Teams SSO integration possible.',
 'Tutorial',
 ARRAY('teams', 'microsoft', 'mcp', 'azure', 'bots'),
 '2024-10-30',
 423,
 134
),

('doc_011',
 'MCP vs Direct API: When to Use Each',
 'Choosing between Model Context Protocol and direct API integration. Use MCP when: Building multiple agents/platforms (Teams, Slack, web), adding new data sources frequently, want protocol standardization, need future-proof architecture, team has multiple developers. Benefits: 80% code reuse, M+N complexity instead of M×N, automatic API change handling by protocol layer. Use Direct API when: Single platform, single data source, need specific API features not in MCP, rapid prototype with no reuse plans, tight deadline with no architecture time. Direct API advantages: More control, access to latest features immediately, no protocol overhead. Migration path: Start with direct API for MVP, refactor to MCP when adding 2nd platform or data source. Most enterprises should default to MCP for maintainability.',
 'Decision Guide',
 ARRAY('mcp', 'api', 'architecture', 'comparison'),
 '2024-11-03',
 891,
 267
),

('doc_012',
 'Security Best Practices for AI Integrations',
 'Securing AI bot integrations with Databricks: 1) Use OAuth not PATs - OAuth provides per-user authentication, automatic token refresh, and shorter exposure windows (1 hour vs 90 days). 2) Secret Management - Store credentials in Azure KeyVault or AWS Secrets Manager, never commit to git, rotate regularly. 3) Least Privilege - Grant bot OAuth app only required scopes, use Unity Catalog GRANT for table-level access, restrict function execution permissions. 4) Audit Logging - Enable Unity Catalog audit logs, monitor query patterns, alert on anomalies. 5) User Attribution - With OAuth, every query shows actual user identity in logs (not service principal), enables insider threat detection and compliance. 6) Network Security - Use private endpoints where possible, restrict IP ranges, enable TLS 1.2+. ROI: Reduces breach exposure by 99% (1-hour tokens vs 90-day PATs), cuts compliance audit time by 75%.',
 'Security',
 ARRAY('security', 'oauth', 'compliance', 'best-practices'),
 '2024-10-18',
 1234,
 389
);

-- Create vector search index (syntax example - adjust based on your setup)
-- Note: In production, you'd generate actual embeddings using a model
-- For demo purposes, we'll use the documentation table as-is

COMMENT ON TABLE documentation IS 'Documentation corpus with 12 articles covering Genie, MCP, Vector Search, Unity Catalog, deployments, and security. Use for RAG demonstrations and semantic search examples.';

-- Enable Change Data Feed for Vector Search delta sync
ALTER TABLE documentation SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- ============================================================================
-- Sample queries for testing
-- ============================================================================

-- Full-text search simulation (in production, use actual vector search)
SELECT 
    doc_id,
    title,
    category,
    tags,
    views,
    helpful_votes
FROM documentation
WHERE 
    LOWER(content) LIKE '%mcp%'
    OR LOWER(title) LIKE '%mcp%'
ORDER BY helpful_votes DESC;

-- Most helpful documentation
SELECT 
    title,
    category,
    views,
    helpful_votes,
    ROUND(100.0 * helpful_votes / views, 1) as helpfulness_rate
FROM documentation
ORDER BY helpful_votes DESC
LIMIT 5;

-- Documentation by category
SELECT 
    category,
    COUNT(*) as doc_count,
    SUM(views) as total_views,
    AVG(helpful_votes) as avg_helpful_votes
FROM documentation
GROUP BY category
ORDER BY total_views DESC;

SELECT '✅ Vector Search mock data created!' as status,
       'Table: demo_retail.ecommerce.documentation' as location,
       '12 comprehensive documents' as summary;

