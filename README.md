# rabona
一个 EA FIFA18 线下赛事辅助工具。

# Raw Image Process

## 流程
- from ri import RabonaImage as ri
- 构建 ri 对象: ri(raw_img, threshold)
- 首先判断图像大小是否满足最低要求（w1440 x h1920)
- cv2.imread() 转换为矩阵
- 矩阵高度被统一成 1920
- ri.dynamicThreshold() 返回二值化后的图像 bin_img
    - 采用对象构建时的 threshold 进行 first guess
- 构建屏幕对象 Screen(bin_img, bleed)
    - bin_img
    - bleed
    - Screen.getScreen()识别屏幕尺寸
        - 输出到考虑中可读性的字典 Screen.size
        - 输出 PIL 的 resize 参数 `region` 接受的数组形式 Screen.rect
- ri.crop() 根据 Screen.rect 裁剪 Screen
    - [improvement] 此处 region 应按比例计算，以从原图上裁剪
        - 目前的临时做法是先将原图缩小再裁剪，看上去相当愚蠢