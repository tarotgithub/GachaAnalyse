import easyocr
import cv2 as cv
import numpy as np
from openpyxl import Workbook


# 文字识别器
reader = easyocr.Reader(['ch_sim'], gpu=False)

# 打开视频
video_path = input('请输入视频路径（请勿含有中文）：')
xlsx_path = video_path[0:-3] + 'xlsx'
cap = cv.VideoCapture(video_path)

if not cap.isOpened():
    print('打开视频失败！')
    exit()

# 获取视频图像的宽度和高度
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# 计算角色部分在图像上的位置
character_x1 = frame_width * 917 // 3200
character_y1 = frame_height * 632 // 1440
character_x2 = frame_width * 1423 // 3200
character_y2 = frame_height * 1131 // 1440


def get_character(image):
    return image[character_y1:character_y2, character_x1:character_x2]


# 计算页码部分在图像上的位置
page_x1 = frame_width * 1450 // 3200
page_y1 = frame_height * 1168 // 1440
page_x2 = frame_width * 1670 // 3200
page_y2 = frame_height * 1238 // 1440


def get_page(image):
    return image[page_y1:page_y2, page_x1:page_x2]


# 图像显示时的大小与图像实际大小的比值（缩放比例）
ratio = 1000 / frame_width

# 用户确认角色部分与页码部分是否计算正确
ret, frame = cap.read()
cv.rectangle(frame, (character_x1, character_y1), (character_x2, character_y2), (0, 0, 255), thickness=10)
cv.rectangle(frame, (page_x1, page_y1), (page_x2, page_y2), (0, 255, 0), thickness=10)
frame = cv.resize(frame, None, fx=ratio, fy=ratio)
cv.imshow('image', frame)
cv.waitKey(1)

t = input('请确认红色方框与绿色方框是否分别框选角色部分与页码部分（是：Y，否：N）：')
if t == 'y' or t == 'Y':
    pass
elif t == 'n' or t == 'N':
    print('请手动框选角色部分并按Enter键')
    character_box = cv.selectROI('image', frame, showCrosshair=False)
    print('请手动框选页码部分并按Enter键')
    page_box = cv.selectROI('image', frame, showCrosshair=False)
    cv.destroyAllWindows()

    character_x1, character_y1 = character_box[0], character_box[1]
    character_x2, character_y2 = character_box[0]+character_box[2], character_box[1]+character_box[3]
    [character_x1, character_x2, character_y1, character_y2] = \
        list(map(lambda x: int(x / ratio), [character_x1, character_x2, character_y1, character_y2]))

    page_x1, page_y1 = page_box[0], page_box[1]
    page_x2, page_y2 = page_box[0]+page_box[2], page_box[1]+page_box[3]
    [page_x1, page_x2, page_y1, page_y2] = \
        list(map(lambda x: int(x / ratio), [page_x1, page_x2, page_y1, page_y2]))
else:
    exit()


# 获取起始页码和终止页码
start_page = int(input('请输入起始页码：'))
end_page = int(input('请输入终止页码：'))

# 获取不同帧的图像差异值列表
# 图像差异值为两个图像在灰度化、阈值化处理后，进行异或操作并将结果求和所得值
# 图像差异值越小，则两个图像的差异越小
differences = []


# 图像灰度化、阈值化
def image_process(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, image = cv.threshold(image, 200, 255, cv.THRESH_BINARY)
    return image


# 获取图像差异值
def get_difference(image1, image2):
    image1 = image_process(image1)
    image2 = image_process(image2)

    return np.sum(cv.bitwise_xor(image1, image2))


print('正在分析相邻帧页码部分图像差异值...')

frame_num = 2  # 记录帧的位置，对应 frame2
_, frame1 = cap.read()

while True:
    ret, frame2 = cap.read()
    if not ret:
        break

    differences.append({'frame_num': frame_num, 'difference': get_difference(get_page(frame1), get_page(frame2))})
    frame1 = np.copy(frame2)
    frame_num += 1

# 根据差异值进行降序排序
differences = sorted(differences, key=lambda x: x['difference'], reverse=True)

# 获取前 end_page-start_page 个数据，第一帧对应起始页码，应额外添加
differences = differences[0:end_page-start_page]
frame_nums = [x['frame_num'] for x in differences]
frame_nums.append(1)
frame_nums = sorted(frame_nums)

# 创建excel的workbook
wb = Workbook()
# 获取被激活的worksheet
ws = wb.active
# 在第一行添加提示
ws.append(['页码', '角色'])


# 依次识别各个数据中对应的角色图像
print('正在识别角色部分...')
page_num = start_page
for frame_num in frame_nums:
    # 跳转至指定帧并读取
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()

    # 识别角色图像并将识别结果保存到worksheet中
    results = reader.readtext(image_process(get_character(frame)))
    # 识别角色图像
    for result in results:
        ws.append([page_num, result[1]])

    page_num += 1

# 保存并退出
# 保存workbook
wb.save(xlsx_path)
