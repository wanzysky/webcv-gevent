# Webcv-gevent

This is an mirror implementation of [webcv](https://github.com/wanzysky/webcv) using gevent and Flask to support older version of Python (< 3.7). The usage is the same with webcv and diplaying of images, text, and tables is also supported:

```python
import webcv2 as cv2

cv2.head_show("h1", "Showing an image in browser.")
cv2.imshow("image", cv2.imread("your-image.jpg"))
cv2.waitKey()
```

**You may need `pip install -r requirements.txt` to install dependencies.**
