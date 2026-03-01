from fastapi import APIRouter
from app.schemas.schemas import SystemStatusResponse, SimulateRequest
from app.services.service import luminosity_service

router = APIRouter(prefix="/api", tags=["luminosity"])


@router.get("/status", response_model=SystemStatusResponse)
def get_status():
    """Obtém status completo do sistema"""
    return luminosity_service.get_status()


@router.get("/sensor/ldr", response_model=dict)
def get_ldr():
    """Obtém dados do sensor LDR"""
    sensor_data = luminosity_service.ldr_sensor.get_data()
    return {
        "light_intensity": sensor_data.light_intensity,
        "luminosity_level": sensor_data.luminosity_level,
        "is_dark": sensor_data.is_dark
    }


@router.get("/relay/status", response_model=dict)
def get_relay():
    """Obtém status do relé"""
    return {"is_on": luminosity_service.relay.is_on}


@router.get("/leds/status", response_model=dict)
def get_leds():
    """Obtém status dos LEDs"""
    leds = luminosity_service.led_indicators.get_status()
    return {"low": leds.low, "medium": leds.medium, "high": leds.high}


@router.post("/relay/set")
def set_relay(state: bool):
    """Define estado do relé manualmente"""
    luminosity_service.set_relay_manual(state)
    return {"is_on": luminosity_service.relay.is_on}


@router.post("/mode/toggle", response_model=dict)
def toggle_mode():
    """Alterna entre modo automático e manual"""
    manual = luminosity_service.toggle_manual_mode()
    return {"manual_mode": manual}


@router.post("/mode/auto", response_model=dict)
def enable_auto():
    """Ativa modo automático"""
    luminosity_service.enable_auto_mode()
    return {"manual_mode": False}


@router.post("/simulate", response_model=dict)
def simulate(request: SimulateRequest):
    """Simula mudança na intensidade de luz"""
    if request.light_intensity < 0 or request.light_intensity > 100:
        return {"error": "Intensidade deve estar entre 0 e 100"}

    luminosity_service.update_light_intensity(request.light_intensity)
    status = luminosity_service.get_status()
    return status.model_dump()

