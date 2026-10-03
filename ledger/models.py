from enum import Enum
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, ForeignKey, String, Enum as SQLEnum


class EntryDirection(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class AccountType(Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    account_type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType))
    currency: Mapped[str] = mapped_column(String(3))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")
