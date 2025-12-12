# 🌟 AI 관상 전문가 (Physiognomy Analyzer with Gemini)

이 프로젝트는 Google의 Gemini 2.5 Flash 모델을 활용하여 사용자의 웹캠 이미지로부터 동양 관상학 기반의 전문적인 분석 보고서를 실시간으로 제공하는 웹 애플리케이션입니다.

FastAPI 및 웹소켓 기반에서 Streamlit Cloud 배포를 위해 **Streamlit 기반 단일 페이지 앱**으로 성공적으로 전환되었습니다.

## ✨ 주요 기능

* **웹캠 이미지 캡처:** Streamlit의 `st.camera_input` 기능을 사용하여 사용자의 얼굴 정면 이미지를 촬영합니다.
* **Gemini Vision 분석:** 캡처된 이미지를 Google Gemini 2.5 Flash 모델로 전송하여 관상 분석을 요청합니다.
* **전문적인 보고서:** 얼굴형, 오관(눈, 코, 입, 귀, 눈썹), 삼정(초/중/말년운) 분석을 포함한 상세하고 전문적인 보고서를 한국어 Markdown 형식으로 제공합니다.
* **클라우드 배포:** Streamlit Community Cloud를 통해 전 세계 어디서든 웹 브라우저로 쉽게 접근 및 사용 가능합니다.

## 🛠️ 기술 스택

| 구분 | 기술 / 라이브러리 | 용도 |
| :--- | :--- | :--- |
| **핵심 AI** | Google Gemini 2.5 Flash | 이미지 분석 및 전문적인 관상학적 텍스트 생성 |
| **웹 프레임워크** | Streamlit | 빠르고 쉬운 웹 UI 구축 및 배포 (Streamlit Cloud 최적화) |
| **API 연동** | `google-genai` SDK | Gemini API 통신 관리 |
| **환경 관리** | `python-dotenv` | 로컬 개발 환경에서 API 키 관리 |

## 🚀 실행 및 배포 가이드

### 1. 로컬 환경에서 실행하기

1.  **가상 환경 설정:**
    ```bash
    conda create -n wapapp01 python=3.11
    conda activate wapapp01
    ```
2.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```
    (또는 직접 설치: `pip install streamlit python-dotenv Pillow google-genai`)
3.  **API 키 설정:**
    프로젝트 루트 폴더에 `.env` 파일을 만들고 Gemini API 키를 입력합니다.
    ```env
    # .env
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
4.  **앱 실행:**
    ```bash
    streamlit run webcam_face_recognition.py
    ```

### 2. Streamlit Cloud 배포 (Final Stage)

이 앱은 Streamlit Cloud에 배포하기 위해 최적화되었습니다.

1.  **GitHub 푸시:** `webcam_face_recognition.py`와 `requirements.txt` 파일을 GitHub에 푸시합니다.
2.  **Streamlit Cloud 로그인 및 Secrets 설정:**
    * Streamlit Cloud 대시보드에서 **Settings** > **Secrets**로 이동합니다.
    * 다음 형식으로 Gemini API 키를 설정합니다.
        ```toml
        # secrets.toml 설정
        GEMINI_API_KEY = "YOUR_API_KEY_HERE"
        ```
3.  **Deploy:** 새 앱을 배포할 때, **Main file path**를 `webcam_face_recognition.py`로 지정하여 배포를 완료합니다.

## 📝 라이선스

[해당 라이선스 정보를 여기에 명시해주세요. 예: MIT License]# face1212
