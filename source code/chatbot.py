import openai
from apikey import api_data
import pytesseract
from tkinter.filedialog import askopenfilename
from PIL import Image

openai.api_key = api_data

messages = []
print("Import picture to extract...")


def open_image():
    file_path = askopenfilename()
    return Image.open(file_path)


def process_image(image):
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(image, lang='eng')
    print(text)
    pass


if __name__ == '__main__':
    image = open_image()
    if image:
        process_image(image)  
    while True:
        message = input()
        if message.lower() == "quit()":
            break

        messages.append({"role": "user", "content": message})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")
