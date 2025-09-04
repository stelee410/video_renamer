# 视频自动重命名程序

这是一个Python程序，可以自动提取视频预览帧，使用AI分析内容，并自动重命名视频文件。

## 功能特性

- �� 支持多种视频格式（MP4, AVI, MOV, MKV, WMV, FLV）
- ��️ 自动提取视频预览帧
- �� AI智能分析视频内容
- ✏️ 自动生成描述性文件名
- �� 批量处理整个目录
- 🧹 自动清理临时文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用（不使用AI API）

```bash
python video_renamer.py sample/
```

### 2. 使用AI API

```bash
python video_renamer.py sample/ --api-key "your_api_key" --api-endpoint "https://api.openai.com/v1/completions"
```

### 3. 保留预览帧文件

```bash
python video_renamer.py sample/ --keep-frames
```

### 4. 自定义预览帧输出目录

```bash
python video_renamer.py sample/ --output-dir "my_frames"
```

## 配置AI API

编辑 `config.py` 文件，填入你的AI API配置信息：

```python
AI_CONFIG = {
    "openai": {
        "api_key": "your_openai_api_key_here",
        "endpoint": "https://api.openai.com/v1/chat/completions"
    }
}
```

## 支持的AI服务

- OpenAI GPT-4 Vision
- 百度AI
- 腾讯AI
- 其他支持图像分析的AI服务

## 注意事项

1. 确保有足够的磁盘空间存储预览帧
2. 使用AI API时注意API调用限制和费用
3. 建议先在小批量文件上测试
4. 程序会自动备份原文件（如果启用）

## 示例输出
