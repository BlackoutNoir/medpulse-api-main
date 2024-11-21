from typing import List, Optional
from app.db.models import Chat
from app.db.main import db_session
from app.entities.chat.schema import ChatResponse, ChatCreate, ChatUpdate, ChatFilter 
from sqlmodel import select, and_


class ChatRepo:

    async def get_all_chats(self, session: db_session) -> List[ChatResponse]:
        statement = select(Chat)
        result = await session.execute(statement)
        chats = result.scalars().all()

        return [ChatResponse.model_validate(chat) for chat in chats]
    
    async def get_chat(self, chat_id: str, session: db_session) -> Optional[ChatResponse]:
        statement = select(Chat).where(Chat.uid == chat_id)
        result = await session.execute(statement)
        chat = result.scalars().one_or_none()

        return ChatResponse.model_validate(chat) if chat else None
    
    async def create_chat(self, chat_data: ChatCreate, session: db_session) -> ChatResponse:
      
        new_chat = Chat(**chat_data.model_dump())
        session.add(new_chat)
        await session.commit()
        await session.refresh(new_chat)

        return ChatResponse.model_validate(new_chat)
    
    async def update_chat(self, chat_id: str, chat: ChatUpdate, session: db_session) -> ChatResponse:
        statement = select(Chat).where(Chat.uid == chat_id)
        result = await session.execute(statement)
        chat_to_update = result.scalars().one_or_none()

        if not chat_to_update:
            return None

        for key, value in chat.model_dump(exclude_unset=True).items():
            setattr(chat_to_update, key, value) 
        

        await session.commit()
        await session.refresh(chat_to_update)
        return ChatResponse.model_validate(chat_to_update)
    
    async def delete_chat(self, chat_id: str, session: db_session) -> bool:
        statement = select(Chat).where(Chat.uid == chat_id)
        result = await session.execute(statement)
        chat_to_delete= result.scalars().one_or_none()
        if not chat_to_delete:
            return False
        await session.delete(chat_to_delete)
        await session.commit()
        return True 
    

    async def filter_chats(self, filters: ChatFilter, session: db_session) -> List[ChatResponse]:

        statement = select(Chat)
        

        partial_match_fields = [
            "uuid","name"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Chat, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Chat, filters.order_by):
            order_column = getattr(Chat, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        chats = result.scalars().all()

        return [ChatResponse.model_validate(chat) for chat in chats]