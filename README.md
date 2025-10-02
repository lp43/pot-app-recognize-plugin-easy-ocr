# Pot-App EasyOCR 插件v1.0.0 (基于 [EasyOCR](https://github.com/JaidedAI/EasyOCR))

> [!NOTE]
> 该插件支持跨平台 (Windows/macOS/Linux)，但需要系统安装 Python 3.8+ 和 EasyOCR 库。

## 安装依赖
1. 安装 Python 3.8+（从 [python.org](https://www.python.org/) 下载）。
2. 在终端执行：`pip install easyocr`（首次使用会下载语言模型 ~500MB）。
3. 如果有 NVIDIA GPU，可安装 CUDA 版 PyTorch 以加速：`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`。

## 使用方法
1. 下载对应平台的插件，解压得到 `.potext` 文件（包含 ocr.py、info.json 等）。
2. 打开 Pot - 偏好设置 - 服务设置 - 文字识别 - 添加外部插件 - 安装外部插件。
3. 选择刚刚解压得到的 `.potext` 文件，安装成功。
4. 在文字识别服务列表中添加 EasyOCR 即可使用（在设置中指定 Python 路径如果需要）。
5. 测试：按快捷键截图 OCR，选择 EasyOCR 引擎。

## 支持语言
EasyOCR 支持 80+ 语言，包括中文（简/繁）、英文、日文、韩文、法文、德文…等。插件会自动映射 Pot 的语言代码。

## 語系自動偵測
目前支援 中文（简/繁）、英文 三種語系的自動偵測。

