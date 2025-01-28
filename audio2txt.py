import os
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator

def convert_audio_to_text(audio_path, language="en-US"):
    """
    将音频文件转换为文本
    :param audio_path: 音频文件路径
    :param language: 语言代码，默认为英文（en-US），中文为 zh-CN
    :return: 转换后的文本
    """
    # 初始化识别器
    recognizer = sr.Recognizer()

    # 加载音频文件
    try:
        # 使用 pydub 处理音频文件
        audio = AudioSegment.from_file(audio_path)
        # 将音频转换为 WAV 格式（SpeechRecognition 只支持 WAV）
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export("temp.wav", format="wav")

        # 使用 SpeechRecognition 读取 WAV 文件
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)

        # 识别音频内容
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except Exception as e:
        return f"转换失败: {str(e)}"
    finally:
        # 删除临时文件
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")

def translate_text(text, target_language="zh-CN"):
    """
    将文本翻译为目标语言
    :param text: 需要翻译的文本
    :param target_language: 目标语言代码，默认为中文（zh-CN）
    :return: 翻译后的文本
    """
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"翻译失败: {str(e)}"

def main():
    # 获取用户输入的音频文件路径
    audio_path = input("请输入音频文件路径（支持 .ogg, .mp3, .m4a, .wav 等格式）: ").strip()

    # 检查文件是否存在
    if not os.path.exists(audio_path):
        print("文件不存在，请检查路径是否正确。")
        return

    # 选择语言
    language = input("请选择语言（1: 英文, 2: 中文）: ").strip()
    if language == "1":
        language_code = "en-US"  # 英文
        target_language = "en"
    elif language == "2":
        language_code = "en-US"  # 先识别为英文
        target_language = "zh-CN"  # 然后翻译为中文
    else:
        print("选择无效，默认使用英文。")
        language_code = "en-US"
        target_language = "en"

    # 转换音频为文本
    print("正在转换，请稍候...")
    result = convert_audio_to_text(audio_path, language_code)

    # 如果用户选择中文且源语言是英文，则翻译文本
    if target_language == "zh-CN" and language_code == "en-US":
        print("正在翻译为中文...")
        result = translate_text(result, target_language)

    print("转换结果：")
    print(result)

if __name__ == "__main__":
    main()
