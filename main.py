import base64
import os
import time
import cv2

import keyboard
import pyautogui

import requests

import obs_grapper

api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


result = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (576, 324))


history = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are assisting in playing Baba is You. Your task is to write only keys to control the actions. Do not provide any explanations, additional text, or special symbols such as backticks."
        },
        {
          "type": "text",
          "text": "The main keys is w a s d z, write only one key"
        }
      ]
    },
]
image_path = "test_screenshot.png"


while True:
    obs_grapper.get()
    base64_image = encode_image(image_path)
    f = cv2.imread("test_screenshot.png")
    f = cv2.resize(f, (576, 324))
    result.write(f)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    history.append(
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "next action"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
    )
    payload = {
      "model": "gpt-4o",
      "messages": history,
      "max_tokens": 5
    }

    if len(history) >= 4:
        history.pop(1)
        history.pop(1)

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    prev = str(response.json()["choices"][0]['message']["content"])
    print(prev)
    history.append(
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": prev
            },
          ]
        }
    )
    try:
        keyboard.press(prev)
        time.sleep(0.1)
        keyboard.release(prev)
    except Exception as e:
        history.append(
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": e.__str__()
                },
              ]
            }
        )
    if keyboard.is_pressed("q"):
        result.release()
        break
