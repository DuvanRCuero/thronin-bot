import cv2 as cv
from thronin.lib.logger import logger


class CachedImages:
    def __init__(self):
        self._cached_images = {}

    def get_cached_image(self, path):
        # Cache the image if not already cached
        if path not in self._cached_images:
            logger.debug(f"Caching Image: {path}")
            self._cached_images[path] = cv.imread(path, cv.IMREAD_COLOR)

        # Ensure the image was successfully loaded
        if self._cached_images[path] is None:
            raise ValueError(f"'{path}' could not be loaded.")

        return self._cached_images[path]


# Pre-create an instance
cached_images = CachedImages()
