from phi.agent import Agent, AgentMemory
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
import os
from phi.vectordb.pgvector import PgVector, SearchType
from phi.vectordb.search import SearchType
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.memory.db.sqlite import SqliteMemoryDb
import re

def define_model():
    model = Groq(id="llama-3.3-70b-versatile")
    model_to_use = os.getenv('PACO_AI_MODEL')
    if model_to_use == 'GPT':
        model = OpenAIChat(id="gpt-4o-mini")
    return model

def get_weby(client_id, propmt, options):
    model = define_model()

    knowledge_base = WebsiteKnowledgeBase(
        urls=options["urls"],
        # Number of links to follow from the seed URLs
        max_depth=3,
        vector_db= PgVector(table_name="websites", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", search_type=SearchType.hybrid),
    )
    
    knowledge_base.load(recreate=False)

    return Agent(
        # Basic config
        model=model,
        show_tool_calls=True,
        debug_mode=True,
        # Training config
        description="You are a helpful assistant that receive web urls, summarize information from the websites, and answer questions about the information found",
        # Knowledge config
        knowledge=knowledge_base,
        search_knowledge=True,
        # Memory config
        storage= SqlAgentStorage(table_name="agent_sessions", db_file="tmp/storage/weby/agent_storage.db"),
        memory=AgentMemory(
            db=SqliteMemoryDb(table_name="agent_memory", db_file="tmp/storage/weby/agent_storage.db"), create_user_memories=True, create_session_summary=True
        ),
        session_id=client_id,
        add_history_to_messages=True,
        num_history_responses=3
    )