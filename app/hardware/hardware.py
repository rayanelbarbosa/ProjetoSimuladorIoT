from config import LDR_DARK_THRESHOLD, LDR_MEDIUM_THRESHOLD
from app.schemas.schemas import LuminosityLevel, LDRSensorResponse, LEDStatusResponse, RelayResponse


class LDRSensor:
    """Simula sensor LDR de fotoresistor"""

    def __init__(self):
        self.light_intensity = 50.0

    def set_intensity(self, value: float) -> None:
        """Define intensidade de luz (0-100)"""
        self.light_intensity = max(0, min(100, value))

    def read(self) -> float:
        """Lê intensidade de luz"""
        return self.light_intensity

    def get_level(self) -> LuminosityLevel:
        """Retorna nível de luminosidade"""
        if self.light_intensity < LDR_DARK_THRESHOLD:
            return LuminosityLevel.LOW
        elif self.light_intensity < LDR_MEDIUM_THRESHOLD:
            return LuminosityLevel.MEDIUM
        return LuminosityLevel.HIGH

    def is_dark(self) -> bool:
        """Verifica se está escuro"""
        return self.light_intensity < LDR_DARK_THRESHOLD

    def get_data(self) -> LDRSensorResponse:
        """Retorna dados do sensor"""
        return LDRSensorResponse(
            light_intensity=self.light_intensity,
            luminosity_level=self.get_level(),
            is_dark=self.is_dark()
        )


class LEDIndicators:
    """Simula LEDs indicadores de luminosidade"""

    def __init__(self):
        self.low = False
        self.medium = False
        self.high = False

    def update(self, level: LuminosityLevel) -> None:
        """Atualiza estado dos LEDs por nível"""
        self.low = level == LuminosityLevel.LOW
        self.medium = level == LuminosityLevel.MEDIUM
        self.high = level == LuminosityLevel.HIGH

    def get_status(self) -> LEDStatusResponse:
        """Retorna estado dos LEDs"""
        return LEDStatusResponse(low=self.low, medium=self.medium, high=self.high)


class Relay:
    """Simula relé da lâmpada"""

    def __init__(self):
        self.is_on = False

    def turn_on(self) -> None:
        """Liga a lâmpada"""
        self.is_on = True

    def turn_off(self) -> None:
        """Desliga a lâmpada"""
        self.is_on = False

    def set_state(self, state: bool) -> None:
        """Define estado do relé"""
        self.is_on = state

    def get_status(self) -> RelayResponse:
        """Retorna estado do relé"""
        return RelayResponse(is_on=self.is_on)

