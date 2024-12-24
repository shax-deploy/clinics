import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "W4u7S4r2tOD1n1aHA")  # Maxfiy kalitni muhit o'zgaruvchisi orqali olish
    ALGORITHM: str = "HS256"  # Algoritmni tanlash
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Tokenning amal qilish vaqti (minutlarda)

settings = Settings()
