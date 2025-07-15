import os
from dotenv import load_dotenv

# Garante carregamento do .env.local para qualquer módulo que importar isso
load_dotenv(dotenv_path=".env.local")
