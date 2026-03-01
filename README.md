# Controle de Luminosidade com Sensor LDR

Backend em FastAPI para simulação de IoT com controle automático de luminosidade.

## 📁 Estrutura do Projeto

```
PythonProject/
├── config.py                    # Configurações globais
├── requirements.txt             # Dependências
└── app/
    ├── main.py                  # Aplicação FastAPI principal
    ├── __init__.py
    ├── schemas/                 # Modelos Pydantic
    │   ├── __init__.py
    │   └── schemas.py           # Schemas de entrada/saída
    ├── hardware/                # Simulação de componentes
    │   ├── __init__.py
    │   └── hardware.py          # LDRSensor, Relay, LEDIndicators
    ├── services/                # Lógica de negócio
    │   ├── __init__.py
    │   └── service.py           # LuminosityService
    └── api/                     # Endpoints da API
        ├── __init__.py
        └── routes.py            # Rotas REST
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar a API

```bash
python app/main.py
```

A API estará disponível em: **http://localhost:8000**

## 📡 Endpoints da API

### Status Geral
- **GET** `/api/status` - Status completo do sistema

### Sensores
- **GET** `/api/sensor/ldr` - Dados do sensor LDR (intensidade, nível, is_dark)

### Atuadores
- **GET** `/api/relay/status` - Status da lâmpada (is_on)
- **POST** `/api/relay/set?state=true` - Ligar/desligar lâmpada
- **GET** `/api/leds/status` - Status dos LEDs (low, medium, high)

### Controle
- **POST** `/api/mode/toggle` - Alternar entre modo automático e manual
- **POST** `/api/mode/auto` - Ativar modo automático

### Simulação
- **POST** `/api/simulate` - Simular mudança na intensidade de luz

## 🔌 Como Conectar as Rotas

As rotas estão definidas em `app/api/routes.py` e são registradas automaticamente no `app/main.py`:

```python
# Em app/main.py
from app.api.routes import router

app.include_router(router)
```

Para adicionar novos endpoints:

1. Crie a função em `app/api/routes.py`
2. Use o decorator `@router.get()` ou `@router.post()`
3. A rota será automaticamente registrada com prefixo `/api`

Exemplo:
```python
@router.get("/novo-endpoint")
def novo_endpoint():
    return {"resultado": "sucesso"}
```

## 🧪 Como Testar

### Usando curl

```bash
# Status completo
curl http://localhost:8000/api/status

# Simular ambiente escuro (vai ligar a lâmpada automaticamente)
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"light_intensity": 15}'

# Verificar se lâmpada ligou
curl http://localhost:8000/api/relay/status

# Simular ambiente claro
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"light_intensity": 80}'

# Alternar para modo manual
curl -X POST http://localhost:8000/api/mode/toggle

# Controlar relé manualmente
curl -X POST "http://localhost:8000/api/relay/set?state=true"

# Voltar ao modo automático
curl -X POST http://localhost:8000/api/mode/auto
```

### Usando Swagger UI

Acesse **http://localhost:8000/docs** e teste os endpoints interativamente.

### Usando Python/React

```javascript
// Exemplo em React
const response = await fetch('http://localhost:8000/api/status');
const status = await response.json();
console.log(status);
```

## 📊 Limiares de Luminosidade

- **Baixo (Escuro)**: < 30% - Lâmpada liga automaticamente
- **Médio**: 30% - 60%
- **Alto (Claro)**: > 60% - Lâmpada desliga automaticamente

Esses valores podem ser ajustados em `config.py`:
```python
LDR_DARK_THRESHOLD = 30
LDR_MEDIUM_THRESHOLD = 60
```

## 🔄 Fluxo de Funcionamento

### Modo Automático (Padrão)
1. Sensor LDR lê intensidade de luz
2. Se luz < 30%: Relé liga, LED vermelho acende
3. Se luz 30-60%: Relé desliga, LED amarelo acende
4. Se luz > 60%: Relé desliga, LED verde acende

### Modo Manual
1. Usuário envia comando para ligar/desligar via API
2. LEDs continuam indicando nível atual de luz
3. Usuário pode voltar ao modo automático a qualquer momento

## 🛠️ Arquitetura em Camadas

1. **Schemas** (`app/schemas/`) - Validação e serialização de dados
2. **Hardware** (`app/hardware/`) - Simulação de sensores e atuadores
3. **Services** (`app/services/`) - Lógica de negócio
4. **API** (`app/api/`) - Endpoints REST

Cada camada tem responsabilidade bem definida e se comunica com a anterior.

## 📝 Resposta Padrão

Todos os endpoints retornam JSON com status completo ou parcial:

```json
{
  "ldr_sensor": {
    "light_intensity": 45.5,
    "luminosity_level": "médio",
    "is_dark": false
  },
  "relay_status": {
    "is_on": false
  },
  "leds_status": {
    "low": false,
    "medium": true,
    "high": false
  },
  "manual_mode": false
}
```

## 🎯 Implementado

✅ Sensor LDR simulado  
✅ Relé automático para lâmpada  
✅ LEDs indicadores (3 níveis)  
✅ Controle manual via botão (API)  
✅ Modo automático e manual  
✅ 8 endpoints REST  
✅ CORS habilitado para React  
✅ Documentação automática (Swagger)  

