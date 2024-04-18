from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Uuid,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatrialStatus(Base):
    __tablename__ = "matrial_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(32), unique=True)

    users = relationship("User", back_populates="matrial_status")


class OccupationStatus(Base):
    __tablename__ = "occupation_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(16), unique=True)

    users = relationship("User", back_populates="occupation_status")


class IncomeStatus(Base):
    __tablename__ = "income_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(16), unique=True)

    users = relationship("User", back_populates="income_status")


class EducationStatus(Base):
    __tablename__ = "education_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(16), unique=True)

    users = relationship("User", back_populates="education_status")


class User(Base):
    __tablename__ = "user"

    id = Column(Uuid, primary_key=True)
    id_matrial_status = Column(Integer, ForeignKey("matrial_status.id"), nullable=False)
    id_occupation_status = Column(
        Integer, ForeignKey("occupation_status.id"), nullable=False
    )
    id_income_status = Column(Integer, ForeignKey("income_status.id"), nullable=False)
    id_education_status = Column(
        Integer, ForeignKey("education_status.id"), nullable=False
    )
    age = Column(Integer)
    family_size = Column(Integer)
    zip_code = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    gender = Column(Boolean)
    output = Column(Boolean)
    feedback = Column(Boolean)

    matrial_status = relationship("MatrialStatus", back_populates="users")
    occupation_status = relationship("OccupationStatus", back_populates="users")
    income_status = relationship("IncomeStatus", back_populates="users")
    education_status = relationship("EducationStatus", back_populates="users")

    orders = relationship("Orders", back_populates="user")


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Uuid, primary_key=True)
    id_user = Column(Uuid, ForeignKey("user.id"), nullable=False)
    creation_date = Column(DateTime)
    message = Column(Text)

    user = relationship("User", back_populates="orders")

    op = relationship("OrderProducts", back_populates="order")


class Products(Base):
    __tablename__ = "products"

    id = Column(Uuid, primary_key=True)
    name = Column(Text)
    description = Column(Text)

    op = relationship("OrderProducts", back_populates="product")


class OrderProducts(Base):
    __tablename__ = "order_products"

    id = Column(Uuid, primary_key=True)
    id_order = Column(Uuid, ForeignKey("orders.id"), nullable=False)
    id_product = Column(Uuid, ForeignKey("products.id"), nullable=False)
    amount = Column(Integer)

    order = relationship("Orders", back_populates="op")
    product = relationship("Products", back_populates="op")
