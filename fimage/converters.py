import numpy as np


def rgb2hsv(rgb: np.ndarray) -> np.ndarray:
    axis = rgb.ndim - 1

    rgb = rgb.astype(np.float32) / 255
    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]

    max_array = rgb.max(axis=axis)
    min_array = rgb.min(axis=axis)

    v = max_array
    d = max_array - min_array
    d[d == 0] = 1

    s = np.where(max_array == 0, 0, d / max_array)

    h = np.zeros_like(s)

    np.putmask(h, max_array == r, ((g - b) / d) + np.where(g < b, 6, 0).astype(np.float32))
    np.putmask(h, max_array == g, (b - r) / d + 2)
    np.putmask(h, max_array == b, (r - g) / d + 4)

    h = h / 6
    return np.dstack([h, s, v])
    
    
def hsv2rgb(hsv: np.ndarray) -> np.ndarray:
    input_shape = hsv.shape
    hsv = hsv.reshape(-1, 3)
    h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]

    i = np.int32(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    rgb = np.zeros_like(hsv)
    v, t, p, q = v.reshape(-1, 1), t.reshape(-1, 1), p.reshape(-1, 1), q.reshape(-1, 1)
    rgb[i == 0] = np.hstack([v, t, p])[i == 0]
    rgb[i == 1] = np.hstack([q, v, p])[i == 1]
    rgb[i == 2] = np.hstack([p, v, t])[i == 2]
    rgb[i == 3] = np.hstack([p, q, v])[i == 3]
    rgb[i == 4] = np.hstack([t, p, v])[i == 4]
    rgb[i == 5] = np.hstack([v, p, q])[i == 5]
    rgb[s == 0.0] = np.hstack([v, v, v])[s == 0.0]

    return rgb.reshape(input_shape)