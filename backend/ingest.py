import os
import uuid
from typing import List
from datetime import datetime
from markitdown import MarkItDown
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3")
COLLECTION_NAME = "hr_docs"

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL)
embeddings = OllamaEmbeddings(
    base_url=OLLAMA_BASE_URL,
    model=EMBEDDING_MODEL
)
llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=CHAT_MODEL,
    temperature=0
)

class AgenticChunker:
    """
    Decomposes text into standalone propositions using an LLM
    and then groups them into semantically coherent chunks with identified titles.
    """
    def __init__(self, llm: ChatOllama):
        self.llm = llm
        self.extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at decomposing complex text into standalone propositions. "
                       "Decompose the given text into a list of independent, factual propositions. "
                       "Each proposition MUST be a complete, standalone sentence that is understandable without its original context. "
                       "Include relevant subjects and entities in every sentence. "
                       "Respond with a bulleted list of propositions ONLY."),
            ("human", "{input}")
        ])
        self.titling_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at summarizing content. Given a list of propositions, "
                       "provide a concise, descriptive title (3-7 words) that represents the main topic. "
                       "Respond with the title ONLY, no quotes or preamble."),
            ("human", "{propositions}")
        ])

    def _get_propositions(self, text: str) -> List[str]:
        chain = self.extraction_prompt | self.llm
        try:
            response = chain.invoke({"input": text})
            lines = response.content.split("\n")
            return [line.strip("- *").strip() for line in lines if line.strip()]
        except Exception as e:
            print(f"Error extracting propositions: {e}")
            return [text]

    def _get_title(self, propositions: List[str]) -> str:
        chain = self.titling_prompt | self.llm
        try:
            props_text = "\n".join(propositions[:10])
            response = chain.invoke({"propositions": props_text})
            title = response.content.split("\n")[0].strip("\"' ")
            return title if title else "Untitled Section"
        except Exception as e:
            print(f"Error generating title: {e}")
            return "Untitled Section"

    def split_documents(self, documents: List[Document]) -> List[Document]:
        final_chunks = []
        
        for doc in documents:
            initial_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
            initial_docs = initial_splitter.split_documents([doc])
            
            all_propositions = []
            for idoc in initial_docs:
                all_propositions.extend(self._get_propositions(idoc.page_content))
            
            unique_propositions = []
            seen_props = set()
            for prop in all_propositions:
                clean_prop = prop.strip().lower()
                if clean_prop not in seen_props:
                    unique_propositions.append(prop)
                    seen_props.add(clean_prop)
            
            current_group = []
            current_len = 0
            
            for prop in unique_propositions:
                # Target chunk size ~1800 chars for better context
                if current_len + len(prop) < 1800:
                    current_group.append(prop)
                    current_len += len(prop)
                else:
                    if current_group:
                        section_title = self._get_title(current_group)
                        new_metadata = doc.metadata.copy()
                        new_metadata["section_title"] = section_title
                        # Inject section title into content for better retrieval grounding
                        content = f"Section: {section_title}\n" + " ".join(current_group)
                        final_chunks.append(Document(
                            page_content=content,
                            metadata=new_metadata
                        ))
                    current_group = [prop]
                    current_len = len(prop)
            
            if current_group:
                section_title = self._get_title(current_group)
                new_metadata = doc.metadata.copy()
                new_metadata["section_title"] = section_title
                content = f"Section: {section_title}\n" + " ".join(current_group)
                final_chunks.append(Document(
                    page_content=content,
                    metadata=new_metadata
                ))
        
        return final_chunks

def get_vector_store():
    ensure_collection_exists()
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

def ensure_collection_exists():
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        # nomic-embed-text uses 768 dimensions
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

def process_and_index_file(file_path: str, filename: str) -> str:
    """
    Parses a file using MarkItDown, chunks it using Agentic Chunking, and indexes it into Qdrant.
    Returns the file_id.
    """
    ensure_collection_exists()
    
    file_id = str(uuid.uuid4())
    upload_date = datetime.now().isoformat()
    
    # 1. Parse using MarkItDown
    md = MarkItDown()
    result = md.convert(file_path)
    markdown_content = result.text_content
    
    # Create a LangChain Document from the markdown content
    docs = [Document(page_content=markdown_content, metadata={"source": filename})]
    
    # 2. Agentic Chunking
    chunker = AgenticChunker(llm)
    chunks = chunker.split_documents(docs)
    
    # 3. Add Metadata
    for chunk in chunks:
        chunk.metadata["file_id"] = file_id
        chunk.metadata["filename"] = filename
        chunk.metadata["upload_date"] = upload_date
        
    # 4. Index
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    
    return file_id

def delete_file_from_index(file_id: str):
    """
    Deletes all vectors associated with a specific file_id.
    """
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.file_id",
                        match=models.MatchValue(value=file_id),
                    )
                ]
            )
        ),
    )
