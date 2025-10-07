import smbus


class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        """
        Установка напряжения на выходе MCP4725
        
        Args:
            voltage (float): Напряжение от 0.0 до dynamic_range В
        """
        # Проверка диапазона
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.3f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0
        
        # Преобразование напряжения в 12-битное значение
        value = int((voltage / self.dynamic_range) * 4095)
        
        # Ограничение значения (0-4095)
        value = max(0, min(4095, value))
        
        # Использование существующего метода set_number
        self.set_number(value)
        
        if self.verbose:
            actual_voltage = (value / 4095.0) * self.dynamic_range
            print(f"Установлено напряжение: {actual_voltage:.3f} В, код ЦАП: {value}/4095")


if __name__ == "__main__":
    try:
        # Создание MCP4725 с указанными параметрами
        dac = MCP4725(dynamic_range=5, address=0x61, verbose=True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()