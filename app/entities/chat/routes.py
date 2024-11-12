from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.chat.repo import ChatRepo
from app.entities.chat.schema import ChatResponse, ChatCreate, ChatUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Chat_router = APIRouter()
repo = ChatRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Chat_router.get("/", response_model=List[ChatResponse],
                          )
async def get_allchat(session: db_session,   _details: access_token_bearer):
    return await ChatRepo().get_allchat(session)


@Chat_router.get("/{Chat_id}", response_model=ChatResponse)
async def get_chat(Chat_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Chat =  await ChatRepo().get_chat(Chat_id, session)
    if not Chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    
    return Chat

@Chat_router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(Chat: ChatCreate, session: db_session, _details: access_token_bearer):
    return await ChatRepo().create_chat(Chat, session)


@Chat_router.put("/{Chat_id}", response_model=ChatResponse)
async def update_chat(Chat_id: str, Chat: ChatUpdate, session: db_session,  _details: access_token_bearer):    
    Chat = await ChatRepo().get_chat(Chat_id, session)
    
    if not Chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return await ChatRepo().update_chat(Chat_id, Chat, session)


@Chat_router.delete("/{Chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(Chat_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await ChatRepo().delete_chat(Chat_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")  
    return 
