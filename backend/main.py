from fastapi import FastAPI, HTTPException
from .models import TelemetryIn
from .influx_client import write_sensor_data

app = FastAPI(
    title="API Monitor Tanque ESP32",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"status": "ok", "msg": "API do monitor de tanque está no ar."}


@app.post("/telemetry")
def receive_telemetry(payload: TelemetryIn):
    try:
        write_sensor_data(payload.model_dump())
        return {"status": "ok"}
    except Exception as e:
        print("Erro ao escrever no InfluxDB:", e)
        raise HTTPException(status_code=500, detail="Erro ao salvar dados no InfluxDB")
