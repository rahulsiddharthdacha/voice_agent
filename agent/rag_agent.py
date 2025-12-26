import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from agent.intent_gate import IntentGate


SYSTEM_PROMPT = """You are a Wise customer support agent.
You may ONLY answer questions related to:
"Where is my money?" for sending money.

STRICT RULES:
- Use ONLY the provided context.
- If the context does NOT clearly answer the question and only use when the context is insufficient.,
  respond EXACTLY with:
  "I'll connect you to a human support agent."
- Do NOT use outside knowledge.

Context:
{context}"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "..", "vectorstore", "wise_faq")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RAGAgent:
    def __init__(self):
        self.intent_gate = IntentGate() #Intent for correct Questions
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        
        self.db = FAISS.load_local(
            VECTORSTORE_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        self.llm = ChatOllama(
            model="llama3",
            temperature=0
        )
    
        self.chat_histories = {}
        

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
      
        self.chain = self._create_chain()
    
    def _create_chain(self): #TODO For Future Scope
        """Create LCEL chain with memory integration"""
       
        base_chain = self.prompt | self.llm
        
        
        chain_with_history = RunnableWithMessageHistory(
            base_chain,
            self._get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )
        
        return chain_with_history
    
    def _get_session_history(self, session_id: str) -> InMemoryChatMessageHistory: #TODO For Future Scope
        """Get or create chat history for a session"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = InMemoryChatMessageHistory()
        return self.chat_histories[session_id]
    
    def answer(self, question: str, session_id: str = "default") -> str:

        if not self.intent_gate.is_supported(question):
            return "I'll connect you to a human support agent."
        
        docs_with_scores = self.db.similarity_search_with_score(
            question,
            k=2
        )
        context = "\n\n".join(
            doc.page_content for doc, _ in docs_with_scores
        )
        
 
        response = self.chain.invoke(
            {
                "context": context,
                "question": question
            },
            config={"configurable": {"session_id": session_id}}
        )
        
        return response.content.strip()
    
    def clear_history(self, session_id: str = "default"): #TODO For Future Scope
        
        if session_id in self.chat_histories:
            self.chat_histories[session_id].clear()
    
    def get_history(self, session_id: str = "default") -> list: #TODO For Future Scope
      
        if session_id in self.chat_histories:
            return self.chat_histories[session_id].messages
        return []


# # Example usage
# if __name__ == "__main__":
#     agent = RAGAgent()
    
#     # Single session conversation
#     print(agent.answer("Where is my money?"))
#     print(agent.answer("Can you clarify that?"))  # Uses history

#     # Clear history when needed
#     agent.clear_history("user_123")