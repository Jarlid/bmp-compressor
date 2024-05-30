import sys

from PIL import Image

import numpy as np

from time import time

STYPE = np.uint32
DTYPE = np.float32
INT_SIZE = FLOAT_SIZE = 4
IMAGE_INT_SIZE = 1


def standard(matrix):
    return np.linalg.svd(matrix, full_matrices=False)


def simple(matrix):
    eigen_values, eigen_vectors = np.linalg.eig(np.dot(matrix.T, matrix))

    sorted_indices = np.argsort(eigen_values)[::-1]
    eigen_values = eigen_values[sorted_indices]
    eigen_vectors = eigen_vectors[:, sorted_indices]

    u = np.dot(matrix, eigen_vectors)
    u /= np.linalg.norm(u, axis=0)

    return u, np.sqrt(eigen_values), eigen_vectors.T


EPS = 0.1
MAX_ITERATIONS = 17


def advanced_constructor(permitted_amount):
    def v_part():
        tmp = np.random.normal(size=permitted_amount)
        return tmp / np.linalg.norm(tmp)

    def advanced(matrix):
        v = np.matrix([v_part() for _ in range(matrix.shape[1])])

        for _ in range(MAX_ITERATIONS):
            q, _ = np.linalg.qr(matrix @ v)
            u = np.matrix(q[:, 0:permitted_amount])

            q, r = np.linalg.qr(matrix.T @ u)
            v = np.matrix(q[:, 0:permitted_amount])
            s = np.matrix(r[0:permitted_amount, 0:permitted_amount])

            if np.linalg.norm(matrix @ v - u * s) < EPS:
                break

        return u, np.diagonal(s).astype(DTYPE), v.T

    return advanced


def compress(input_filename, output_filename, function_name, n):
    image = Image.open(input_filename)

    width, height = image.size
    permitted_amount = (width * height * IMAGE_INT_SIZE) // ((width + 1 + height) * INT_SIZE * n) - 1

    function_name = function_name.lower()
    if function_name == "standard":
        func = standard
    elif function_name == "simple":
        func = simple
    elif function_name == "advanced":
        func = advanced_constructor(permitted_amount)
    else:
        exit(328472344)

    svd_us = [None] * 3
    svd_ss = [None] * 3
    svd_vhs = [None] * 3

    start_time = time()

    for color in range(3):
        color_matrix = np.array(image, dtype=np.float64)[:, :, color]
        if height > width:
            color_matrix = color_matrix.T

        svd_us[color], svd_ss[color], svd_vhs[color] = func(color_matrix)

        svd_us[color] = svd_us[color][:, :permitted_amount]
        svd_ss[color] = svd_ss[color][:permitted_amount]
        svd_vhs[color] = svd_vhs[color][:permitted_amount, :]

    end_time = time()
    print(f"Timedelta (s): {end_time - start_time}")

    compressed_data = bytearray()
    compressed_data.extend(STYPE(width).tobytes())
    compressed_data.extend(STYPE(height).tobytes())
    compressed_data.extend(STYPE(permitted_amount).tobytes())

    for color in range(3):
        compressed_data.extend(svd_us[color].astype(dtype=DTYPE).tobytes())
        compressed_data.extend(svd_ss[color].astype(dtype=DTYPE).tobytes())
        compressed_data.extend(svd_vhs[color].astype(dtype=DTYPE).tobytes())

    with open(output_filename, 'wb') as file:
        file.write(compressed_data)


def decompress(input_filename, output_filename):
    with open(input_filename, 'rb') as file:
        data = file.read()

    width = int(np.frombuffer(data, offset=0, dtype=STYPE, count=1)[0])
    height = int(np.frombuffer(data, offset=INT_SIZE, dtype=STYPE, count=1)[0])
    amount = int(np.frombuffer(data, offset=2 * INT_SIZE, dtype=STYPE, count=1)[0])

    rotate = False
    if height > width:
        height, width = width, height
        rotate = True

    offset = 3 * INT_SIZE

    decompressed_data = [None] * 3

    for i in range(3):
        svd_u = np.frombuffer(data, offset=offset, dtype=DTYPE, count=height * amount).reshape((height, amount))
        offset += svd_u.size * FLOAT_SIZE

        svd_s = np.diag(np.frombuffer(data, offset=offset, dtype=DTYPE, count=amount))
        offset += amount * FLOAT_SIZE

        svd_vh = np.frombuffer(data, offset=offset, dtype=DTYPE, count=width * amount).reshape((amount, width))
        offset += svd_vh.size * FLOAT_SIZE

        decompressed_data[i] = svd_u @ svd_s @ svd_vh

        if rotate:
            decompressed_data[i] = decompressed_data[i].T

    image = Image.fromarray(np.uint8(np.stack((
        decompressed_data[0],
        decompressed_data[1],
        decompressed_data[2]
    ), axis=-1)))
    image.save(output_filename)


# main.py [input filename] [output filename] [compress/decompress] [standard/simple/advanced] [N: int]
if __name__ == "__main__":
    if sys.argv[3] == "compress":
        compress(sys.argv[1], sys.argv[2],  sys.argv[4], int(sys.argv[5]))
    if sys.argv[3] == "decompress":
        decompress(sys.argv[1], sys.argv[2])
