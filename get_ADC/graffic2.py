import matplotlib.pyplot as plt

filename = 'data.txt'
# Чтение данных из файла
data = []
with open(filename, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        time = float(parts[0])
        voltage = float(parts[1])
        data.append((time, voltage))

# Разделение на время и напряжение
time_data = [point[0] for point in data]
voltage_data = [point[1] for point in data]

# Расчет периодов дискретизации
sampling_periods = []
for i in range(1, len(time_data)):
    sampling_periods.append(time_data[i] - time_data[i-1])

# Находим период сигнала (время между двумя соседними максимумами или минимумами)
# Для простоты будем искать точки, где производная меняет знак (экстремумы)
extremum_times = []
for i in range(1, len(voltage_data)-1):
    if (voltage_data[i] > voltage_data[i-1] and voltage_data[i] > voltage_data[i+1]) or \
       (voltage_data[i] < voltage_data[i-1] and voltage_data[i] < voltage_data[i+1]):
        extremum_times.append(time_data[i])

# Вычисляем периоды сигнала (время между экстремумами)
signal_periods = []
for i in range(1, len(extremum_times)):
    signal_periods.append(extremum_times[i] - extremum_times[i-1])

# Для каждого периода сигнала считаем, сколько периодов дискретизации в него входит
sampling_periods_per_signal_period = []
for signal_period in signal_periods:
    count = 0
    current_time = 0
    for sampling_period in sampling_periods:
        current_time += sampling_period
        if current_time <= signal_period:
            count += 1
        else:
            break
    if count > 0:
        sampling_periods_per_signal_period.append(count)

# Создание окна с тремя графиками
plt.figure(figsize=(18, 6))

# Первый график - напряжение от времени
plt.subplot(1, 3, 1)
plt.plot(time_data, voltage_data)
plt.title('Напряжение на пине OUT от времени')
plt.xlabel('Время, с')
plt.ylabel('Напряжение, В')
plt.grid(True)

# Второй график - гистограмма периодов дискретизации
plt.subplot(1, 3, 2)
plt.hist(sampling_periods, bins=20)
plt.title('Распределение периодов дискретизации')
plt.xlabel('Период дискретизации, с')
plt.ylabel('Количество')
plt.grid(True)

# Третий график - гистограмма количества периодов дискретизации в периоде сигнала
plt.subplot(1, 3, 3)
if sampling_periods_per_signal_period:
    plt.hist(sampling_periods_per_signal_period, bins=range(min(sampling_periods_per_signal_period), max(sampling_periods_per_signal_period)+2))
    plt.title('Количество периодов дискретизации в периоде сигнала')
    plt.xlabel('Количество периодов дискретизации')
    plt.ylabel('Количество периодов сигнала')
    plt.grid(True)
else:
    plt.text(0.5, 0.5, 'Не удалось определить\nпериоды сигнала', 
             horizontalalignment='center', verticalalignment='center',
             transform=plt.gca().transAxes)
    plt.title('Количество периодов дискретизации в периоде сигнала')

plt.tight_layout()
plt.show()

# Вывод статистики
if sampling_periods_per_signal_period:
    print(f"Среднее количество периодов дискретизации в периоде сигнала: {sum(sampling_periods_per_signal_period)/len(sampling_periods_per_signal_period):.2f}")
    print(f"Минимальное количество: {min(sampling_periods_per_signal_period)}")
    print(f"Максимальное количество: {max(sampling_periods_per_signal_period)}")
