from agent.rag_agent import RAGAgent
from speech.stt import listen_text
from speech.tts import text_to_speech

#Actual Main File to run the Voice RAG Agent Locally
def main():
    print("🚀 Voice RAG Agent started")

    rag_agent = RAGAgent()

    while True:
        user_text = listen_text() #stt

        if not user_text:
            continue

        print(f"🗣️ User: {user_text}")

        response = rag_agent.answer(user_text)

        print(f"🤖 Agent: {response}")
        text_to_speech(response) #tts

        # End call if deflected
        if "human support agent" in response.lower():
            print("📞 Ending call")
            break


if __name__ == "__main__":
    main()
