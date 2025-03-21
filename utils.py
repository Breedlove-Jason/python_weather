import cairosvg
from PIL import Image, ImageTk
import io


def load_svg_as_photoimage(svg_path, size=(50, 50)):
    try:
        # Convert SVG to PNG in-memory
        png_data = cairosvg.svg2png(url=svg_path, output_width=size[0], output_height=size[1])

        # Open as PIL Image from bytes
        img = Image.open(io.BytesIO(png_data))

        # Optional resize (you already control output size above, so may not need this)
        img = img.resize(size)

        # Convert to Tkinter PhotoImage
        return ImageTk.PhotoImage(img)

    except Exception as e:
        print(f"Error loading SVG: {e}")
        return None