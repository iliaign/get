import time
start_time  = time.time()
# Альтернативная версия с более простым форматом
def write_to_txt_simple(value, filename='data.txt'):
    """
    Упрощенная версия записи в текстовый файл
    """
    elapsed_time = time.time() - start_time
    
    with open(filename, 'a', encoding='utf-8') as file:
        a = str(round(elapsed_time,6)) + ','+ str(value) +'\n'
        file.write(a)

print(1)

