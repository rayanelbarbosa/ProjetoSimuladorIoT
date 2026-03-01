from app.hardware.hardware import LDRSensor, LEDIndicators, Relay
from app.schemas.schemas import SystemStatusResponse


class LuminosityService:
    """Serviço de lógica de controle de luminosidade"""

    def __init__(self):
        self.ldr_sensor = LDRSensor()
        self.led_indicators = LEDIndicators()
        self.relay = Relay()
        self.manual_mode = False

    def update_light_intensity(self, intensity: float) -> None:
        """Atualiza intensidade de luz e controla sistema"""
        self.ldr_sensor.set_intensity(intensity)

        # Atualiza LEDs
        sensor_data = self.ldr_sensor.get_data()
        self.led_indicators.update(sensor_data.luminosity_level)

        # Controle automático do relé
        if not self.manual_mode:
            if sensor_data.is_dark:
                self.relay.turn_on()
            else:
                self.relay.turn_off()

    def toggle_manual_mode(self) -> bool:
        """Alterna entre modo automático e manual"""
        self.manual_mode = not self.manual_mode
        return self.manual_mode

    def set_relay_manual(self, state: bool) -> None:
        """Controla relé manualmente"""
        if self.manual_mode:
            self.relay.set_state(state)

    def enable_auto_mode(self) -> None:
        """Ativa modo automático"""
        self.manual_mode = False
        # Atualiza estado do relé baseado em luz atual
        sensor_data = self.ldr_sensor.get_data()
        if sensor_data.is_dark:
            self.relay.turn_on()
        else:
            self.relay.turn_off()

    def get_status(self) -> SystemStatusResponse:
        """Retorna status completo do sistema"""
        return SystemStatusResponse(
            ldr_sensor=self.ldr_sensor.get_data(),
            relay_status=self.relay.get_status(),
            leds_status=self.led_indicators.get_status(),
            manual_mode=self.manual_mode
        )


# Instância global do serviço
luminosity_service = LuminosityService()

