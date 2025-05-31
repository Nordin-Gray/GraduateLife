import cv2
import numpy as np
import random
import os
import glob

def rotate_image_with_background(image, angle, bg_color=(143, 148, 151)):
    """
    对图像进行旋转，并使用指定颜色填充空白背景。

    参数：
    - image: 输入图像（numpy数组）
    - angle: 顺时针旋转角度（整数）
    - bg_color: 背景填充颜色（默认是灰色）

    返回：
    - 旋转后的图像
    """
    (h, w) = image.shape[:2]        # 图像高度和宽度
    (cX, cY) = (w // 2, h // 2)     # 图像中心点坐标

    # 获取旋转矩阵：顺时针旋转 angle 度，缩放比例为 1
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    # 提取旋转矩阵中的 cos 和 sin 值
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 计算旋转后图像的新尺寸，确保不裁剪
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    """
    这一步是在？
    """
    # 调整旋转矩阵的平移部分，将旋转中心移到新图像中心
    M[0, 2] += (new_w / 2) - cX
    M[1, 2] += (new_h / 2) - cY

    # 执行仿射变换，设置背景颜色
    rotated = cv2.warpAffine(image, M, (new_w, new_h), borderValue=bg_color)
    return rotated

# 处理主函数
def process_images(
    input_dir,              # 输入文件夹路径（原始图像）
    output_dir,             # 输出文件夹路径（旋转图像）
    log_path,               # 保存角度的txt文件路径
    angle_range=(-10, 10),  # 角度范围（默认 -10 到 +10 度）
    image_ext="jpg"         # 图像扩展名（默认 jpg）
):
    """
    批量处理文件夹中的图像，执行旋转并记录角度。

    参数说明见上方。
    """

    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有匹配的图像路径（如 *.jpg）
    image_paths = glob.glob(os.path.join(input_dir, f"*.{image_ext}"))

    # 打开角度日志文件，追加写入模式
    with open(log_path, "a") as log_file:
        for path in image_paths:
            file_name = os.path.splitext(os.path.basename(path))[0]  # 提取不带扩展名的文件名
            angle = random.randint(*angle_range)                     # 随机生成角度

            img = cv2.imread(path)                                   # 读取图像
            if img is None:
                print(f"无法读取图像: {path}")                        # 错误提示
                continue

            rotated_img = rotate_image_with_background(img, angle)   # 旋转图像

            save_path = os.path.join(output_dir, f"{file_name}.{image_ext}")  # 构造保存路径
            cv2.imwrite(save_path, rotated_img)                      # 保存旋转图像

            log_file.write(f"{file_name}\t{angle}\n")                # 写入文件名和旋转角度

    print(f"已完成处理，共处理图像 {len(image_paths)} 张。")           # 完成提示


if __name__ == "__main__":
    # 配置参数
    folder_name = "Open_circuit"     # 原始文件夹名
    base_path = "D:/Desktop/PCB_DATASET/images"  # 根目录

    input_folder = os.path.join(base_path, folder_name)                # 输入路径
    output_folder = os.path.join(base_path, folder_name + "_rotation") # 输出路径
    log_file_path = folder_name + "_angles.txt"                        # 日志文件名

    # 调用图像处理函数
    process_images(
        input_dir=input_folder,
        output_dir=output_folder,
        log_path=log_file_path,
        angle_range=(-10, 10),     # 角度范围
        image_ext="jpg"            # 文件类型
    )
