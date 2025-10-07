import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        
        # Создание и запуск ШИМ
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)  # Запуск с 0% заполнения
        
        if self.verbose:
            print(f"PWM DAC инициализирован на пине {gpio_pin}")
            print(f"Частота ШИМ: {pwm_frequency} Гц")
            print(f"Динамический диапазон: {dynamic_range:.3f} В")
        
    def deinit(self):
        """Остановка ШИМ и очистка GPIO"""
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        if self.verbose:
            print("PWM DAC деинициализирован")
    
    def set_voltage(self, voltage):
        """Установка напряжения через ШИМ"""
        # Проверка диапазона напряжения
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.3f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0
        
        # Расчет коэффициента заполнения (duty cycle)
        duty_cycle = (voltage / self.dynamic_range) * 100
        
        # Установка коэффициента заполнения
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.3f} В, заполнение: {duty_cycle:.2f}%")


# Основной охранник
if __name__ == "__main__":
    try:
        # Создание ШИМ ЦАП с указанными параметрами
        dac = PWM_DAC(12, 500, 3.290, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()