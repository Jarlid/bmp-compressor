### Использование программы

Для сжатия изображения: 

```python main [имя входного bmp-файла] [имя выходного файла] compress [тип сжатия: standard/simple/advanced] [коэффициент сжатия: int]```

Для получения изображения из сжатого формата:

```python main [имя входного файла] [имя выходного bmp-файла] decompress```

### Сжатый формат изображения.

Сжатый формат представляет собой последовательно записанные величины в битовом представлении:

Ширина, высота и amount в виде uint32, а затем матрицы U, Σ (значения на диагонали) и V для каждого цвета с размерами высота × amount, amount, ширина × amount соответсвенно, записанные в виде последовательных чисел float32.

Стоит заметить, что если ширина меньше высоты, то матрицы описывают транспонированное изображение.