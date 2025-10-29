from app.config import settings

ACCESS_TOKEN_SECRET = settings.access_token_secret
REFRESH_TOKEN_SECRET = settings.refresh_token_secret

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 14
