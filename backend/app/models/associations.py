from sqlalchemy import Column, Integer, ForeignKey, Table
from ..database import Base

contact_list_association = Table(
    'contact_list_association', 
    Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id')),
    Column('contact_list_id', Integer, ForeignKey('contact_lists.id'))
)