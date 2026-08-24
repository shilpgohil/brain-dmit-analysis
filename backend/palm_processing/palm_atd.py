"""
Geometric atd-angle estimation from a palm image.

This is NOT a dermatoglyphic (ridge-triradius) measurement. Casual palm photos
contain flexion creases, not friction ridges, so the true a/t/d triradii cannot
be recovered. This estimator approximates the atd angle from hand geometry:
it segments the hand, locates the inter-finger webs and the axial region, and
computes the angle at the axial point t between the index-base (a) and
little-base (d) landmarks. Every result carries a confidence; below threshold
the estimate is withheld (returned as None) rather than guessed.
"""
from __future__ import annotations

import logging
import math
from typing import Any, Dict, Optional, Tuple

import cv2  # type: ignore
import numpy as np

logger = logging.getLogger(__name__)

Point = Tuple[int, int]


class PalmAtdEstimator:
    MIN_CONFIDENCE = 0.35
    # Angles outside this band almost certainly reflect estimation error,
    # not real anatomy. Clinical ATD angles range ~25-62 degrees.
    PLAUSIBLE_RANGE = (25.0, 62.0)

    def estimate(self, image_path: str, hand: str) -> Optional[Dict[str, Any]]:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            logger.warning("Palm atd: could not read image %s", image_path)
            return None

        image = self._downscale(image, 900)
        mask = self._segment_hand(image)
        if mask is None:
            return None

        contour = self._largest_contour(mask)
        if contour is None:
            return None

        frame_area = mask.shape[0] * mask.shape[1]
        contour_area = cv2.contourArea(contour)
        if contour_area < 0.05 * frame_area:
            return None

        landmarks = self._atd_landmarks(contour, hand)
        if landmarks is None:
            return None

        a, t, d = landmarks["a"], landmarks["t"], landmarks["d"]
        angle = self._angle_at(t, a, d)
        if angle is None:
            return None

        confidence = self._confidence(landmarks, angle, contour_area, frame_area)
        if confidence < self.MIN_CONFIDENCE:
            logger.info("Palm atd: low confidence %.2f for %s, withholding", confidence, image_path)
            return None

        return {
            "angle_deg": round(float(angle), 1),
            "confidence": round(float(confidence), 3),
            "method": "geometric_landmark",
            "points": {"a": a, "t": t, "d": d},
        }

    @staticmethod
    def _downscale(image: np.ndarray, max_side: int) -> np.ndarray:
        h, w = image.shape[:2]
        scale = max_side / float(max(h, w))
        if scale < 1.0:
            return cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        return image

    @staticmethod
    def _segment_hand(image: np.ndarray) -> Optional[np.ndarray]:
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        skin = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
        kernel = np.ones((5, 5), np.uint8)
        skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, kernel, iterations=2)
        skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), iterations=2)
        if cv2.countNonZero(skin) < 0.03 * skin.size:
            return None
        return skin

    @staticmethod
    def _largest_contour(mask: np.ndarray):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        return max(contours, key=cv2.contourArea)

    def _atd_landmarks(self, contour, hand: str) -> Optional[Dict[str, Any]]:
        points = contour.reshape(-1, 2)
        xs, ys = points[:, 0], points[:, 1]
        x_min, x_max = int(xs.min()), int(xs.max())
        y_min, y_max = int(ys.min()), int(ys.max())
        height = y_max - y_min
        width = x_max - x_min
        if height < 30 or width < 30:
            return None

        cx = int(np.mean(xs))

        webs = self._finger_webs(contour, y_min + 0.55 * height)

        t = self._axial_triradius_point(points, cx, y_min, height)

        if len(webs) >= 2:
            webs_sorted = sorted(webs, key=lambda p: p[0])
            thumb_on_left = hand.lower() == "right"
            if thumb_on_left:
                a = webs_sorted[0]
                d = webs_sorted[-1]
            else:
                a = webs_sorted[-1]
                d = webs_sorted[0]
            web_count = len(webs)
        else:
            base_y = int(y_min + 0.4 * height)
            band = points[np.abs(points[:, 1] - base_y) < max(8, 0.06 * height)]
            if len(band) < 2:
                return None
            left = tuple(band[np.argmin(band[:, 0])])
            right = tuple(band[np.argmax(band[:, 0])])
            if hand.lower() == "right":
                a, d = (int(left[0]), int(left[1])), (int(right[0]), int(right[1]))
            else:
                a, d = (int(right[0]), int(right[1])), (int(left[0]), int(left[1]))
            web_count = 0

        return {
            "a": (int(a[0]), int(a[1])),
            "t": (int(t[0]), int(t[1])),
            "d": (int(d[0]), int(d[1])),
            "web_count": web_count,
        }

    @staticmethod
    def _finger_webs(contour, max_y: float):
        hull = cv2.convexHull(contour, returnPoints=False)
        if hull is None or len(hull) < 4:
            return []
        try:
            defects = cv2.convexityDefects(contour, hull)
        except cv2.error:
            return []
        if defects is None:
            return []

        pts = contour.reshape(-1, 2)
        webs = []
        for i in range(defects.shape[0]):
            # OpenCV 4.x returns shape (N,1,4); OpenCV 5.x can return (N,4).
            # np.ravel handles both — the old "defects[i, 0]" unpacking crashes
            # on 5.x with "cannot unpack non-iterable numpy.int32".
            vals = np.ravel(defects[i])
            if vals.shape[0] < 4:
                continue
            _s, _e, f, depth = (int(v) for v in vals[:4])
            if depth / 256.0 < 20:
                continue
            if f < 0 or f >= len(pts):
                continue
            far = tuple(int(v) for v in pts[f])
            if far[1] <= max_y:
                webs.append(far)
        return webs

    @staticmethod
    def _axial_triradius_point(points: np.ndarray, cx: int, y_min: int, height: int) -> Point:
        """
        Approximate the axial triradius 't' — proximal palm, just above the
        wrist crease, roughly 78-92% of the way down the hand bounding box.
        Uses the median (not max-y) of contour points in this band: max-y is
        unstable and picks stray pixels; median is robust. The band cap at 92%
        also excludes forearm pixels if the photo includes some arm.
        """
        y_low = y_min + 0.78 * height
        y_high = y_min + 0.92 * height
        band = points[(points[:, 1] >= y_low) & (points[:, 1] <= y_high)]
        if len(band) < 2:
            return (cx, int(y_min + 0.85 * height))
        t_x = int(np.median(band[:, 0]))
        t_y = int(np.median(band[:, 1]))
        return (t_x, t_y)

    @staticmethod
    def _angle_at(vertex: Point, p1: Point, p2: Point) -> Optional[float]:
        v1 = (p1[0] - vertex[0], p1[1] - vertex[1])
        v2 = (p2[0] - vertex[0], p2[1] - vertex[1])
        n1 = math.hypot(*v1)
        n2 = math.hypot(*v2)
        if n1 < 1e-6 or n2 < 1e-6:
            return None
        cosang = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
        cosang = max(-1.0, min(1.0, cosang))
        return math.degrees(math.acos(cosang))

    def _confidence(self, landmarks: Dict[str, Any], angle: float,
                    contour_area: float, frame_area: float) -> float:
        score = 0.0
        web_count = landmarks.get("web_count", 0)
        score += min(web_count, 3) / 3.0 * 0.5
        if self.PLAUSIBLE_RANGE[0] <= angle <= self.PLAUSIBLE_RANGE[1]:
            score += 0.3
        area_ratio = contour_area / frame_area
        if 0.1 <= area_ratio <= 0.75:
            score += 0.2
        return max(0.0, min(1.0, score))
