import sass
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_SRC = os.path.join(BASE_DIR, 'static/scss')   # مجلد SCSS
STATIC_OUT = os.path.join(BASE_DIR, 'static/css')    # مجلد CSS الناتج

sass.compile(
    dirname=(STATIC_SRC, STATIC_OUT),
    output_style='compressed'
)

print("✔ تم تحويل SCSS إلى CSS بنجاح.")
