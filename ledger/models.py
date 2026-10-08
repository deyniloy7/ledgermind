from datetime import datetime
from decimal import Decimal
from enum import Enum
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    func,
    String,
    Enum as SQLEnum,
    true,
)


class EntryDirection(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class RelationType(Enum):
    REVERSAL = "REVERSAL"
    REPLACEMENT = "REPLACEMENT"


class AccountType(Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    account_type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType))
    currency: Mapped[str] = mapped_column(String(3))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true())


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("organization_id", "idempotency_key"),
        CheckConstraint(
            "(related_transaction_id IS NULL AND relation_type IS NULL) "
            "OR (relation_type IS NOT NULL AND related_transaction_id IS NOT NULL)",
            name="ck_transactions_relations_pair",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    description: Mapped[str] = mapped_column(String(200))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    idempotency_key: Mapped[str] = mapped_column(String(255))
    related_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id")
    )
    relation_type: Mapped[RelationType | None] = mapped_column(SQLEnum(RelationType))
    entries: Mapped[list["Entry"]] = relationship(back_populates="transaction")


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_entries_amount_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 4))
    direction: Mapped[EntryDirection] = mapped_column(SQLEnum(EntryDirection))
    transaction: Mapped["Transaction"] = relationship(back_populates="entries")
