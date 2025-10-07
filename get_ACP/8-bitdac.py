import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Исправляем список пинов (убираем дублирование)
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]  # ✅ Заменил второй 16 на 12
dynamic_range = 3.3

for i in dac_bits:
    GPIO.setup(i, GPIO.OUT)

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавлниваем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]


def number_to_dac(number):
    bits = dec2bin(number)
    for i in range(8):
        GPIO.output(dac_bits[i], bits[i])

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)  # ✅ Правильный вызов
            print(f"Установлено напряжение: {voltage:.2f} В, код ЦАП: {number}")

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()