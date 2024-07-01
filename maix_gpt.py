import requests, time, os
from maix import camera, display, image, nn
from maix import audio, app
# import  ws2812

# class 
# ws2812(led_pin=-1,led_num=-1)#,i2s_num=I2S_DEVICE_2,i2s_chn=I2S_CHANNEL_3,i2s_dma_chn=DMAC_CHANNEL1)

print(os.getcwd())
print(os.path.abspath(os.path.dirname(__file__)))
print(os.listdir('.'))

# # Set your OpenAI API key here
OPENAI_API_KEY = 'your-api-key'

now = time.time()
test_prompt = "What’s the weather in north asia now? Tell me in Chinese."

# Headers
headers = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json'
}

# https://wiki.sipeed.com/maixpy/doc/zh/peripheral/pwm.html
# https://wiki.sipeed.com/maixpy/doc/zh/projects/face_tracking.html
# https://github.com/sipeed/MaixPy/tree/cd09857ccd0fff77c71c6d13be3a1345d97b9392/projects/app_face_tracking
# https://maixhub.com/share/1
# https://wiki.sipeed.com/maixpy/doc/zh/vision/face_detection.html
# https://github.com/sipeed/MaixPy-v1_scripts/blob/master/modules/grove/ws2812/ws2812.py
# https://controllerstech.com/ws2812-leds-using-spi/

r = audio.Recorder()
r.volume(12)
print("sample_rate:{} format:{} channel:{}".format(r.sample_rate(), r.format(), r.channel()))

# while not app.need_exit():
#     data = r.record()
#     print("data size", len(data))

#     time.sleep_ms(10)

p = audio.Player()

# with open('/root/output.pcm', 'rb') as f:
#     ctx = f.read()

# p.play(bytes(ctx))

# while not app.need_exit():
#     time.sleep_ms(10)

# print("play finish!")


cam = camera.Camera(480, 320)   # 640, 480)
print("=============================== -- camera init ok")

disp = display.Display(640, 480)
print("=============================== -- display init ok")

t = time.time() 
img = cam.read()
for i in range(3):
    # t = time.time()  # time_ms()
    img = cam.read()
    disp.show(img, fit = image.Fit.FIT_CONTAIN)
    print(f"{i}, time: {time.time() - t}s, fps: {1 / (time.time() - t)}")
    t = time.time() 

img = cam.read()
disp.show(img, fit = image.Fit.FIT_CONTAIN)

print("===============================", type(img), len(img.to_bytes()))

def gpt4v(prompt=test_prompt, detail="auto"):
    import base64

    # Function to encode the image
    def encode_image():    # image_path):
        return base64.b64encode(img.to_jpeg().to_bytes()).decode('utf-8')

            # with open(image_path, "rb") as image_file:
            #     return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    # image_path = \
    # "/root/langtable_blocks.png"
    # "./langtable_real.jpeg"
    # output_image100.jpg"

    # INTER_AREA interpolation method preferred for image shrinking
    # cv2.INTER_LINEAR or cv2.INTER_CUBIC for a smoother effect.
    # resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Getting the base64 string
    base64_image = encode_image()    # image_path)
    print(len(base64_image))
    
    # base64_image_sim = encode_image(image_path)
    # base64_image_real = encode_image(image_path)

    payload = {
        "model": "gpt-4o-2024-05-13",
        # gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                {
                "type": "text",
                # "text": "Assuming you are a robot and controlling a robotics arm to move the yellow pentagon to the green star."
                # "text": prompt
                "text": "short reply",
                # Describe the position of each block, one after one in structure.",#What’s in this image? in Chinese.",
                # What’s in this image? can you tell me a reference size of the red car in the image in centimeter?"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail,   # "low", "high", "auto"
                }
                },
                # {
                # "type": "image_url",
                # "image_url": {
                #     "url": f"data:image/jpeg;base64,{base64_image_sim}"
                # }
                # },
                # {
                # "type": "image_url",
                # "image_url": {
                #     "url": f"data:image/jpeg;base64,{base64_image_real}"
                # }
                # },
            ]
            }
        ],
        "max_tokens": 300
    }

    print(f'\033[0;41;42m{time.time() - now}\033[0m', "\tSending the prompt to get the GPT4V completion.")
    response = requests.post("https://api.open-assistant.cn/v1/chat/completions", headers=headers, json=payload)

    content = response.json()
    print(response.json())

    content = content['choices'][0]['message']['content']
    print(f"\033[0;41;41m========[detail={detail}]========\033[0m")
    print(content)

    # openai_voice(content)

gpt4v()
print(f"time: {time.time() - t}s.")
# time.sleep(1)

while 1:
    t = time.time()  # time_ms()
    img = cam.read()
    disp.show(img)
    # print(f"time: {time.time() - t}s, fps: {1 / (time.time() - t)}")
