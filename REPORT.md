### Рубрика Эксперименты!

<details>
<summary>Изначальное изображение.</summary>

![](pictures/base.bmp)

</details>

<details>
<summary>Таблица изображений после сжатия.</summary>

| N      | standard                      | simple                      | advanced                      |
|--------|-------------------------------|-----------------------------|-------------------------------|
| **1**  | ![](pictures/standard_1.bmp)  | ![](pictures/simple_1.bmp)  | ![](pictures/advanced_1.bmp)  |
| **2**  | ![](pictures/standard_2.bmp)  | ![](pictures/simple_2.bmp)  | ![](pictures/advanced_2.bmp)  |
| **3**  | ![](pictures/standard_3.bmp)  | ![](pictures/simple_3.bmp)  | ![](pictures/advanced_3.bmp)  |
| **5**  | ![](pictures/standard_5.bmp)  | ![](pictures/simple_5.bmp)  | ![](pictures/advanced_5.bmp)  |
| **10** | ![](pictures/standard_10.bmp) | ![](pictures/simple_10.bmp) | ![](pictures/advanced_10.bmp) |
| **20** | ![](pictures/standard_20.bmp) | ![](pictures/simple_20.bmp) | ![](pictures/advanced_20.bmp) |
| **30** | ![](pictures/standard_30.bmp) | ![](pictures/simple_30.bmp) | ![](pictures/advanced_30.bmp) |
| **50** | ![](pictures/standard_50.bmp) | ![](pictures/simple_50.bmp) | ![](pictures/advanced_50.bmp) |

</details>

Можно видеть, что результаты разных алгоритмов очень похожи (```standard``` и ```simple``` не отличить на глаз, а ```advanced``` немного отличается из-за приближения).

<details>
<summary>Таблица времён работы (в секундах).</summary>

| N      | standard | simple | advanced |
|--------|----------|--------|----------|
| **1**  | 16.52    | 18.37  | 701.15   |
| **2**  | 16.47    | 18.50  | 323.44   |
| **3**  | 16.45    | 18.38  | 213.40   |
| **5**  | 16.38    | 18.41  | 126.53   |
| **10** | 16.37    | 18.35  | 60.90    |
| **20** | 16.38    | 18.38  | 28.16    |
| **30** | 16.41    | 18.35  | 18.12    |
| **50** | 16.30    | 18.53  | 10.51    |

</details>

Можно видеть, что ```standard``` и ```simple``` всегда работают одинаковое время, причем ```standard``` немного быстрее,
а ```advanced``` работает очень долго при малых коэффициентах сжатия, но куда быстрее (и даже быстрее, чем ```standard```) при больших.
