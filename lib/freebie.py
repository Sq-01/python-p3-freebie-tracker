from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    # Relationship between Company and Freebie
    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary="devs_companies")
    
    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    # Relationship between Dev and Freebie
    freebies = relationship("Freebie", backref="dev")
    companies = relationship("Company", secondary="devs_companies")
    
    def __repr__(self):
        return f'<Dev {self.name}>'    

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    
    # Foreign keys for Dev and Company
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
