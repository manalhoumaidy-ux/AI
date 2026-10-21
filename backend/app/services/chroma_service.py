"""
LanceDB service for local vector storage - No API keys needed!
Replaces ChromaDB with LanceDB (no C++ compilation required on Windows)
"""
import lancedb
from typing import List, Dict, Optional
from app.core.config import settings
import os
import pyarrow as pa


class VectorService:
    """
    Service for LanceDB - Local vector database.
    No API keys, no cloud dependencies, no C++ compilation!
    """

    def __init__(self):
        self.db_path = settings.CHROMA_PERSIST_DIR  # Reusing the config variable
        self.table_name = "bias_detector_docs"
        self.db = None
        self.table = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of LanceDB"""
        if self._initialized:
            return

        # Ensure directory exists
        os.makedirs(self.db_path, exist_ok=True)

        # Connect to LanceDB
        self.db = lancedb.connect(self.db_path)

        # Check if table exists
        existing_tables = self.db.table_names()
        if self.table_name in existing_tables:
            self.table = self.db.open_table(self.table_name)
        else:
            self.table = None

        self._initialized = True

    def _create_table_if_needed(self, embedding_dim: int):
        """Create table with proper schema if it doesn't exist"""
        if self.table is not None:
            return

        # Create empty table with schema
        schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("text", pa.string()),
            pa.field("document_id", pa.string()),
            pa.field("filename", pa.string()),
            pa.field("chunk_index", pa.int32()),
            pa.field("vector", pa.list_(pa.float32(), embedding_dim))
        ])

        self.table = self.db.create_table(self.table_name, schema=schema)

    async def upsert_document(
        self,
        document_id: str,
        text_chunks: List[str],
        embeddings: List[List[float]],
        metadata: Dict
    ) -> bool:
        """
        Store document chunks with their embeddings

        Args:
            document_id: Unique identifier for the document
            text_chunks: List of text chunks from the document
            embeddings: List of embedding vectors
            metadata: Metadata about the document

        Returns:
            True if successful
        """
        try:
            self._ensure_initialized()

            if not embeddings:
                return True

            embedding_dim = len(embeddings[0])
            self._create_table_if_needed(embedding_dim)

            # First, delete existing chunks for this document
            await self.delete_document(document_id)

            # Prepare data for insertion
            data = []
            for i, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
                chunk_id = f"{document_id}_chunk_{i}"
                data.append({
                    "id": chunk_id,
                    "text": chunk,
                    "document_id": document_id,
                    "filename": metadata.get("filename", ""),
                    "chunk_index": i,
                    "vector": embedding
                })

            # Add to LanceDB
            if data:
                self.table.add(data)

            return True

        except Exception as e:
            raise Exception(f"Error upserting document to LanceDB: {str(e)}")

    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Perform semantic search using query embedding

        Args:
            query_embedding: Embedding vector of the search query
            top_k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of search results with scores and metadata
        """
        try:
            self._ensure_initialized()

            if self.table is None:
                return []

            # Build the search query
            query = self.table.search(query_embedding).limit(top_k)

            # Apply filter if provided
            if filter and "document_id" in filter:
                query = query.where(f"document_id = '{filter['document_id']}'")

            results = query.to_pandas()

            # Convert to standard format
            search_results = []
            for _, row in results.iterrows():
                # LanceDB returns _distance, convert to similarity
                distance = row.get('_distance', 0)
                similarity = 1 / (1 + distance)

                search_results.append({
                    "id": row['id'],
                    "score": similarity,
                    "metadata": {
                        "text": row['text'],
                        "document_id": row['document_id'],
                        "filename": row['filename'],
                        "chunk_index": row['chunk_index']
                    }
                })

            return search_results

        except Exception as e:
            raise Exception(f"Error searching in LanceDB: {str(e)}")

    async def get_document_chunks(self, document_id: str) -> List[Dict]:
        """Retrieve all chunks for a specific document"""
        try:
            self._ensure_initialized()

            if self.table is None:
                return []

            results = self.table.search().where(f"document_id = '{document_id}'").to_pandas()

            chunks = []
            for _, row in results.iterrows():
                chunks.append({
                    "id": row['id'],
                    "metadata": {
                        "text": row['text'],
                        "document_id": row['document_id'],
                        "filename": row['filename'],
                        "chunk_index": row['chunk_index']
                    }
                })

            return chunks

        except Exception as e:
            raise Exception(f"Error retrieving document chunks: {str(e)}")

    async def delete_document(self, document_id: str) -> bool:
        """Delete all vectors associated with a document"""
        try:
            self._ensure_initialized()

            if self.table is None:
                return True

            # LanceDB delete with filter
            self.table.delete(f"document_id = '{document_id}'")

            return True

        except Exception as e:
            # If delete fails (e.g., no matching rows), that's okay
            return True

    async def get_stats(self) -> Dict:
        """Get collection statistics"""
        try:
            self._ensure_initialized()

            if self.table is None:
                return {
                    "total_vectors": 0,
                    "table_name": self.table_name,
                    "db_path": self.db_path
                }

            count = self.table.count_rows()
            return {
                "total_vectors": count,
                "table_name": self.table_name,
                "db_path": self.db_path
            }
        except Exception as e:
            return {
                "total_vectors": 0,
                "table_name": self.table_name,
                "db_path": self.db_path,
                "error": str(e)
            }

    async def reset(self) -> bool:
        """Reset the table (delete all data)"""
        try:
            self._ensure_initialized()

            if self.table_name in self.db.table_names():
                self.db.drop_table(self.table_name)

            self.table = None
            return True
        except Exception as e:
            raise Exception(f"Error resetting LanceDB: {str(e)}")


# Singleton instance - keep the name for compatibility
chroma_service = VectorService()
