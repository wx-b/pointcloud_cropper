import pointcloud_cropper as pc
import numpy as np
import time


def np_get_crop_index(points, x_min, y_min, z_min, x_max, y_max, z_max):
    indices = np.where((points[:, 0] >= x_min) & (points[:, 0] <= x_max)
                       & (points[:, 1] >= y_min) & (points[:, 1] <= y_max)
                       & (points[:, 2] >= z_min) & (points[:, 2] <= z_max))
    return np.array(indices).ravel()


def run_benchmark():
    # Set up data.
    np.random.seed(0)
    points = np.random.rand(int(1e8), 3)
    x_min = 0.25
    y_min = 0.25
    z_min = 0.25
    x_max = 0.75
    y_max = 0.75
    z_max = 0.75

    # Crop with numpy.
    s = time.time()
    index_np = np_get_crop_index(points=points,
                                 x_min=x_min,
                                 y_min=y_min,
                                 z_min=z_min,
                                 x_max=x_max,
                                 y_max=y_max,
                                 z_max=z_max)
    print("Time with numpy", time.time() - s)
    print(index_np.shape)

    # Crop impl with TBB.
    s = time.time()
    index_tbb = pc.get_crop_index(points=points,
                                  x_min=x_min,
                                  y_min=y_min,
                                  z_min=z_min,
                                  x_max=x_max,
                                  y_max=y_max,
                                  z_max=z_max)
    print("Time with TBB", time.time() - s)
    print(index_tbb.shape)

    # Crop serial impl.
    s = time.time()
    index_serial = pc.get_crop_index_serial(points=points,
                                            x_min=x_min,
                                            y_min=y_min,
                                            z_min=z_min,
                                            x_max=x_max,
                                            y_max=y_max,
                                            z_max=z_max)
    print("Time with serial impl", time.time() - s)
    print(index_serial.shape)

    if np.allclose(index_np, index_tbb) and np.allclose(
            index_np, index_serial):
        print("Equal")


if __name__ == "__main__":
    run_benchmark()