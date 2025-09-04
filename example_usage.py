#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例脚本
"""

from video_renamer import VideoRenamer
import os

def example_without_api():
    """不使用AI API的示例"""
    print("=== 不使用AI API的示例 ===")
    
    # 创建重命名器（不配置API）
    renamer = VideoRenamer()
    
    # 处理sample目录中的视频
    sample_dir = "sample"
    if os.path.exists(sample_dir):
        results = renamer.process_directory(sample_dir)
        print(f"处理结果: {results}")
    else:
        print(f"目录 {sample_dir} 不存在")

def example_with_api():
    """使用AI API的示例"""
    print("\n=== 使用AI API的示例 ===")
    
    # 配置AI API（需要替换为真实的API密钥）
    api_key = "your_api_key_here"
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    
    # 创建重命名器
    renamer = VideoRenamer(api_key=api_key, api_endpoint=api_endpoint)
    
    # 处理sample目录中的视频
    sample_dir = "sample"
    if os.path.exists(sample_dir):
        results = renamer.process_directory(sample_dir)
        print(f"处理结果: {results}")
    else:
        print(f"目录 {sample_dir} 不存在")

if __name__ == "__main__":
    # 运行示例
    example_without_api()
    example_with_api()
