# -*- coding: utf-8 -*-
"""
配置文件
"""

# AI API配置
AI_CONFIG = {
    # OpenAI GPT-4 Vision API配置
    "openai": {
        "api_key": "your_openai_api_key_here",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4-vision-preview"
    },
    
    # 百度AI配置
    "baidu": {
        "api_key": "your_baidu_api_key_here",
        "secret_key": "your_baidu_secret_key_here",
        "endpoint": "https://aip.baidubce.com/rest/2.0/image-classify/v1/advanced_general"
    },
    
    # 腾讯AI配置
    "tencent": {
        "api_key": "your_tencent_api_key_here",
        "endpoint": "https://api.ai.qq.com/fcgi-bin/vision/vision_objectr"
    }
}

# 视频处理配置
VIDEO_CONFIG = {
    "supported_formats": ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
    "preview_frame_quality": 95,  # JPEG质量
    "max_preview_size": (800, 600),  # 预览帧最大尺寸
    "frame_extraction_method": "middle",  # 提取方法: middle, first, random
}

# 输出配置
OUTPUT_CONFIG = {
    "preview_frames_dir": "preview_frames",
    "log_file": "video_renamer.log",
    "backup_original": True,  # 是否备份原文件
    "max_name_length": 20,  # 最大文件名长度
}
