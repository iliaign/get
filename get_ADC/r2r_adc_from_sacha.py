import RPi.GPIO as IO
import time
import save_to_gr


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.1, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        # Инициализация GPIO
        IO.setmode(IO.BCM)
        IO.setup(self.bits_gpio, IO.OUT, initial=0)
        IO.setup(self.comp_gpio, IO.IN)
        
        if self.verbose:
            print("R2R_ADC initialized successfully")

    def deinit(self):
        """Корректное завершение работы с GPIO"""
        IO.output(self.bits_gpio, 0)
        IO.cleanup()
        if self.verbose:
            print("R2R_ADC deinitialized")

    def set_number(self, number):
        """Преобразование числа в бинарный массив"""
        return [int(element) for element in bin(number)[2:].zfill(8)]

    def number_to_dac(self, N):
        """Установка значения на ЦАП"""
        v_ar = self.set_number(N)
        for i, pin in enumerate(self.bits_gpio):
            IO.output(pin, v_ar[i])
        

    def sequental_counting_adc(self):
        """АЦП методом последовательного счета"""
        for i in range(256):
            self.number_to_dac(i)
            time.sleep(0.001)  # Небольшая задержка для стабилизации
            if IO.input(self.comp_gpio) > 0:
                break
        time.sleep(self.compare_time)
        return i

    def get_sc_voltage(self):
        """Получение напряжения методом последовательного счета"""
        return self.sequental_counting_adc() / 255 * self.dynamic_range

    def successive_approximation_adc(self):
        """АЦП методом последовательного приближения (бинарный поиск)"""
        left = 0
        right = 256
        
        while (right - left) > 1:
            mid = (right + left) // 2
            self.number_to_dac(mid)
            time.sleep(0.001)  # Задержка для стабилизации сигнала
            
            if IO.input(self.comp_gpio) > 0:
                right = mid
            else:
                left = mid

        
        time.sleep(self.compare_time)
        return left

    def get_sar_voltage(self):
        """Получение напряжения методом последовательного приближения"""
        return self.successive_approximation_adc() / 255 * self.dynamic_range


if __name__ == "__main__":
    filename = 'data_pp.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        pass


    
    try:
        # Создаем объект АЦП с динамическим диапазоном 3.31V
        adc = R2R_ADC(3.31, verbose=True)
        
        print("Starting SAR ADC measurements. Press Ctrl+C to stop.")
        
        while True:
            # Измеряем напряжение методом последовательного приближения
            voltage = adc.get_sar_voltage()
            
            print(f"Measured voltage: {voltage:.3f} V")
        
            # Сохраняем в файл (если модуль save_to_gr доступен)
            save_to_gr.write_to_txt_simple(voltage,filename)
            
            # Небольшая пауза между измерениями
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Корректное завершение работы
        adc.deinit()
        print("Program finished")
