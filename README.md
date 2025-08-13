# code_linker

Projeto inicial para comunicação LoRa com Heltec WiFi LoRa 32 V3, envio periódico de mensagens "Hello World" com contador e leitura/log da porta serial via Python.

## Visão geral

- Emissor (ESP32 Heltec V3): envia, a cada ~1 segundo, a mensagem `Hello world #N` via LoRa.
- Receptor (ESP32 Heltec V3): escuta o mesmo canal e imprime na serial o payload recebido com RSSI e tamanho.
- Logger Python: lê a saída serial do receptor (via `pyserial`) e salva tudo em `lora_log.txt`.

> Observação: os exemplos usam frequência LoRa de 450 MHz definida no código. Verifique a regulamentação local antes de operar nessa faixa e ajuste conforme necessário.

### Ambiente de referência

- Execução atual do logger em um Raspberry Pi 5 com Ubuntu 24.04 LTS. Por isso, o valor padrão da porta serial no script é `/dev/ttyUSB0`.
- Para usuários no Windows, mantenha as instruções com portas `COMx` (ex.: `COM3`, `COM4`).

## Estrutura do repositório

- `LoRaSender_millis_counter/LoRaSender_millis_counter.ino`
	- Emissor. Monta a string `Hello world #<contador>` e envia via LoRa aproximadamente a cada 1s.
	- Parâmetros relevantes: `RF_FREQUENCY = 450000000`, `TX_OUTPUT_POWER = 5`, `Serial.begin(115200)`.

- `LoRaReceiver_millis_counter/LoRaReceiver_millis_counter.ino`
	- Receptor. Mantém o rádio em RX contínuo e imprime mensagens recebidas: `received packet "..." with rssi X , length Y`.
	- Parâmetros relevantes: `RF_FREQUENCY = 450000000`, `Serial.begin(115200)`.

- `leitura_da_serial.py`
	- Script Python que:
		- Abre a porta serial (115200 bps),
		- Lê linhas do monitor serial do receptor,
		- Prependa timestamp e salva em `lora_log.txt` (modo append),
		- Mostra no console.
	- Ajuste a constante `SERIAL_PORT` para a porta correta. Por padrão está `/dev/ttyUSB0` (ambiente alvo: Raspberry Pi 5 + Ubuntu 24.04 LTS). No Windows, use algo como `COM3`, `COM4`, etc.

- `lora_log.txt`
	- Arquivo de log gerado pelo script Python com as mensagens recebidas do receptor.

## Requisitos

- Hardware
	- 2x Heltec WiFi LoRa 32 (V3) ou equivalentes (um para TX, outro para RX).

- Software (Arduino)
	- Arduino IDE (ou PlatformIO) com suporte para Heltec V3 e biblioteca LoRa (projeto Heltec que fornece `LoRaWan_APP.h`).

- Software (Python)
	- Python 3.x
	- Pacote `pyserial`

## Como usar

1) Carregar os sketches
- Abra cada `.ino` na IDE do Arduino.
- Selecione a placa Heltec WiFi LoRa 32 V3 e a porta correta.
- Garanta que emissor e receptor usem o mesmo `RF_FREQUENCY` e parâmetros LoRa.
- Faça o upload do emissor em um dispositivo e do receptor no outro.

2) Verificar a serial do receptor (opção A: IDE)
- Abra o Monitor Serial na IDE do Arduino (115200 bps) no dispositivo receptor para ver as mensagens chegando.

3) Registrar logs com Python (opção B: Windows PowerShell)
- Instale o `pyserial` e rode o logger apontando para a porta do receptor:

```powershell
pip install pyserial

# Edite a constante SERIAL_PORT no arquivo se necessário (ex.: 'COM4').
python .\leitura_da_serial.py
```

O console mostrará as linhas recebidas com timestamp e o arquivo `lora_log.txt` será atualizado continuamente.

## Dicas e solução de problemas

- Porta ocupada: feche o Monitor Serial da IDE antes de executar o script Python.
- Porta incorreta (Windows): teste `COM3`, `COM4`, etc. Verifique no Gerenciador de Dispositivos.
- Sem recepção: confirme antenas, frequência (`RF_FREQUENCY`) e proximidade dos módulos. Ajuste potência/parametrização LoRa conforme necessário.
- Codificação: o script tenta UTF-8 e, se falhar, usa Latin-1 para evitar erros de decodificação.

 
