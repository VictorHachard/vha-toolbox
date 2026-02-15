import math


def _ratio(w, h):
    return w / h if h else 0.0


def should_rotate_by_ratio(
        img,
        frame_img,
        frame_target_ratio: float,
        img_target_ratio: float,
        tol: float = 0.05,
        require_orientation_flip: bool = True,
):
    """
    Determines whether the frame should be rotated based on:

    - the actual frame ratio
    - the actual image ratio
    - the expected target ratios (e.g. 2/3, 3/2, square, etc.)
    - a tolerance
    - and optionally an orientation change (portrait -> landscape)

    Args:
        img (PIL.Image.Image): The original image.
        frame_img (PIL.Image.Image): The frame image.
        frame_target_ratio (float): Expected frame ratio (e.g. 2/3).
        img_target_ratio (float): Expected image ratio (e.g. 3/2).
        tol (float): Relative tolerance when comparing ratios.
        require_orientation_flip (bool): If True, enforces portrait vs landscape mismatch.

    Returns:
        bool: True if the frame should be rotated, False otherwise.

    Example:
        >>> from PIL import Image
        >>> img = Image.new('RGB', (300, 200))  # Landscape image
        >>> frame_img = Image.new('RGB', (200, 300))  # Portrait
        >>> should_rotate_by_ratio(img, frame_img, frame_target_ratio=2/3, img_target_ratio=3/2)
        True
    """
    pw, ph = img.size
    fw, fh = frame_img.size

    img_r = _ratio(pw, ph)
    frame_r = _ratio(fw, fh)

    # square frame → never rotate
    if math.isclose(frame_r, 1.0, rel_tol=tol):
        return False

    # check frame ratio
    frame_match = math.isclose(frame_r, frame_target_ratio, rel_tol=tol)

    # check image ratio
    img_match = math.isclose(img_r, img_target_ratio, rel_tol=tol)

    if not (frame_match and img_match):
        return False

    # if orientation must flip (portrait ↔ landscape)
    if require_orientation_flip:
        frame_is_portrait = fh > fw
        img_is_landscape = pw > ph
        orientation_ok = frame_is_portrait and img_is_landscape
        return orientation_ok

    return True
