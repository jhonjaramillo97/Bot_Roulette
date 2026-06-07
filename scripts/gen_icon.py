from PIL import Image
import os, shutil, struct, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "bot_ruleta")

logo_path = os.path.join(BASE, "dashboard", "static", "logo.png")
ico_path = os.path.join(BASE, "icon.ico")
favicon_path = os.path.join(BASE, "dashboard", "static", "favicon.ico")

img = Image.open(logo_path).convert('RGBA')

# Sizes que Windows necesita para verse bien en todas partes
sizes = [16, 24, 32, 48, 64, 128, 256]

# Construir ICO manualmente con PNG comprimido para cada tamano
# ICO format: Header + Directory entries + Image data
icon_dir = []  # (width, height, png_data)
for s in sizes:
    resized = img.resize((s, s), Image.LANCZOS)
    buf = io.BytesIO()
    resized.save(buf, format='PNG')
    png_data = buf.getvalue()
    icon_dir.append((s, s, png_data))

# ICO Header: reserved(2) + type(2) + count(2)
num_images = len(icon_dir)
header = struct.pack('<HHH', 0, 1, num_images)

# Calculate offsets
dir_size = 6 + num_images * 16  # header + entries
offset = dir_size

entries = b''
image_data = b''
for w, h, png in icon_dir:
    bw = 0 if w >= 256 else w   # 0 means 256 in ICO format
    bh = 0 if h >= 256 else h
    entry = struct.pack('<BBBBHHII',
        bw,              # width
        bh,              # height
        0,               # color palette
        0,               # reserved
        1,               # color planes
        32,              # bits per pixel
        len(png),        # size of image data
        offset           # offset to image data
    )
    entries += entry
    image_data += png
    offset += len(png)

ico_bytes = header + entries + image_data

with open(ico_path, 'wb') as f:
    f.write(ico_bytes)

print(f"icon.ico creado: {os.path.getsize(ico_path)} bytes ({len(icon_dir)} resoluciones)")
for w, h, png in icon_dir:
    print(f"  - {w}x{h}: {len(png)} bytes")

# Copiar como favicon
shutil.copy2(ico_path, favicon_path)
print(f"favicon.ico copiado")
