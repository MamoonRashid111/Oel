from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from secured_graph import secured_graph
from langchain_core.messages import HumanMessage, AIMessage
import uuid

app = FastAPI(title="Medical Assistant API")

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    context: Optional[str] = None
    requires_approval: bool = False

class ApproveRequest(BaseModel):
    thread_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Invoke the graph
        result = secured_graph.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config
        )
        
        # Check if we are at an interrupt point
        snapshot = secured_graph.get_state(config)
        requires_approval = len(snapshot.next) > 0 and "human_reviewer" in snapshot.next
        
        print(f"DEBUG: thread_id={thread_id}, snapshot.next={snapshot.next}, requires_approval={requires_approval}")
        
        last_message = result["messages"][-1].content
        context = result.get("context", "")
        
        return ChatResponse(
            response=last_message,
            thread_id=thread_id,
            context=context,
            requires_approval=requires_approval
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/approve", response_model=ChatResponse)
async def approve(request: ApproveRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        # Resume the graph by passing None as input
        result = secured_graph.invoke(None, config)
        
        last_message = result["messages"][-1].content
        context = result.get("context", "")
        
        return ChatResponse(
            response=last_message,
            thread_id=request.thread_id,
            context=context,
            requires_approval=False
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import StreamingResponse
import json

@app.post("/stream")
async def stream_chat(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    async def event_generator():
        async for chunk in secured_graph.astream(
            {"messages": [HumanMessage(content=request.message)]},
            config,
            stream_mode="updates"
        ):
            # Format as Server-Sent Events (SSE)
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
