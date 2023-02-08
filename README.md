# GachaAnalyse
这是一个原神抽卡分析工具，通过抽卡历史界面的录制视频识别并统计抽卡记录。

# 特点
由于同一页码图像相近，故灰度化、阈值化、异或并求和所得值较小，不同页码则较大，因此对这些值统计并降序排序后可获得页面发生跳转的帧的序号，而无需对页码进行文字识别。

## 用词说明：
“角色部分”：指祈愿历史记录中“名称”一列（不包括“名称”单元格）；
  
“页码部分”：指祈愿历史记录中正下方的数字。

## 录制的视频要求：
1.视频格式应为.mp4；
  
2.从第一帧到最后一帧不应出现祈愿历史记录界面以外的画面；
  
3.祈愿历史记录翻页时不应反向翻页，如从第9页翻到第8页。


## 手动框选角色部分与页码部分方法：
类似于截屏操作，将鼠标移至要框选区域的左上角，按住鼠标左键不动，将鼠标移至要框选区域的右下角，松开鼠标左键。
