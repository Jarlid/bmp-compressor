import sys

from PIL import Image

import numpy as np

STYPE = np.uint32
DTYPE = np.float32
INT_SIZE = FLOAT_SIZE = 4
IMAGE_INT_SIZE = 1


def compress(input_filename, output_filename, function_name, n):
    image = Image.open(input_filename)

    height, width = image.size
    permitted_amount = (width * height * IMAGE_INT_SIZE) // ((width + 1 + height) * INT_SIZE * n) - 1

    function_name = function_name.lower()
    if function_name == "standard":
        func = np.linalg.svd
    elif function_name == "simple":
        exit(459845723)
    elif function_name == "advanced":
        exit(876363467)
    else:
        exit(328472344)

    svd_us = [None] * 3
    svd_ss = [None] * 3
    svd_vhs = [None] * 3

    for i in range(3):
        svd_us[i], svd_ss[i], svd_vhs[i] = func(np.array(image, dtype=DTYPE)[:, :, i], full_matrices=False)

        svd_us[i] = svd_us[i][:, :permitted_amount]
        svd_ss[i] = svd_ss[i][:permitted_amount]
        svd_vhs[i] = svd_vhs[i][:permitted_amount, :]

    compressed_data = bytearray()
    compressed_data.extend(STYPE(height).tobytes())
    compressed_data.extend(STYPE(width).tobytes())
    compressed_data.extend(STYPE(permitted_amount).tobytes())

    for i in range(3):
        compressed_data.extend(svd_us[i].astype(dtype=DTYPE).tobytes())
        compressed_data.extend(svd_ss[i].astype(dtype=DTYPE).tobytes())
        compressed_data.extend(svd_vhs[i].astype(dtype=DTYPE).tobytes())

    with open(output_filename, 'wb') as file:
        file.write(compressed_data)


def decompress(input_filename, output_filename):
    with open(input_filename, 'rb') as file:
        data = file.read()

    width = int(np.frombuffer(data, offset=0, dtype=STYPE, count=1)[0])
    height = int(np.frombuffer(data, offset=INT_SIZE, dtype=STYPE, count=1)[0])
    amount = int(np.frombuffer(data, offset=2 * INT_SIZE, dtype=STYPE, count=1)[0])

    offset = 3 * INT_SIZE

    decompressed_data = [None] * 3

    for i in range(3):
        svd_u = np.frombuffer(data, offset=offset, dtype=DTYPE, count=width * amount).reshape((width, amount))
        offset += svd_u.size * FLOAT_SIZE

        svd_s = np.diag(np.frombuffer(data, offset=offset, dtype=DTYPE, count=amount))
        offset += amount * FLOAT_SIZE

        svd_vh = np.frombuffer(data, offset=offset, dtype=DTYPE, count=height * amount).reshape((amount, height))
        offset += svd_vh.size * FLOAT_SIZE

        decompressed_data[i] = svd_u @ svd_s @ svd_vh

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
