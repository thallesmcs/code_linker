import serial
import time

# --- CONFIGURAÇÕES ---
# Altere para a porta serial correta do seu ESP32.
# No Windows, será algo como 'COM3', 'COM4', etc.
# No Linux ou macOS, será algo como '/dev/ttyUSB0' ou '/dev/tty.SLAB_USBtoUART'.
SERIAL_PORT = '/dev/ttyUSB0'  # <-- MUDE AQUI
BAUD_RATE = 115200    # Deve ser igual ao Serial.begin() do seu Arduino
OUTPUT_FILE = 'lora_log.txt' # Nome do arquivo onde os dados serão salvos

print(f"Iniciando logger na porta {SERIAL_PORT} a {BAUD_RATE} bps.")
print(f"Os dados serão salvos em '{OUTPUT_FILE}'.")
print("Pressione Ctrl+C para parar.")

# O 'try...finally' garante que a porta serial seja fechada corretamente ao sair
ser = None
try:
    # Abre a porta serial
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    # Abre o arquivo de log no modo 'append' (adicionar ao final)
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        while True:
            # Verifica se há dados na porta serial
            if ser.in_waiting > 0:
                # Lê uma linha (até encontrar um '\n')
                line = ser.readline()

                # Decodifica os bytes para uma string (UTF-8) e remove espaços em branco
                try:
                    decoded_line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    decoded_line = line.decode('latin-1').strip() # Tenta outra codificação se falhar

                # Se a linha não estiver vazia após remover espaços
                if decoded_line:
                    # Cria um timestamp
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"[{timestamp}] {decoded_line}"

                    # Imprime no console
                    print(log_entry)

                    # Escreve no arquivo, adicionando uma nova linha
                    f.write(log_entry + '\n')
                    f.flush() # Força a escrita imediata no disco

except serial.SerialException as e:
    print(f"Erro: Não foi possível abrir a porta serial '{SERIAL_PORT}'.")
    print(f"Detalhes: {e}")
    print("Verifique se a porta está correta e não está sendo usada por outro programa (como a Serial Monitor do Arduino IDE).")

except KeyboardInterrupt:
    print("\nParando o script...")

finally:
    if ser and ser.is_open:
        ser.close()
        print("Porta serial fechada.")
    print("Script finalizado.")