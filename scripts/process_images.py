# -*- coding: utf-8 -*-
"""
桥梁图片批量处理脚本
- 重命名为标准格式
- 调整尺寸为多种规格
- 压缩优化
"""

import os
from PIL import Image

# 源目录
SOURCE_DIR = r"D:\AI创意大赛\【桥见千年】中国古代桥梁智慧可视化平台\frontend\public\images\bridges"

# 文件名映射（中文 -> 英文ID）
NAME_MAP = {
    "十七孔桥": "shiqikong-bridge",
    "卢沟桥": "lugou-bridge",
    "广济桥": "guangji-bridge",
    "泸定桥": "luding-bridge",
    "洛阳桥": "luoyang-bridge",
    "西湖断桥": "duan-bridge",
    "赵州桥": "zhaozhou-bridge",
    "风雨桥 侗族": "fengyu-bridge",
    "风雨桥": "fengyu-bridge",
}

# 目标尺寸
SIZES = {
    "main": (800, 450),      # 主图
    "detail": (1200, 600),  # 详情大图
    "thumb": (300, 200),    # 缩略图
}

def process_image(input_path, output_path, size):
    """处理单张图片"""
    with Image.open(input_path) as img:
        # 转换为 RGB（如果带有 alpha 通道）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # 获取原始尺寸
        orig_width, orig_height = img.size
        target_width, target_height = size
        
        # 计算缩放比例（保持宽高比，裁剪填充）
        ratio = max(target_width / orig_width, target_height / orig_height)
        new_width = int(orig_width * ratio)
        new_height = int(orig_height * ratio)
        
        # 缩放
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # 居中裁剪
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        img_cropped = img_resized.crop((left, top, right, bottom))
        
        # 保存
        img_cropped.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  OK: {os.path.basename(output_path)} ({target_width}x{target_height})")

def main():
    print("=" * 50)
    print("桥梁图片批量处理")
    print("=" * 50)
    
    # 遍历源目录
    files = os.listdir(SOURCE_DIR)
    processed = 0
    
    for filename in files:
        # 跳过已处理的文件
        if filename.endswith(('-main.jpg', '-detail.jpg', '-thumb.jpg')):
            continue
        
        # 查找匹配的中文名
        bridge_id = None
        for cn_name, en_id in NAME_MAP.items():
            if cn_name in filename:
                bridge_id = en_id
                break
        
        if not bridge_id:
            print(f"⚠ 跳过未知文件: {filename}")
            continue
        
        # 源文件路径
        input_path = os.path.join(SOURCE_DIR, filename)
        
        print(f"\n处理: {filename} → {bridge_id}")
        
        # 生成各种尺寸
        for size_name, size in SIZES.items():
            output_filename = f"{bridge_id}-{size_name}.jpg"
            output_path = os.path.join(SOURCE_DIR, output_filename)
            
            try:
                process_image(input_path, output_path, size)
            except Exception as e:
                print(f"  ERROR: {e}")
        
        processed += 1
    
    print(f"\n" + "=" * 50)
    print(f"完成！共处理 {processed} 座桥梁")
    print("=" * 50)

if __name__ == "__main__":
    main()
