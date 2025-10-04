# from fastapi import FastAPI #pip install fastapi
# import pydantic
# from pydantic import BaseModel
# from back import qa_chain
# import os

# app=FastAPI()

# class QuesReceive(BaseModel):
#     api_key : str
#     question :str
#     source : bool

# @app.post('/chat')
# def ask__question(req:QuesReceive):
#     result = qa_chain.invoke({"question": req.question})
#     if req.source:
#         for doc in result["source_documents"]:
#             src = doc.metadata.get("source", "Unknown Source")
#             page = doc.metadata.get("page", "Unknown Page")
#     else:
#         src=None
#         page=None        
#     return {"answer" : result["answer"],"Source" : src, "Page": page}

# #following code doesnt work bcz we would have to invoke LLM second time for one single question so, we included this code in above function
# # @app.post('/chat')
# # def give_sources(req:QuesReceive):
# #     result = qa_chain.invoke({"question": req.question})
# #     for doc in result["source_documents"]:
# #         src = doc.metadata.get("source", "Unknown Source")
# #         page = doc.metadata.get("page", "Unknown Page")
# #         #print(f"Source: {source}, Page: {page}")

# #     return {"Source" : {src}, "Page": {page}}  #This will only return the laatest src and page , so one solution is that we can store all srcs and pages in a list


# @app.post('/chat')
# def set_key(req:QuesReceive):
#     key=qa_chain.invoke({'api_key' : req.api_key})

#     with open(".env", "w") as f:
#         f.write(f"GROQ_API_KEY={req.api_key}\n")

#     # Update environment variable for current session
#     os.environ["GROQ_API_KEY"] = req.api_key
#     return {"api_status" : "✅ API key saved and loaded!"}

# I made seperate classes for key and (question,source bool) because they are to be executed seperately, first I Load the API key , it will show that its loaded and then we send source bool and str question which is seperate from API key sending .For same reason, we divided the classes bcz I wanna run them at different endpoints bcz If I wanna send all of them from same endpoint and class, I have to send them simultaneously, not the API first which doesnt happen in frontend. For same reason, I didnt make payload for the backend 

# Following code doessnt work fine as well

# from fastapi import FastAPI
# from pydantic import BaseModel
# from Backend.back import qa_chain
# import os

# app = FastAPI()

# class QuesReceive(BaseModel):
#     question: str
#     source: bool = False


# # 1) Chat endpoint
# @app.post('/chat')
# def ask_question(req: QuesReceive):
#     result = qa_chain.invoke({"question": req.question})

#     sources = []
#     if req.source:
#         for doc in result["source_documents"]:
#             sources.append({
#                 "source": doc.metadata.get("source", "Unknown Source"),
#                 "page": doc.metadata.get("page", "Unknown Page")
#             })

#     return {
#         "answer": result["answer"],
#         "sources": sources
#     }


# # 2) API key setter endpoint
# class KeyReceive(BaseModel):
#     api_key: str

# @app.post('/set_key')
# def set_key(req: KeyReceive):
#     with open(".env", "w") as f:
#         f.write(f"GROQ_API_KEY={req.api_key}\n")
#     os.environ["GROQ_API_KEY"] = req.api_key
#     return {"api_status": "✅ API key saved and loaded!"}


# # uvicorn Backend.backend:app --reload --port 8000


#Following works as I have made function in back.py which will make LLM everytime endpoint is hit with new API key (not bubble at same API key if backend stuck at an error)

from fastapi import FastAPI
from pydantic import BaseModel
from Backend import back
import os

app = FastAPI()

class QuesReceive(BaseModel):
    question: str
    source: bool = False


# 1) Chat endpoint
@app.post('/chat')
def ask_question(req: QuesReceive):
    qa_chain=back.get_chain()
    result = qa_chain.invoke({"question": req.question})

    sources = []
    if req.source:
        for doc in result["source_documents"]:
            sources.append({
                "source": doc.metadata.get("source", "Unknown Source"),
                "page": doc.metadata.get("page", "Unknown Page")
            })

    return {
        "answer": result["answer"],
        "sources": sources
    }


# 2) API key setter endpoint
class KeyReceive(BaseModel):
    api_key: str

@app.post('/set_key')
def set_key(req: KeyReceive):
    with open(".env", "w") as f:
        f.write(f"GROQ_API_KEY={req.api_key}\n")
    os.environ["GROQ_API_KEY"] = req.api_key
    return {"api_status": "✅ API key saved and loaded!"}


# uvicorn Backend.backend:app --reload --port 8000