from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Backend import back
import os
import groq

app = FastAPI()

class QuesReceive(BaseModel):
    question: str
    source: bool = False

# 1) Chat endpoint
@app.post('/chat')
def ask_question(req: QuesReceive):
    try:
        qa_chain = back.get_chain()
        result = qa_chain.invoke({"question": req.question})

        sources = []
        if req.source:
            for doc in result["source_documents"]:
                sources.append({
                    "source": doc.metadata.get("source", "Unknown Source"),
                    "page": doc.metadata.get("page", "Unknown Page")
                })

        return {"answer": result["answer"], "sources": sources}

    except groq.AuthenticationError:
        raise HTTPException(status_code=401, detail="❌ Invalid API Key")

    except groq.APIConnectionError:
        raise HTTPException(status_code=502, detail="⚠️ Failed to connect to Groq API")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# 2) API key setter endpoint
class KeyReceive(BaseModel):
    api_key: str

@app.post('/set_key')
def set_key(req: KeyReceive):
    with open(".env", "w") as f:
        f.write(f"GROQ_API_KEY={req.api_key}\n")
    os.environ["GROQ_API_KEY"] = req.api_key
    return {"api_status": "✅ API key saved and loaded!"}
