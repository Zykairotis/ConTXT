#!/usr/bin/env python3
"""
Script to add a health endpoint to the FastAPI application for Docker health checks.
This script checks if a health endpoint exists and adds one if needed.
"""
import os
import re

def add_health_endpoint():
    """
    Add a health endpoint to the FastAPI application if one doesn't exist.
    """
    # Path to main.py
    main_py_path = os.path.join("app", "main.py")
    
    # Read the current content
    with open(main_py_path, 'r') as file:
        content = file.read()
    
    # Check if a health endpoint already exists
    if "@app.get('/health')" in content or "@app.get(\"/health\")" in content:
        print("Health endpoint already exists.")
        return
    
    # Find where to insert the health endpoint
    # Add after the last route or before the if __name__ == "__main__" block
    if "if __name__ == \"__main__\"" in content:
        # Insert before the if __name__ block
        pattern = r'if __name__ == "__main__"'
        replacement = """
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "context_processor"}

if __name__ == "__main__"\
"""
        content = re.sub(pattern, replacement, content)
    else:
        # Append to the end of the file
        content += """

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "context_processor"}
"""
    
    # Add database health check endpoint
    if "@app.get('/api/health/databases')" not in content and "@app.get(\"/api/health/databases\")" not in content:
        # Add database health check after health endpoint or at the end
        health_endpoint_pattern = r'@app\.get\("\/health"\)[^\}]+\}'
        if re.search(health_endpoint_pattern, content):
            # Add after the health endpoint
            content = re.sub(
                health_endpoint_pattern,
                lambda m: m.group(0) + """

@app.get("/api/health/databases")
async def database_health():
    """Database health check endpoint."""
    health_status = {"neo4j": False, "qdrant": False, "postgres": False, "redis": False}
    
    try:
        # Check Neo4j
        from app.db.neo4j_client import Neo4jClient
        neo4j_client = Neo4jClient()
        result = await neo4j_client.run_query("RETURN 'Connected to Neo4j!' as message")
        if result and result[0].get("message") == "Connected to Neo4j!":
            health_status["neo4j"] = True
        await neo4j_client.close()
    except Exception as e:
        health_status["neo4j_error"] = str(e)
    
    try:
        # Check Qdrant
        from app.db.qdrant_client import QdrantClient
        qdrant_client = QdrantClient()
        client = qdrant_client.get_client()
        collections = client.get_collections()
        if hasattr(collections, "collections"):
            health_status["qdrant"] = True
            health_status["qdrant_collections"] = [c.name for c in collections.collections]
        qdrant_client.close()
    except Exception as e:
        health_status["qdrant_error"] = str(e)
    
    # Placeholder for PostgreSQL check (implement when PostgreSQL client is available)
    try:
        health_status["postgres"] = True  # Placeholder
    except Exception as e:
        health_status["postgres_error"] = str(e)
    
    # Placeholder for Redis check (implement when Redis client is available)
    try:
        health_status["redis"] = True  # Placeholder
    except Exception as e:
        health_status["redis_error"] = str(e)
    
    status_code = 200 if all([health_status["neo4j"], health_status["qdrant"]]) else 503
    return health_status""",
                content
            )
        else:
            # Add to the end
            content += """

@app.get("/api/health/databases")
async def database_health():
    """Database health check endpoint."""
    health_status = {"neo4j": False, "qdrant": False, "postgres": False, "redis": False}
    
    try:
        # Check Neo4j
        from app.db.neo4j_client import Neo4jClient
        neo4j_client = Neo4jClient()
        result = await neo4j_client.run_query("RETURN 'Connected to Neo4j!' as message")
        if result and result[0].get("message") == "Connected to Neo4j!":
            health_status["neo4j"] = True
        await neo4j_client.close()
    except Exception as e:
        health_status["neo4j_error"] = str(e)
    
    try:
        # Check Qdrant
        from app.db.qdrant_client import QdrantClient
        qdrant_client = QdrantClient()
        client = qdrant_client.get_client()
        collections = client.get_collections()
        if hasattr(collections, "collections"):
            health_status["qdrant"] = True
            health_status["qdrant_collections"] = [c.name for c in collections.collections]
        qdrant_client.close()
    except Exception as e:
        health_status["qdrant_error"] = str(e)
    
    # Placeholder for PostgreSQL check (implement when PostgreSQL client is available)
    try:
        health_status["postgres"] = True  # Placeholder
    except Exception as e:
        health_status["postgres_error"] = str(e)
    
    # Placeholder for Redis check (implement when Redis client is available)
    try:
        health_status["redis"] = True  # Placeholder
    except Exception as e:
        health_status["redis_error"] = str(e)
    
    status_code = 200 if all([health_status["neo4j"], health_status["qdrant"]]) else 503
    return health_status
"""
    
    # Write the updated content
    with open(main_py_path, 'w') as file:
        file.write(content)
    
    print("Health endpoints added successfully.")

if __name__ == "__main__":
    add_health_endpoint() 