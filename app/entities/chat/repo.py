from typing import List, Optional
from app.db.models import Chat
from app.db.main import db_session
from app.entities.chat.schema import ChatCreate, ChatUpdate, ChatResponse
from sqlmodel import select

class ChatRepo:

    async def get_all_chat(self, session: db_session) -> List[ChatResponse]:
        statement = select(Chat)
        result = await session.execute(statement)
        Chat = result.scalars().all()

        return [ChatResponse.model_validate(Chat) for Chat in Chat]
    
    async def get_chat(self, Chat_id: str, session: db_session) -> Optional[ChatResponse]:
        statement = select(Chat).where(Chat.uid == Chat_id)
        result = await session.execute(statement)
        Chat = result.scalars().one_or_none()

        return ChatResponse.model_validate(Chat) if Chat else None

    async def create_chat(self, Chat_data: ChatCreate, session: db_session) -> ChatResponse:
        new_Chat = Chat(**Chat_data.model_dump())
        session.add(new_Chat)
        await session.commit()
        await session.refresh(new_Chat)
        return ChatResponse.model_validate(new_Chat)
    
    async def update_chat(self, Chat_id: str, Chat: ChatUpdate, session: db_session) -> ChatResponse:
        statement = select(Chat).where(Chat.uid == Chat_id)
        result = await session.execute(statement)
        Chat_to_update = result.scalars().one_or_none()

        if not Chat_to_update:
            return None

        for key, value in Chat.model_dump(exclude_unset=True).items():
            setattr(Chat_to_update, key, value) 

        await session.commit()
        await session.refresh(Chat_to_update)
        return ChatResponse.model_validate(Chat_to_update)
    
    async def delete_chat(self, Chat_id: str, session: db_session) -> bool:
        statement = select(Chat).where(Chat.uid == Chat_id)
        result = await session.execute(statement)
        Chat_to_delete= result.scalars().one_or_none()
        if not Chat_to_delete:
            return False
        await session.delete(Chat_to_delete)
        await session.commit()
        return True
    
