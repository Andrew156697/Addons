from gpiozero import LED
from time import sleep

# Định nghĩa chân GPIO cho LED
led = LED(17)  # Sử dụng chân GPIO 17

while True:
    led.on()  # Bật LED
    sleep(1)  # Chờ 1 giây
    led.off()  # Tắt LED
    sleep(1)  # Chờ 1 giây