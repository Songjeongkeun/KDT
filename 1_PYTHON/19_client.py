import gradio as gr
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL=os.getenv("AD_API_URL")

def generate_ad(product_name, details, tone_and_manner):
    product_name = (product_name or "").strip() 
    details = (details or "").strip()
    tone_and_manner = tone_and_manner or []
    
    if not product_name:
        return "제품 이름을 입력하세요", []
    
    if not details:
        return "제품의 주요 내용을 입력하세요", []
    
    if not tone_and_manner:
        return "광고 문구의 느낌을 한 개 이상 선택하세요", []

    request_data = {
        "product_name": product_name,
        "details": details,
        "tone_and_manner": ",".join(tone_and_manner)
    }
    
    try:
        response = requests.post(API_URL, json=request_data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        ad = result.get("ad", "")
        datas = result.get("datas", [])
        
        if not ad:
            return "서버에서 광고 문구를 받지 못했습니다"
        
        processed_datas = [
            [
                data.get("product_name", ""),
                data.get("details", ""),
                data.get("tone_and_manner", ""),
                data.get("ad", "")
            ]for data in datas
        ]
        return ad, processed_datas
    
    except requests.exceptions.ConnectionError:
        return "FastAPI 서버에 연결할 수 없습니다."
    except requests.exceptions.Timeout:
        return "서버의 응답 시간이 초과되었습니다."
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            detail = e.get("detail", "서버 요청 처리 중 오류가 발생했습니다.")
        except ValueError:
            detail = "서버 요청 처리 중 오류가 발생했습니다."
            return f'서버 오류 {detail}'
    except Exception as e:
        print(f'알 수 없는 오류: {e}')
        
with gr.Blocks(title="AI 광고 문구 생성기") as demo:
    gr.Markdown(
    """
    # AI 광고 문구 생성기
    제품의 이름과 주요 특징을 입력하고 원하는 광고 부누이기를 선택하세요.
    AI가 입력 내용을 분석하여 한 문장의 광고 문구를 생성합니다.
    """
    )
    with gr.Row():
        product_input = gr.Textbox(label="제품 이름", placeholder="제품 이름을 입력하세요")
        details_input = gr.Textbox(label="주요 내용", placeholder="제품의 특징과 장점을 입력하세요")
    
    tone_options = gr.CheckboxGroup(label="광고 문구의 느낌", choices=["재밌게", "과장스럽게", "참신하게", "고급스럽게", "센스있게", "신선하게", "전문성있게"], value=["참신하게"])
    
    generate_button = gr.Button("광고 문구 생성하기", variant="primary")
    output_ad = gr.Textbox(label="생성된 광고 문구", lines=3, interactive=False)
    output_table = gr.DataFrame(label="최근 생성 데이터", headers=["제품 이름", "주요 내용", "광고 문구의 느낌", "생성된 광고 문구"],datatype=["str", "str", "str", "str"], wrap=True, interactive=False)
    
    generate_button.click(fn=generate_ad, inputs=[product_input, details_input, tone_options], outputs=[output_ad, output_table])
    
    demo.launch()