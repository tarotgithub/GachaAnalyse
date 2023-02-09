# GachaAnalyse
这是一个原神抽卡分析工具，通过抽卡历史界面的录制视频识别并统计抽卡记录。

# 特点
由于同一页码图像相近，故灰度化、阈值化、异或并求和所得值较小，不同页码则较大，因此对这些值统计并降序排序后可获得页面发生跳转的帧的序号，而无需对页码进行文字识别，提高了效率。

# 使用说明
## 安装依赖包说明：
1.更新pip：
```python -m pip install --upgrade pip```

2.若安装过程中显示依赖包版本冲突，请使用
```pip install -r requirements.txt --no-dependencies```

## easyocr说明
首次运行该程序时会提示如下内容并开始下载easyocr的模型：
  
```Downloading detection model, please wait. This may take several minutes depending upon your network connection.```
  
请确保网络状况良好。该下载过程可能会失败，请尝试重启程序以重新下载（可能会失败多次）或手动下载。  
手动下载地址如：```https://www.jaided.ai/easyocr/modelhub/```（需下载此链接中的zh_sim_g2与CRAFT，参考：```https://zhuanlan.zhihu.com/p/566665446```）  
若手动下载模型，则下载完成后将文件craft_mlt_25k.pth与文件zh_sim_g2.pth放到目录C:\Users\123\.EasyOCR\model下（123为用户名）。


## 用词说明：
“角色部分”：指祈愿历史记录中“名称”一列（不包括“名称”单元格）；
  
“页码部分”：指祈愿历史记录中正下方的数字。

## 视频要求：
1.视频格式应为.mp4；
  
2.从第一帧到最后一帧不应出现祈愿历史记录界面以外的画面；
  
3.祈愿历史记录翻页时不应反向翻页，如从第9页翻到第8页。
  
4.由于easyocr不支持中文路径，故视频路径中不应包含中文。

## 手动框选角色部分与页码部分方法：
类似于截屏操作，将鼠标移至要框选区域的左上角，按住鼠标左键不动，将鼠标移至要框选区域的右下角，松开鼠标左键。

## 生成的文件
该工具会在视频所在目录下生成一个与视频同名的.xlsx文件

## 启用gpu加速
该工具使用easyocr时默认不启用gpu，若要启用，请于main.py文件中将  
```reader = easyocr.Reader(['ch_sim'], gpu=False)```   
更改为  
```reader = easyocr.Reader(['ch_sim'], gpu=True)``` 
  
同时，请确保pytorch版本与cuda版本相符。

