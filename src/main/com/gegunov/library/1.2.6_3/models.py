from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# Модель для таблицы категорий
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Связь с товарами
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"


# Модель для таблицы поставщиков
class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(Text)

    # Связь с поставками
    shipments = relationship("Shipment", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name})>"


# Модель для таблицы товаров
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))

    # Связи
    category = relationship("Category", back_populates="products")
    transactions = relationship("Transaction", back_populates="product")
    shipment_items = relationship("ShipmentItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, quantity={self.quantity}, price={self.price})>"


# Модель для таблицы транзакций
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    change = Column(Integer, nullable=False)
    transaction_type = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    # Связь с товаром
    product = relationship("Product", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, product_id={self.product_id}, change={self.change}, type={self.transaction_type})>"


# Модель для таблицы поставок
class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    shipment_date = Column(TIMESTAMP, default=datetime.now)

    # Связи
    supplier = relationship("Supplier", back_populates="shipments")
    shipment_items = relationship("ShipmentItem", back_populates="shipment")

    def __repr__(self):
        return f"<Shipment(id={self.id}, supplier_id={self.supplier_id}, date={self.shipment_date})>"


# Модель для таблицы связей товаров с поставками
class ShipmentItem(Base):
    __tablename__ = 'shipment_items'

    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    # Связи
    shipment = relationship("Shipment", back_populates="shipment_items")
    product = relationship("Product", back_populates="shipment_items")

    def __repr__(self):
        return f"<ShipmentItem(id={self.id}, shipment_id={self.shipment_id}, product_id={self.product_id}, quantity={self.quantity})>"
