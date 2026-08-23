import cv2
import numpy as np
import os

def create_synthetic_finger():
    # Create blank image (dark background)
    height, width = 640, 480
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (30, 30, 30)  # Dark gray background
    
    # Draw "finger" (ellipse)
    center = (width // 2, height // 2 + 100)
    axes = (100, 300)
    angle = 0
    color = (180, 200, 220)  # Skin-ish tone (in BGR)
    cv2.ellipse(image, center, axes, angle, 0, 360, color, -1)
    
    # Add some "ridges" (noise/lines)
    rng = np.random.default_rng()
    noise = rng.integers(0, 50, (height, width), dtype=np.uint8)
    noise_colored = cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)
    
    # Blend noise into finger area
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.ellipse(mask, center, axes, angle, 0, 360, 255, -1)
    mask_inv = cv2.bitwise_not(mask)
    
    finger_area = cv2.bitwise_and(image, image, mask=mask)
    finger_with_noise = cv2.addWeighted(finger_area, 0.9, cv2.bitwise_and(noise_colored, noise_colored, mask=mask), 0.1, 0)
    
    final_image = cv2.add(finger_with_noise, cv2.bitwise_and(image, image, mask=mask_inv))
    
    # Save
    os.makedirs("fingers", exist_ok=True)
    cv2.imwrite("fingers/synthetic_thumb.jpg", final_image)
    print("Created fingers/synthetic_thumb.jpg")

if __name__ == "__main__":
    create_synthetic_finger()
