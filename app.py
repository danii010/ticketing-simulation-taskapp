"""
Streamlit 배포용 티켓팅 시뮬레이션 앱
- index.html 내 로컬 이미지 파일 참조(hongik_poster.png)를
  base64 데이터 URI로 자동 치환하여 Streamlit Cloud에서 동작하도록 합니다.
"""

import base64
import pathlib
import re
import streamlit as st
import streamlit.components.v1 as components

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="티켓팅 시뮬레이션",
    page_icon="🎫",
    layout="centered",
)

# Streamlit 자체 헤더·푸터·패딩 숨기기 (풀스크린 느낌)
hide_streamlit_style = """
<style>
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# ── 이미지 → base64 변환 헬퍼 ────────────────────────────────
def image_to_data_uri(image_path: pathlib.Path) -> str:
    """로컬 이미지 파일을 base64 data URI 문자열로 변환합니다."""
    suffix = image_path.suffix.lower().lstrip(".")
    mime_map = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif", "webp": "webp"}
    mime = mime_map.get(suffix, "png")
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime};base64,{encoded}"


# ── index.html 읽기 및 이미지 치환 ───────────────────────────
base_dir = pathlib.Path(__file__).parent

html_path = base_dir / "index.html"
html_content = html_path.read_text(encoding="utf-8")

# 프로젝트 폴더 내 PNG/JPG/WEBP 파일을 모두 찾아서 치환
for img_file in base_dir.glob("**/*.png"):
    data_uri = image_to_data_uri(img_file)
    relative_name = img_file.name
    # CSS url('...') 형태 치환
    html_content = html_content.replace(f"url('{relative_name}')", f"url('{data_uri}')")
    html_content = html_content.replace(f'url("{relative_name}")', f'url("{data_uri}")')
    # HTML src="..." 형태 치환
    html_content = html_content.replace(f'src="{relative_name}"', f'src="{data_uri}"')
    html_content = html_content.replace(f"src='{relative_name}'", f"src='{data_uri}'")

for img_file in base_dir.glob("**/*.jpg"):
    data_uri = image_to_data_uri(img_file)
    relative_name = img_file.name
    html_content = html_content.replace(f"url('{relative_name}')", f"url('{data_uri}')")
    html_content = html_content.replace(f'url("{relative_name}")', f'url("{data_uri}")')
    html_content = html_content.replace(f'src="{relative_name}"', f'src="{data_uri}"')
    html_content = html_content.replace(f"src='{relative_name}'", f"src='{data_uri}'")

# ── Streamlit에 HTML 렌더링 ───────────────────────────────────
# scrolling=True, height=900 으로 앱 전체가 보이도록 설정
components.html(html_content, height=950, scrolling=True)
