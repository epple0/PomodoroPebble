import time
import board
import digitalio
import busio
import neopixel
import adafruit_ssd1306

# ==========================================
# PINOUT (Updated: No Top LEDs)
# ==========================================
# Pin 0 (GPIO 26) -> Start/Stop Button
# Pin 1 (GPIO 27) -> Reset Button
# Pin 2 (GPIO 28) -> Underglow LEDs (4x, Bottom)
# Pin 3 (GPIO 29) -> UNUSED (Empty)
# Pin 4 (GPIO 6)  -> OLED SDA
# Pin 5 (GPIO 7)  -> OLED SCL
# ==========================================

# --- 1. DISPLAY SETUP (I2C) ---
i2c = busio.I2C(scl=board.D5, sda=board.D4)
oled_width = 128
oled_height = 32
try:
    display = adafruit_ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
except ValueError:
    print("Screen error: Check wiring. Ensure VCC/GND are correct.")

# --- 2. BUTTON SETUP ---
btn_start = digitalio.DigitalInOut(board.D0)
btn_start.direction = digitalio.Direction.INPUT
btn_start.pull = digitalio.Pull.UP

btn_reset = digitalio.DigitalInOut(board.D1)
btn_reset.direction = digitalio.Direction.INPUT
btn_reset.pull = digitalio.Pull.UP

# --- 3. LED SETUP ---
# Only Pin 2 is used now
pin_underglow = board.D2
num_underglow = 4
pixels = neopixel.NeoPixel(pin_underglow, num_underglow, brightness=0.3, auto_write=False)

# --- 4. CONFIGURATION ---
WORK_MINUTES = 25
BREAK_MINUTES = 5
current_seconds = WORK_MINUTES * 60

running = False
is_work_mode = True
last_tick = time.monotonic()
btn_start_state = True
btn_reset_state = True

# Colors (R, G, B)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
ORANGE  = (255, 100, 0)
WHITE   = (50, 50, 50)
OFF     = (0, 0, 0)

# --- HELPER FUNCTIONS ---

def draw_screen(title, seconds_left):
    display.fill(0)
    m = seconds_left // 60
    s = seconds_left % 60
    
    display.text(title, 0, 0, 1)
    time_str = "{:02d}:{:02d}".format(m, s)
    display.text(time_str, 40, 14, 1, size=2)
    display.show()

def set_underglow(color):
    pixels.fill(color)
    pixels.show()

# --- MAIN LOOP ---
print("Pomodoro Timer Started")
draw_screen("READY", current_seconds)
set_underglow(ORANGE) # Ready state

while True:
    now = time.monotonic()
    
    # --- READ BUTTONS ---
    cur_start = btn_start.value
    cur_reset = btn_reset.value

    # Check Start/Stop
    if not cur_start and btn_start_state:
        running = not running
        print("Start/Stop Pressed. Running:", running)
        time.sleep(0.05) # Debounce
    btn_start_state = cur_start

    # Check Reset
    if not cur_reset and btn_reset_state:
        print("Reset Pressed")
        running = False
        is_work_mode = True
        current_seconds = WORK_MINUTES * 60
        draw_screen("RESET", current_seconds)
        set_underglow(WHITE)
        time.sleep(0.5)
        
        # Return to ready state
        draw_screen("READY", current_seconds)
        set_underglow(ORANGE)
    btn_reset_state = cur_reset

    # --- TIMER LOGIC ---
    if running:
        if now - last_tick >= 1.0:
            current_seconds -= 1
            last_tick = now
            
            # Determine Mode & Color
            if is_work_mode:
                mode_txt = "FOCUS"
                glow_col = RED
            else:
                mode_txt = "BREAK"
                glow_col = BLUE
                
            draw_screen(mode_txt, current_seconds)
            set_underglow(glow_col)

            # Timer Finished
            if current_seconds <= 0:
                running = False
                # Flash lights
                for _ in range(5):
                    set_underglow(WHITE)
                    time.sleep(0.2)
                    set_underglow(OFF)
                    time.sleep(0.2)
                
                # Switch Modes
                if is_work_mode:
                    is_work_mode = False
                    current_seconds = BREAK_MINUTES * 60
                    draw_screen("TAKE BREAK", current_seconds)
                    set_underglow(BLUE)
                else:
                    is_work_mode = True
                    current_seconds = WORK_MINUTES * 60
                    draw_screen("BACK 2 WORK", current_seconds)
                    set_underglow(RED)
                    
    else:
        # Paused in middle of session
        if current_seconds != WORK_MINUTES * 60 and current_seconds != BREAK_MINUTES * 60:
            set_underglow(ORANGE) # Orange indicates paused/waiting
            
    time.sleep(0.01)
