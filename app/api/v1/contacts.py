from fastapi import APIRouter, Depends,HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from core.database import get_db
from schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from models.contact import ContactModel

router = APIRouter()

@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_data: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = ContactModel(**contact_data.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

@router.get('/', response_model=dict)
async def list_contacts(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        search: Optional[str] = Query(None, description = 'Поиск по имени, ИНН, номеру телефона'),
        db: AsyncSession = Depends(get_db),
):
    query = select(ContactModel).offset(skip).limit(limit).order_by(ContactModel.created_at.desc())

    if search:
        term = f'%{search}%'
        query = query.where(
            ContactModel.company_name.ilike(term)|
            ContactModel.inn.ilike(term)|
            ContactModel.phone.ilike(term)
        )

    count_query = select(func.count()).select_from(ContactModel)
    if search:
        count_query = count_query.where(
            ContactModel.company_name.ilike(term)|
            ContactModel.inn.ilike(term)|
            ContactModel.phone.ilike(term)
        )

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query)
    contacts = result.scalars().all()
    items = [ContactResponse.model_validate(c) for c in contacts]

    return {
        'items' : items,
        'total' : total,
        'page' : skip//limit+1 if limit else 1,
        'pages' : (total+limit-1)//limit if limit else 1,
    }

@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail='Контакт не найден')
    return contact

@router.patch('/{contact_id}', response_model=ContactResponse)
async def update_contact(
        contact_id: int,
        contact_data: ContactUpdate,
        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail='Контакт не найден')
    for field, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    await db.commit()
    await db.refresh(contact)
    return contact

@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactModel).where(ContactModel.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail='Контакт не найден')

    await db.delete(contact)
    await db.commit()
    return None
