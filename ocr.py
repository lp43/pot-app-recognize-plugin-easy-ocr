import sys
import json
import easyocr
import os

# 語言映射
LANG_MAP = {
    'zh': 'ch_sim',
    'zh_cn': 'ch_sim', # 簡中  
    'zh_tw': 'ch_tra', # 繁中  
    'auto': 'ch_tra',
    'en': 'en',      # 英文       
    'ja': 'ja',      # 日文
    'ko': 'ko',      # 韓文
    'fr': 'fr',      # 法文
    'de': 'de'      # 德文
}

def ocr(image_path: str, lang: str = 'en') -> dict:
    try:
        # 指定模型路徑（預載）
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(plugin_dir, 'models')
        if not os.path.exists(model_dir):
            print("No local models found, downloading...")
            model_dir = None

        if lang == 'auto':
            # 自動偵測：試英文、簡中、繁中，選信心高的（但每個 Reader 都加 'en' 輔助）
            print("Initializing EasyOCR... Downloading models if needed (this may take 1-2 minutes).")

            # 試英文 + 輔助（純 en）
            reader_en = easyocr.Reader(['en'], model_storage_directory=model_dir, gpu=False)
            results_en = reader_en.readtext(image_path)
            avg_conf_en = sum(result[2] for result in results_en) / max(1, len(results_en))

            # 試英文 + 簡中
            reader_sim = easyocr.Reader(['en', 'ch_sim'], model_storage_directory=model_dir, gpu=False)
            results_sim = reader_sim.readtext(image_path)
            avg_conf_sim = sum(result[2] for result in results_sim) / max(1, len(results_sim))

            # 試英文 + 繁中
            reader_tra = easyocr.Reader(['en', 'ch_tra'], model_storage_directory=model_dir, gpu=False)
            results_tra = reader_tra.readtext(image_path)
            avg_conf_tra = sum(result[2] for result in results_tra) / max(1, len(results_tra))

            # 選最高信心
            scores = [('en', avg_conf_en, results_en), ('ch_sim', avg_conf_sim, results_sim), ('ch_tra', avg_conf_tra, results_tra)]
            best_lang, best_conf, best_results = max(scores, key=lambda x: x[1])
            lang = best_lang
            results = best_results
            print(f"Auto detected: {lang} (conf: {best_conf:.2f})")
        else:
            lang = LANG_MAP.get(lang, lang)
            print("Initializing EasyOCR... Downloading models if needed (this may take 1-2 minutes).")

            # 中文相關語言加載 'en' 輔助；其他語言單一
            languages = [lang]
            if lang in ['ch_sim', 'ch_tra', 'zh', 'zh_cn', 'zh_tw']:  # 中文時加 en
                languages.insert(0, 'en')  # 加 en 為主（優先英文）
            reader = easyocr.Reader(languages, model_storage_directory=model_dir, gpu=False)
            results = reader.readtext(image_path)

        print("Model loaded. Starting OCR...")

        data = [{"text": result[1]} for result in results if result[2] > 0.5]  # 每行一個 {"text": "..."}
        print("OCR init completed.")  # split 點，像 Paddle
        print(json.dumps({"data": data}))  # JSON 輸出，main.js 解析

        return {"data": data}
    except Exception as e:
        raise Exception(f"OCR Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ocr.py <image_path> <lang>")
        sys.exit(1)
    image_path = sys.argv[1]
    lang = sys.argv[2]
    ocr(image_path, lang)  # 呼叫，自動印 JSON