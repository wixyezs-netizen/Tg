from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .models import Base, User, Order, Product
from app.utils.logger import get_logger
from typing import Optional, List, Dict, Any
import uuid
import random
import string

logger = get_logger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_user(self, telegram_id: int, username: str, first_name: str, 
                   language_code: str = "ru", referred_by: Optional[int] = None) -> User:
        """Создание пользователя"""
        db = next(self.get_db())
        try:
            # Генерация уникального реферального кода
            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                language_code=language_code,
                referral_code=referral_code,
                referred_by=referred_by
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Создан пользователь: {telegram_id}")
            return user
        except IntegrityError:
            logger.warning(f"Пользователь уже существует: {telegram_id}")
            db.rollback()
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        db = next(self.get_db())
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        return user
    
    def create_order(self, user_id: int, product_type: str, product_id: str, 
                    price: float, order_id: str) -> Order:
        """Создание заказа"""
        db = next(self.get_db())
        order = Order(
            order_id=order_id,
            user_id=user_id,
            product_type=product_type,
            product_id=product_id,
            price=price
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        """Обновление статуса заказа"""
        db = next(self.get_db())
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if order:
            order.status = status
            db.commit()
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Статистика"""
        db = next(self.get_db())
        stats = {
            "total_users": db.query(User).count(),
            "total_orders": db.query(Order).count(),
            "total_revenue": db.query(Order).filter(Order.status == "paid").with_entities(func.sum(Order.price)).scalar() or 0,
            "active_users": db.query(User).filter(User.is_active == True).count()
        }
        return stats