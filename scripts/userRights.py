# Using functional programing create a way to access User.rights        
# SQL Schema: Users -> Roles -> RolesRightsGroups -> RightsGroups -> RightsGroupsRights -> Rights


from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import backref

Base = declarative_base()

#User.rights_groups -> RightsGroup.rights -> Rights.name
user_rights_table = Table('user_rights', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('rights_group_id', Integer, ForeignKey('rights_groups.id'))
)

#RightsGroup.rights -> Rights.name
rights_group_rights_table = Table('rights_group_rights', Base.metadata,
    Column('rights_group_id', Integer, ForeignKey('rights_groups.id')),
    Column('rights_id', Integer, ForeignKey('rights.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rights_groups = relationship("RightsGroup", secondary=user_rights_table, backref="users")

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

class RightsGroup(Base):
    __tablename__ = 'rights_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rights = relationship("Rights", secondary=rights_group_rights_table, backref="rights_groups")

    def __repr__(self):
        return "<RightsGroup(name='%s')>" % (self.name)

class Rights(Base):
    __tablename__ = 'rights'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Rights(name='%s')>" % (self.name)

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(name='user1')
user2 = User(name='user2')
user3 = User(name='user3')

rights_group1 = RightsGroup(name='rights_group1')
rights_group2 = RightsGroup(name='rights_group2')
rights_group3 = RightsGroup(name='rights_group3')

right1 = Rights(name='right1')
right2 = Rights(name='right2')
right3 = Rights(name='right3')

rights_group1.rights.append(right1)
rights_group1.rights.append(right2)
rights_group2.rights.append(right2)
rights_group2.rights.append(right3)

user1.rights_groups.append(rights_group1)
user1.rights_groups.append(rights_group2)
user2.rights_groups.append(rights_group1)
user2.rights_groups.append(rights_group2)
user3.rights_groups.append(rights_group2)
user3.rights_groups.append(rights_group3)

session.add(user1)
session.add(user2)
session.add(user3)
session.add(rights_group1)
session.add(rights_group2)
session.add(rights_group3)
session.add(right1)
session.add(right2)
session.add(right3)
session.commit()

# Show print all rights

#print(session.query(User).filter(User.rights_groups.any(RightsGroup.rights.any(Rights.name == 'right1'))).all())