# rabona
一个 EA FIFA18 线下赛事辅助工具。

# Raw Image Process

## 流程
- from ri import RabonaImage as RI
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
        - 输出到可读性较强的字典 Screen.size
        - 输出 PIL 的 resize 参数 `region` 接受的数组形式 Screen.real_rect
- ri.crop() 根据 Screen.real_rect 裁剪 Screen
- from parser import RabonaParser as RP
- RabonaParser 初始化需要两个东西
    - 二值化后的屏幕图像
    - 用于解析的模板参数
- 在初始化时切片
    - 首先切出 ABCDEFG 区
    - 其后切出各区的小块，如 A 区的 score_area
- 然后用具体的 method 取得文字识别值

    