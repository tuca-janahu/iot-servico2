# Robô monitor de nível de tanque

## Como rodar:
1. Criar o Virtual Environment
```bash
python -m venv .venv

```

2. Ativar o venv 
2. 1. Windows

```bash
.venv\Scripts\Activate.ps1
```

2. 2. MacOS / Linux

```bash
source .venv/bin/activate
```

3. Instalar dependências
```bash
pip install fastapi uvicorn influxdb-client python-dotenv
```

4. Criar arquivo .env e definir variáveis de ambiente 
```env
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=SEU_TOKEN_AQUI
INFLUX_ORG=SuaOrg
INFLUX_BUCKET=tank_monitor
```

5. Rodar via Uvicorn
```bash
uvicorn backend.main:app
``` 