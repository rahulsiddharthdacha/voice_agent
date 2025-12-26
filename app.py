from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from agent.rag_agent import RAGAgent

app = FastAPI()


#Sample Mock Code for Twilio Voice Webhook Integration 
@app.post("/twilio/voice")
async def twilio_voice(request: Request):
    """
    Twilio Voice Webhook
    """
    form_data = await request.form()
    user_input = form_data.get("SpeechResult")

    response = VoiceResponse()

    if not user_input:
        # Ask the user to speak
        gather = response.gather(
            input="speech",
            action="/twilio/voice",
            timeout=5
        )
        gather.say(
            "Hello. Please tell me your issue with your money transfer."
        )
        return Response(str(response), media_type="application/xml")

    user_text = user_input.strip()
    rag_agent = RAGAgent()
    result = rag_agent.answer(user_text)

    final_answer = result["messages"][-1].content

    response.say(final_answer)
    response.hangup()

    return Response(str(response), media_type="application/xml")
