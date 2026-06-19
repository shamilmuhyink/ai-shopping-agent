from langchain_core.tools import tool

from app.clients.embedding_client import embedding_client
from app.core.database import AsyncSessionLocal
from app.repositories.embedding_repo import EmbeddingRepository


@tool
async def search_products(query: str, limit: int = 5) -> str:
    """
    Search the product catalogue for products matching the user's query.
    Use this tool whenever the user asks to find products, asks for recommendations,
    or asks about product availability/prices.
    """
    try:
        # Get query embedding
        query_vector = await embedding_client.embed_query(query)

        # Search using pgvector
        async with AsyncSessionLocal() as session:
            repo = EmbeddingRepository(session)
            products = await repo.search_similar_products(query_vector, limit=limit)

        if not products:
            return "No matching products found in the catalogue."

        response = f"Found {len(products)} relevant products:\n\n"
        for p in products:
            data = p.product_data
            response += f"- ID: {p.product_id}\n"
            response += f"  Name: {data.get('name', 'Unknown')}\n"
            response += f"  Price: ${data.get('price', 'N/A')}\n"
            response += f"  Stock: {data.get('stock', 0)} available\n"
            response += f"  Description: {data.get('description', '')[:200]}...\n\n"

        return response
    except Exception as e:
        return f"Error searching products: {str(e)}"
