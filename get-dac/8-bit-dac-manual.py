import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led = ([22, 27, 17, 26, 25, 21, 20, 16])[::-1]
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)

dynamic_range = 3.3

def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print(f'Напряжение выходит за динамический диапазон ЦАП (0ю00 - {dynamic_range:.2f} В)')
        print(f'Устанавливаем 0.0 В') 
        return 0
    return int(voltage / dynamic_range * 255)


def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]


def number_to_dac(element):
    bn = dec2bin(element)
    for i in range(len(led)):
        GPIO.output(led[i], bn[i])


try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except:
            print('Вы ввели не число. Попробуйте ущё раз')

finally:
    GPIO.output(led, 0)
    GPIO.cleanup()    