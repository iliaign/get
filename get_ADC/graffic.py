import matplotlib.pyplot as plt

filename  = 'data_pp.txt'
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

# Расчет периодов измерений
periods = []
for i in range(1, len(time_data)):
    periods.append(time_data[i] - time_data[i-1])
print(periods)

# Создание окна с двумя графиками
plt.figure(figsize=(15, 6))

# Первый график - напряжение от времени
plt.subplot(1, 2, 1)
plt.plot(time_data, voltage_data)
plt.title('Напряжение на пине OUT от времени')
plt.xlabel('Время, с')
plt.ylabel('Напряжение, В')
plt.grid(True)


# Второй график - гистограмма периодов
plt.subplot(1, 2, 2)
plt.hist(periods)
plt.title('Распределение продолжительности измерений')
plt.xlabel('Продолжительность измерения, с')
plt.ylabel('Количество измерений')
#plt.xlim(0, 0.06)
plt.grid(True)

# Показать оба графика
plt.show()