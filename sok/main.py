#!/usr/bin/env python3
# coding: utf-8

import os,sys
import inspect
import time
from starlette.responses import JSONResponse
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse



import platform
iis=( platform.uname().system=='Windows' )
if iis:
  # pip install a2wsgi
  # pip install wfastcgi
  # wfastcgi-enable - jako admin po aktywacji venv: https://mtuseeq.medium.com/how-to-deploy-flask-app-on-windows-server-using-fastcgi-and-iis-73d8139d5342
  #D:\er\venv\Scripts\python.exe|D:\etr\venv\Lib\site-packages\wfastcgi.py
  from a2wsgi import ASGIMiddleware
use_ssl = iis
if use_ssl:
  import ssl

# logger
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(debug=True,
              title="Nomos",
              description="",
              summary=".",
              version="0.0.1",
              )

@app.get('/health')
def health():
  return HTMLResponse(f"OK", status_code=200)

# Lista dozwolonych źródeł (domen)
# W środowisku deweloperskim możesz użyć "*" dla wszystkich źródeł,
# ale w produkcji ZAWSZE ograniczaj do konkretnych domen.
origins = [
    "http://localhost:3000",  # Adres aplikacji frontend
    "http://127.0.0.1:3000", # Czasem potrzebne, jeśli przeglądarka używa 127.0.0.1 zamiast localhost
    "http://localhost:8080",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista dozwolonych źródeł
    allow_credentials=True, # Zezwól na ciasteczka/nagłówki autoryzacyjne w żądaniach cross-origin
    allow_methods=["*"],    # Zezwól na wszystkie metody HTTP (GET, POST, PUT, DELETE, OPTIONS itp.)
    allow_headers=["*"],    # Zezwól na wszystkie nagłówki w żądaniach cross-origin
)

# Middleware do logowania wywołań
@app.middleware("http")
async def log_requests(request: Request, call_next):
  """
  Middleware do logowania czasu trwania żądania oraz jego statusu.
  """
  start_time = time.time()
  try:
    response = await call_next(request)
  except Exception as e:
    logger.error(f"Request failed: {request.method} {request.url} - Exception: {e}")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

  process_time = time.time() - start_time
  logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Czas: {process_time:.4f}s")
  return response


if iis:
  wsgi_app = ASGIMiddleware(app)

from api.lt import router as lt_router
from api.kn import router as kn_router
from api.legislative import router as legislative_router
from api.judiciary import router as judiciary_router
from api.referendum import router as referendum_router
app.include_router(lt_router)
app.include_router(kn_router)
app.include_router(legislative_router)
app.include_router(judiciary_router)
app.include_router(referendum_router)

if __name__ == "__main__":
  import uvicorn
  logger.info('Start aplikacji Nomos')
  if use_ssl:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    # openssl pkcs12 -export -out self.pfx -inkey  key.pem -in cert.pem
    # dodaj pfx do zaufanych
    ssl_context.load_cert_chain('./cert.pem', keyfile='./key.pem')
    uvicorn.run(app, host="0.0.0.0", port=8086, \
                ssl_keyfile='./key.pem',
                ssl_certfile='./cert.pem')
  else:
    uvicorn.run(app, host="0.0.0.0", port=8086)