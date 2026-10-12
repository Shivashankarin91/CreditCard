
import os
from datetime import datetime
from decimal import Decimal
from typing import Literal
from jwt.exceptions import InvalidTokenError
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, sessionmaker

from database import engine
from models import Transaction

load_dotenv()

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not JWT_SIGNING_KEY:
    raise RuntimeError("JWT_SIGNING_KEY is missing from fastapi_backend/.env")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

app = FastAPI(
    title="Credit Card Payment System API",
    description="JWT-protected simulated payment processing",
    version="1.0.0",
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> int:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Bearer access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SIGNING_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "user_id"]},
        )

        # Django Simple JWT may encode user_id as "4".
        raw_user_id = payload.get("user_id")

        if isinstance(raw_user_id, bool):
            raise ValueError("Invalid user ID")

        user_id = int(raw_user_id)

        if user_id <= 0:
            raise ValueError("Invalid user ID")

        return user_id

    except (InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="INR", pattern="^[A-Z]{3}$")
    description: str | None = Field(default=None, max_length=255)


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    currency: str
    status: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentSimulationRequest(BaseModel):
    outcome: Literal["SUCCESS", "FAILED"]

@app.post(
    "/api/transactions/",
    response_model=TransactionResponse,
    status_code=201,
)
def create_transaction(
    payload: TransactionCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction = Transaction(
        user_id=user_id,
        amount=payload.amount,
        currency=payload.currency,
        status="PENDING",
        description=payload.description,
    )

    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the transaction",
        )


@app.get(
    "/api/transactions/",
    response_model=list[TransactionResponse],
)
def get_transactions(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc(), Transaction.id.desc())
        .all()
    )


@app.post("/api/transactions/{transaction_id}/simulate-payment")
def simulate_payment(
    transaction_id: int,
    payload: PaymentSimulationRequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
        .first()
    )

    if transaction is None:
        # Does not disclose whether another user's transaction exists.
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    if transaction.status.upper() != "PENDING":
        raise HTTPException(
            status_code=409,
            detail="Only pending transactions can be processed",
        )

    transaction.status = payload.outcome

    try:
        db.commit()
        db.refresh(transaction)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not update payment status",
        )

    return {
        "transaction_id": transaction.id,
        "amount": str(transaction.amount),
        "status": transaction.status,
        "message": "Payment simulation completed",
    }