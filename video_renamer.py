#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频自动重命名程序
功能：提取视频预览帧，AI分析内容，自动重命名视频文件
"""

import os
import cv2
import requests
import json
from pathlib import Path
import time
from typing import List, Dict, Optional
import argparse

class VideoRenamer:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        """
        初始化视频重命名器
        
        Args:
            api_key: AI API密钥（可选）
            api_endpoint: AI API端点（可选）
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        
    def extract_preview_frame(self, video_path: str, output_dir: str = "preview_frames") -> Optional[str]:
        """
        从视频中提取预览帧
        
        Args:
            video_path: 视频文件路径
            output_dir: 预览帧输出目录
            
        Returns:
            预览帧图片路径，失败返回None
        """
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 打开视频文件
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"无法打开视频文件: {video_path}")
                return None
            
            # 获取视频总帧数
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames == 0:
                print(f"视频文件无效: {video_path}")
                return None
            
            # 提取中间帧作为预览
            middle_frame = total_frames // 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            ret, frame = cap.read()
            
            if not ret:
                print(f"无法读取视频帧: {video_path}")
                return None
            
            # 生成输出文件名
            video_name = Path(video_path).stem
            frame_path = os.path.join(output_dir, f"{video_name}_preview.jpg")
            
            # 保存预览帧
            cv2.imwrite(frame_path, frame)
            cap.release()
            
            print(f"成功提取预览帧: {frame_path}")
            return frame_path
            
        except Exception as e:
            print(f"提取预览帧时出错: {e}")
            return None
    
    def analyze_frame_with_ai(self, frame_path: str) -> Optional[str]:
        """
        使用AI分析预览帧内容
        
        Args:
            frame_path: 预览帧图片路径
            
        Returns:
            AI生成的视频名称，失败返回None
        """
        try:
            if not self.api_key or not self.api_endpoint:
                # 如果没有配置AI API，使用模拟分析
                return self._mock_ai_analysis(frame_path)
            
            # 读取图片文件并转换为base64
            import base64
            with open(frame_path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # 准备请求数据
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # 使用正确的GPT-4 Vision模型
            payload = {
                "model": "doubao-1-5-thinking-vision-pro-250428",  # 或者使用 "gpt-4o-mini" 作为替代
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "任务：分析图片，生成视频名称。规则：1.只输出名称 2.中文 3.10字以内 4.描述图片主要内容 5.禁止输出'抱歉'、'无法识别'等文字 6.即使不确定也要给出推测名称"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100
            }
            
            # 发送请求
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            video_name = result['choices'][0]['message']['content'].strip()
            
            # 清理名称（移除引号等特殊字符）
            video_name = video_name.replace('"', '').replace("'", "").replace('《', '').replace('》', '')
            
            print(f"AI分析结果: {video_name}")
            return video_name
            
        except Exception as e:
            print(f"AI分析时出错: {e}")
            return self._mock_ai_analysis(frame_path)
    
    def _mock_ai_analysis(self, frame_path: str) -> str:
        """
        模拟AI分析（当没有配置真实API时使用）
        
        Args:
            frame_path: 预览帧图片路径
            
        Returns:
            模拟生成的视频名称
        """
        # 基于文件名生成模拟名称
        base_name = Path(frame_path).stem.replace('_preview', '')
        
        # 模拟一些常见的视频内容描述
        mock_names = [
            f"{base_name}精彩片段",
            f"{base_name}精彩瞬间",
            f"{base_name}精彩画面",
            f"{base_name}精彩内容",
            f"{base_name}精彩视频"
        ]
        
        import random
        mock_name = random.choice(mock_names)
        print(f"使用模拟分析结果: {mock_name}")
        return mock_name
    
    def rename_video(self, old_path: str, new_name: str) -> bool:
        """
        重命名视频文件
        
        Args:
            old_path: 原视频文件路径
            new_name: 新名称
            
        Returns:
            重命名是否成功
        """
        try:
            # 获取原文件扩展名
            old_path_obj = Path(old_path)
            extension = old_path_obj.suffix
            
            # 生成新文件路径
            new_path = old_path_obj.parent / f"{new_name}{extension}"
            
            # 检查新文件名是否已存在
            counter = 1
            while new_path.exists():
                new_path = old_path_obj.parent / f"{new_name}_{counter}{extension}"
                counter += 1
            
            # 重命名文件
            old_path_obj.rename(new_path)
            print(f"成功重命名: {old_path_obj.name} -> {new_path.name}")
            return True
            
        except Exception as e:
            print(f"重命名文件时出错: {e}")
            return False
    
    def process_directory(self, directory_path: str, output_dir: str = "preview_frames") -> Dict[str, str]:
        """
        处理目录中的所有视频文件
        
        Args:
            directory_path: 视频文件目录路径
            output_dir: 预览帧输出目录
            
        Returns:
            处理结果字典 {原文件名: 新文件名}
        """
        results = {}
        
        # 获取目录中的所有视频文件
        video_files = []
        for file_path in Path(directory_path).iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                video_files.append(str(file_path))
        
        if not video_files:
            print(f"在目录 {directory_path} 中未找到支持的视频文件")
            return results
        
        print(f"找到 {len(video_files)} 个视频文件")
        
        # 处理每个视频文件
        for video_path in video_files:
            print(f"\n处理视频: {Path(video_path).name}")
            
            # 1. 提取预览帧
            frame_path = self.extract_preview_frame(video_path, output_dir)
            if not frame_path:
                continue
            
            # 2. AI分析预览帧
            new_name = self.analyze_frame_with_ai(frame_path)
            if not new_name:
                continue
            
            # 3. 重命名视频文件
            if self.rename_video(video_path, new_name):
                results[Path(video_path).name] = f"{new_name}{Path(video_path).suffix}"
            
            # 添加延迟避免API限制
            time.sleep(1)
        
        return results
    
    def cleanup_preview_frames(self, output_dir: str = "preview_frames"):
        """
        清理预览帧文件
        
        Args:
            output_dir: 预览帧目录
        """
        try:
            if os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir)
                print(f"已清理预览帧目录: {output_dir}")
        except Exception as e:
            print(f"清理预览帧时出错: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='视频自动重命名程序')
    parser.add_argument('directory', help='包含视频文件的目录路径')
    parser.add_argument('--api-key', help='AI API密钥')
    parser.add_argument('--api-endpoint', help='AI API端点')
    parser.add_argument('--keep-frames', action='store_true', help='保留预览帧文件')
    parser.add_argument('--output-dir', default='preview_frames', help='预览帧输出目录')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.exists(args.directory):
        print(f"错误: 目录 {args.directory} 不存在")
        return
    
    # 创建视频重命名器
    renamer = VideoRenamer(
        api_key=args.api_key,
        api_endpoint=args.api_endpoint
    )
    
    print("开始处理视频文件...")
    print(f"视频目录: {args.directory}")
    print(f"预览帧目录: {args.output_dir}")
    
    # 处理视频文件
    results = renamer.process_directory(args.directory, args.output_dir)
    
    # 显示处理结果
    if results:
        print(f"\n处理完成！共重命名 {len(results)} 个文件:")
        for old_name, new_name in results.items():
            print(f"  {old_name} -> {new_name}")
    else:
        print("\n没有成功处理任何视频文件")
    
    # 清理预览帧文件
    if not args.keep_frames:
        renamer.cleanup_preview_frames(args.output_dir)
    
    print("\n程序执行完成！")

if __name__ == "__main__":
    main()
