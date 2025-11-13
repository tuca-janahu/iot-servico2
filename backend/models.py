from pydantic import BaseModel, Field
from typing import Optional


class TelemetryIn(BaseModel):
    tank_level: float = Field(..., ge=0, le=100, description="Nível do tanque em %")
    temperature: float
    humidity: float
    luminosity: float
    presence: bool
    timestamp: Optional[int] = Field(
        None,
        description="Epoch time (segundos ou ms) opcional; se não vier, o backend usa o tempo do servidor."
    )
