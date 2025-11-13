import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS  # <<-- IMPORTANTE

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

# (opcional mas recomendado) validação básica das envs
missing = [name for name, value in {
    "INFLUX_URL": INFLUX_URL,
    "INFLUX_TOKEN": INFLUX_TOKEN,
    "INFLUX_ORG": INFLUX_ORG,
    "INFLUX_BUCKET": INFLUX_BUCKET,
}.items() if not value]

if missing:
    raise RuntimeError(f"Variáveis do InfluxDB faltando no .env: {', '.join(missing)}")

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

write_api = client.write_api(write_options=SYNCHRONOUS)
# (ou simplesmente: write_api = client.write_api() )


def write_sensor_data(data: dict):
    # timestamp em SEGUNDOS (epoch). Se vier em ms, use / 1000
    ts = datetime.fromtimestamp(data["timestamp"], tz=timezone.utc)

    p = (
        Point("monitor_tanque")
        .tag("device", data.get("device", "esp32_monitor"))
        .field("tank_level", float(data["tank_level"]))
        .time(ts, WritePrecision.S)
    )

    if "temperature" in data:
        p.field("temperature", float(data["temperature"]))
    if "humidity" in data:
        p.field("humidity", float(data["humidity"]))
    if "luminosity" in data:
        p.field("luminosity", float(data["luminosity"]))
    if "presence" in data:
        p.field("presence", int(data["presence"]))

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
