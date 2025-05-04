from gpiozero import Button, LED, LEDCharDisplay
from pynput.keyboard import Controller
from signal import pause
import os
import time
import threading

# ========================
# 🔧 DEFINIÇÃO DE PINOS
# ========================

# Display 7 segmentos (ordem: A, B, C, D, E, F, G)
SEG_A = 2
SEG_B = 3
SEG_C = 4
SEG_D = 17
SEG_E = 27
SEG_F = 22
SEG_G = 10
# DP (decimal point) é opcional

# LEDs e buzzer
PIN_LED_ACERTO = 5
PIN_LED_ERRO   = 11
PIN_BUZZER     = 18

# Botões físicos (sem conflito com o display)
BTN_ALEGRIA   = 6
BTN_MEDO      = 13
BTN_TRISTEZA  = 19
BTN_NOJO      = 20
BTN_RAIVA     = 26

# Caminho do arquivo usado pelo Ren'Py para enviar comandos
gpio_control_path = "gpio_control.txt"

# ========================
# 🧠 VARIÁVEIS E OBJETOS
# ========================

keyboard = Controller()
pontos = 0

# LED e buzzer
led_acerto = LED(PIN_LED_ACERTO)
led_erro = LED(PIN_LED_ERRO)
buzzer = LED(PIN_BUZZER)  # para buzzer simples ON/OFF

# Display 7 segmentos (LEDs independentes)
display = LEDCharDisplay(SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G)

# ========================
# 📍 DISPLAY E AÇÕES
# ========================

def mostrar_digito(digito):
    try:
        display.value = str(digito % 10)
    except ValueError:
        display.off()

def acerto():
    global pontos
    pontos += 1
    led_acerto.on()
    print(f"[ACERTO] Pontos: {pontos}")
    mostrar_digito(pontos)
    time.sleep(3)
    led_acerto.off()

def erro():
    print("[ERRO]")
    led_erro.on()
    buzzer.on()
    time.sleep(0.5)
    buzzer.off()
    time.sleep(2.5)
    led_erro.off()

# ========================
# ⌨️ BOTÕES → TECLAS
# ========================

botao_map = {
    Button(BTN_ALEGRIA):   "a",
    Button(BTN_MEDO):      "m",
    Button(BTN_TRISTEZA):  "t",
    Button(BTN_NOJO):      "n",
    Button(BTN_RAIVA):     "r"
}

def handle_button_press(tecla):
    keyboard.press(tecla)
    keyboard.release(tecla)

# Conecta botões aos handlers
for botao, tecla in botao_map.items():
    botao.when_pressed = lambda tecla=tecla: handle_button_press(tecla)

# ========================
# 🔄 MONITORAMENTO
# ========================

def monitorar_comandos():
    print("Monitorando comandos do jogo...")
    while True:
        if os.path.exists(gpio_control_path):
            with open(gpio_control_path, "r") as f:
                comando = f.read().strip()
            os.remove(gpio_control_path)

            if comando == "ACERTO":
                acerto()
            elif comando == "ERRO":
                erro()

        time.sleep(0.05)

# ========================
# 🚀 INICIALIZAÇÃO
# ========================

threading.Thread(target=monitorar_comandos, daemon=True).start()

print("✅ Sistema GPIO com Display, LEDs e Buzzer pronto.")
pause()  # Mantém o script rodando
