from fastapi import FastAPI
from app.database import engine, Base
from sqlalchemy.orm import Session
from celery import Celery
import requests, os
from twilio.rest import Client
from database import SessionLocal, engine, Base
from models import Product


app = FastAPI()  
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API funcionando!"}

# Inicializar FastAPI
app = FastAPI()

# Configuração do Celery
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Buscar preço no Mercado Livre
@celery.task
def fetch_product_price(product_id: str):
    url = f"https://api.mercadolibre.com/items/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data["title"],
            "price": data["price"],
            "seller": data["seller_id"],
        }
    return None

# Enviar notificação via WhatsApp
@celery.task
def send_whatsapp_alert(message: str, to_number: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        body=message,
        to=f"whatsapp:{to_number}"
    )

# Endpoint para iniciar monitoramento
@app.post("/track/{product_id}")
def track_product(product_id: str, db: Session = Depends(get_db)):
    task = fetch_product_price.delay(product_id)
    return {"message": "Produto sendo monitorado", "task_id": task.id}

# Passo a passo para rodar o projeto:
# 1. Instale dependências: pip install -r requirements.txt
# 2. Configure o banco PostgreSQL e crie um arquivo .env com as credenciais
# 3. Rode o banco de dados e o Redis (pode usar Docker)
# 4. Inicie o Celery: celery -A app.celery worker --loglevel=info
# 5. Rode a API: uvicorn app.main:app --reload
# 6. Teste o endpoint: use um cliente HTTP como Postman ou Curl para chamar /track/{product_id}
