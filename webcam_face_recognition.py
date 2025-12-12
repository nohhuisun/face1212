import streamlit as st
from PIL import Image
import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
import time

# ====================================================================
# 1. 환경 설정 및 클라이언트 초기화
# ====================================================================

# .env 파일 로드 (로컬 테스트용)
load_dotenv()
# Streamlit Cloud에서는 Secrets를 사용합니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

gemini_client = None
GEMINI_MODEL = 'gemini-2.5-flash' 

if GEMINI_API_KEY:
    try:
        # Streamlit Cloud는 secrets.toml에 설정된 키를 환경 변수로 자동 로드합니다.
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        st.error("Gemini 클라이언트 초기화 오류: API 키를 확인해주세요.")
else:
    st.warning("⚠️ GEMINI_API_KEY가 설정되지 않아 AI 분석을 실행할 수 없습니다. Secrets 설정을 확인하세요.")


# ====================================================================
# 2. Gemini API 분석 함수 (전문적인 프롬프트 재사용)
# ====================================================================

def analyze_physiognomy_with_gemini(image_bytes):
    """
    Gemini API를 호출하여 이미지 분석 및 전문적인 관상 정보를 생성합니다.
    (이전 FastAPI 코드에서 사용하신 전문 프롬프트와 유사하게 구성됩니다.)
    """
    
    if gemini_client is None:
        return "API 키가 유효하지 않아 AI 분석 기능을 사용할 수 없습니다."
        
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # 전문적인 관상 분석 프롬프트
        prompt = (
            "당신은 30년 경력의 전문 관상가입니다. 이 사진 속 얼굴을 전통 관상학의 관점에서 깊이 있게 분석해주세요. "
            "분석 결과를 Streamlit의 Markdown 기능을 활용할 수 있도록 다음 항목들을 포함하여 자세하고 구체적으로 작성하고, 각 항목의 제목은 '**[항목명]**' 형식의 굵은 글씨로 시작해주세요:\n\n"
            
            "**[ 얼굴형 및 골격 분석 ]**\n"
            "- 얼굴형(둥근형, 각진형, 계란형 등)과 그 의미\n"
            "- 이마, 광대뼈, 턱선의 특징과 운세적 해석\n\n"
            
            "**[ 오관(五官) 분석 ]**\n"
            "1. 눈: 눈의 크기, 형태, 눈빛의 인상과 성격/재물운 관계\n"
            "2. 코: 콧대와 콧방울의 형태, 재물운과 건강운\n"
            "3. 입: 입술 두께와 입꼬리, 대인관계운과 언변\n"
            "4. 귀: 귀의 위치와 크기, 장수와 복록\n"
            "5. 눈썹: 형태와 농도, 형제운과 사회적 성공\n\n"
            
            "**[ 삼정(三停) 분석 ]**\n"
            "- 상정(이마): 초년운(1~30세), 지혜와 명예\n"
            "- 중정(눈~코): 중년운(31~50세), 재물과 권력\n"
            "- 하정(입~턱): 말년운(51세 이후), 건강과 자손복\n\n"
            
            "**[ 종합 운세 및 조언 ]**\n"
            "- 전체적인 인상과 기색\n"
            "- 성격적 특징 3가지\n"
            "- 적합한 직업군 또는 인생 방향\n"
            "- 관상학적 개선 방법 또는 개운법\n"
            
            "총 500자 이상으로 구체적이고 전문적으로 작성해주세요."
        )

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt, img]
        )
        
        return response.text.strip()
        
    except APIError as e:
        # 오류 발생 시 사용자에게 친절한 메시지 반환
        return f"**[ API 통신 오류 ]**\n\nGemini API 호출에 실패했습니다. 코드를 확인해주세요. (오류 상세: {str(e)})"
    except Exception as e:
        return f"**[ 분석 처리 오류 ]**\n\n이미지 처리 중 예상치 못한 오류가 발생했습니다. (오류 상세: {type(e).__name__} 발생: {str(e)})"

# ====================================================================
# 3. Streamlit 앱 메인 로직
# ====================================================================

st.set_page_config(page_title="AI 관상 전문가", layout="centered")
st.title("✨ AI 관상 전문가")
st.markdown("---")

st.markdown("""
    **안내:** 관상 분석을 위해 [사진 촬영] 버튼을 눌러 **정면 사진을 캡처**해 주세요.
    (Streamlit Cloud는 실시간 웹캠 스트리밍 대신 사진 캡처 기능을 사용합니다.)
""")

# Streamlit의 웹캠 입력 컴포넌트 (FastAPI의 웹소켓 스트리밍 대체)
uploaded_file = st.camera_input("📸 사진 촬영 버튼", help="웹캠을 활성화하고 캡처합니다.")

# 캡처된 파일이 있을 경우 분석 시작
if uploaded_file is not None:
    st.info("✅ 사진이 캡처되었습니다. AI 관상 분석을 시작합니다.")
    
    # 이미지 바이트 읽기
    image_bytes = uploaded_file.read()
    
    # 캡처된 이미지를 화면에 표시
    st.image(image_bytes, caption='캡처된 사진', use_column_width=True)
    
    # 분석 실행 및 로딩 상태 표시
    with st.spinner('Gemini AI가 전문적인 관상 보고서를 작성 중입니다... (잠시만 기다려주세요)'):
        start_time = time.time()
        analysis_report = analyze_physiognomy_with_gemini(image_bytes)
        end_time = time.time()

    st.subheader("📊 관상 분석 보고서")
    
    # Streamlit은 Markdown 포맷을 자동으로 렌더링하여 전문적인 보고서처럼 보여줍니다.
    st.markdown(analysis_report)
    
    st.success(f"분석 완료! (처리 시간: {end_time - start_time:.2f}초)")

st.markdown("---")
st.caption("본 분석은 AI 기반의 관상학적 해석이며, 재미로 참고해 주시기 바랍니다.")