from enum import Enum
from pydantic import BaseModel


class LuminosityLevel(str, Enum):
    LOW = "baixo"
    MEDIUM = "médio"
    HIGH = "alto"


class LDRSensorResponse(BaseModel):
    light_intensity: float
    luminosity_level: LuminosityLevel
    is_dark: bool


class RelayResponse(BaseModel):
    is_on: bool


class LEDStatusResponse(BaseModel):
    low: bool
    medium: bool
    high: bool


class SystemStatusResponse(BaseModel):
    ldr_sensor: LDRSensorResponse
    relay_status: RelayResponse
    leds_status: LEDStatusResponse
    manual_mode: bool


class SimulateRequest(BaseModel):
    light_intensity: float

