from fastapi import APIRouter, Request
from app.schemas.schemas import SystemStatusResponse, SimulateRequest
from app.services.service import luminosity_service
import json

router = APIRouter(prefix="/api", tags=["luminosity"])


def _print_state(label: str, extra: dict = None):
    s = luminosity_service
    sensor = s.ldr_sensor.get_data()
    relay = s.relay.get_status()
    leds = s.led_indicators.get_status()
    print("\n" + "="*55)
    print(f"  [{label}]")
    if extra:
        print(f"  >> Dados recebidos: {json.dumps(extra, ensure_ascii=False)}")
    print(f"  MEMÓRIA ATUAL:")
    print(f"    Intensidade de luz  : {sensor.light_intensity}%")
    print(f"    Nível de luminosidade: {sensor.luminosity_level}")
    print(f"    Está escuro?        : {sensor.is_dark}")
    print(f"    Relé ligado?        : {relay.is_on}")
    print(f"    LEDs (low/med/high) : {leds.low} / {leds.medium} / {leds.high}")
    print(f"    Modo manual?        : {s.manual_mode}")
    print("="*55)


@router.get("/status", response_model=SystemStatusResponse)
def get_status():
    _print_state("GET /api/status")
    return luminosity_service.get_status()


@router.get("/sensor/ldr", response_model=dict)
def get_ldr():
    """Obtém dados do sensor LDR"""
    _print_state("GET /api/sensor/ldr")
    sensor_data = luminosity_service.ldr_sensor.get_data()
    return {
        "light_intensity": sensor_data.light_intensity,
        "luminosity_level": sensor_data.luminosity_level,
        "is_dark": sensor_data.is_dark
    }


@router.get("/relay/status", response_model=dict)
def get_relay():
    """Obtém status do relé"""
    _print_state("GET /api/relay/status")
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
    _print_state("POST /api/relay/set", {"state": state})
    return {"is_on": luminosity_service.relay.is_on}


@router.post("/mode/toggle", response_model=dict)
def toggle_mode():
    """Alterna entre modo automático e manual"""
    manual = luminosity_service.toggle_manual_mode()
    _print_state("POST /api/mode/toggle", {"manual_mode": manual})
    return {"manual_mode": manual}


@router.post("/mode/auto", response_model=dict)
def enable_auto():
    """Ativa modo automático"""
    luminosity_service.enable_auto_mode()
    _print_state("POST /api/mode/auto")
    return {"manual_mode": False}


@router.post("/simulate", response_model=dict)
def simulate(request: SimulateRequest):
    """Simula mudança na intensidade de luz"""
    if request.light_intensity < 0 or request.light_intensity > 100:
        return {"error": "Intensidade deve estar entre 0 e 100"}

    luminosity_service.update_light_intensity(request.light_intensity)
    _print_state("POST /api/simulate", {"light_intensity": request.light_intensity})
    status = luminosity_service.get_status()
    return status.model_dump()

