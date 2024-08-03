from passlib.context import CryptContext
from fastapi.security import APIKeyHeader

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

apikey_scheme = APIKeyHeader(name="Authorization")
