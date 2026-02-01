import os
import io
import base64
import logging
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VisualElementGenerator:
    """Generate visual micro-elements for the dashboard PDF."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def create_fingerprint_badge(self, size: Tuple[int, int] = (200, 200), 
                                color: str = '#3498DB') -> str:
        """Create a fingerprint pattern badge using Pillow."""
        try:
            # Create base image with transparent background
            img = Image.new('RGBA', size)
            img.putalpha(0)  # Make transparent
            draw = ImageDraw.Draw(img)
            
            # Draw fingerprint pattern (simplified)
            center_x, center_y = size[0] // 2, size[1] // 2
            radius = min(size) // 3
            
            # Draw concentric circles for fingerprint effect
            for i in range(5):
                r = radius - i * 10
                if r > 0:
                    draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                               outline=color, width=2)
            
            # Add some ridge lines
            for i in range(8):
                angle = i * 45
                x1 = center_x + int(radius * 0.7 * np.cos(np.radians(angle)))
                y1 = center_y + int(radius * 0.7 * np.sin(np.radians(angle)))
                x2 = center_x + int(radius * 0.9 * np.cos(np.radians(angle)))
                y2 = center_y + int(radius * 0.9 * np.sin(np.radians(angle)))
                draw.line([x1, y1, x2, y2], fill=color, width=1)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            self.logger.error(f"Error creating fingerprint badge: {e}")
            return ""
    
    def create_brain_badge(self, size: Tuple[int, int] = (200, 200), 
                          color: str = '#E74C3C') -> str:
        """Create a brain pattern badge using Pillow."""
        try:
            # Create base image with transparent background
            img = Image.new('RGBA', size)
            img.putalpha(0)  # Make transparent
            draw = ImageDraw.Draw(img)
            
            # Draw brain outline (simplified)
            center_x, center_y = size[0] // 2, size[1] // 2
            width, height = size[0] // 2, size[1] // 2
            
            # Brain shape points
            points = [
                (center_x - width//2, center_y - height//3),
                (center_x - width//3, center_y - height//2),
                (center_x - width//4, center_y),
                (center_x - width//3, center_y + height//2),
                (center_x - width//2, center_y + height//3),
                (center_x + width//2, center_y + height//3),
                (center_x + width//3, center_y + height//2),
                (center_x + width//4, center_y),
                (center_x + width//3, center_y - height//2),
                (center_x + width//2, center_y - height//3),
            ]
            
            # Draw brain outline
            draw.polygon(points, outline=color, width=3)
            
            # Add brain folds
            for i in range(3):
                y_offset = (i - 1) * height // 4
                draw.line([(center_x - width//3, center_y + y_offset),
                          (center_x + width//3, center_y + y_offset)], 
                         fill=color, width=1)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            self.logger.error(f"Error creating brain badge: {e}")
            return ""
    
    def create_roadmap_badge(self, size: Tuple[int, int] = (200, 200), 
                            color: str = '#27AE60') -> str:
        """Create a roadmap pattern badge using Pillow."""
        try:
            # Create base image with transparent background
            img = Image.new('RGBA', size)
            img.putalpha(0)  # Make transparent
            draw = ImageDraw.Draw(img)
            
            # Draw roadmap path
            start_x, start_y = size[0] // 4, size[1] // 2
            end_x, end_y = 3 * size[0] // 4, size[1] // 2
            
            # Main path
            draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=4)
            
            # Add waypoints
            waypoints = [
                (start_x + (end_x - start_x) // 4, start_y),
                (start_x + 2 * (end_x - start_x) // 4, start_y),
                (start_x + 3 * (end_x - start_x) // 4, start_y),
            ]
            
            for wp_x, wp_y in waypoints:
                draw.ellipse([wp_x - 8, wp_y - 8, wp_x + 8, wp_y + 8], 
                           fill=color, outline='white', width=2)
            
            # Add arrows
            for i in range(3):
                x = start_x + (i + 1) * (end_x - start_x) // 4
                draw.polygon([(x - 10, start_y - 5), (x + 10, start_y), (x - 10, start_y + 5)], 
                           fill=color)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            self.logger.error(f"Error creating roadmap badge: {e}")
            return ""
    
    def create_gradient_banner(self, width: int = 800, height: int = 60, 
                              start_color: str = '#3498DB', 
                              end_color: str = '#2980B9') -> str:
        """Create a gradient banner for charts."""
        try:
            # Create gradient image with transparent background
            img = Image.new('RGBA', (width, height))
            img.putalpha(0)  # Make transparent
            draw = ImageDraw.Draw(img)
            
            # Create gradient effect
            for y in range(height):
                ratio = y / height
                r1, g1, b1 = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
                r2, g2, b2 = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)
                
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b, 180))  # Semi-transparent
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            self.logger.error(f"Error creating gradient banner: {e}")
            return ""
    
    def get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level."""
        if confidence >= 80:
            return '#27AE60'  # Green
        elif confidence >= 60:
            return '#F39C12'  # Amber
        else:
            return '#E74C3C'  # Red
    
    def create_confidence_indicator(self, confidence: float, 
                                  size: Tuple[int, int] = (100, 20)) -> str:
        """Create a confidence indicator badge."""
        try:
            # Create base image with transparent background
            img = Image.new('RGBA', size)
            img.putalpha(0)  # Make transparent
            draw = ImageDraw.Draw(img)
            
            # Get color based on confidence
            color = self.get_confidence_color(confidence)
            
            # Draw progress bar
            progress_width = int(size[0] * confidence / 100)
            draw.rectangle([0, 0, progress_width, size[1]], fill=color)
            draw.rectangle([0, 0, size[0], size[1]], outline='black', width=1)
            
            # Add text
            try:
                font = ImageFont.load_default()
                text = f"{confidence:.0f}%"
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                text_x = (size[0] - text_width) // 2
                text_y = (size[1] - text_height) // 2
                
                draw.text((text_x, text_y), text, fill='black', font=font)
            except:
                # Fallback if font loading fails
                pass
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            self.logger.error(f"Error creating confidence indicator: {e}")
            return "" 