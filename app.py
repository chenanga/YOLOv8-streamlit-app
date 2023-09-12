#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     app.py
   @Author:        ang
   @Date:          2023/9/12
   @Description:
-------------------------------------------------
"""
from pathlib import Path
from PIL import Image
import streamlit as st

import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

# setting page layout
st.set_page_config(
    page_title="YOLOv8 目标检测系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.title("YOLOv8 目标检测系统")

# sidebar
st.sidebar.header("模型配置选择")

# model options
task_type = st.sidebar.selectbox(
    "任务类别选择",
    ["检测", "分割", "关键点"],
)

model_type = None
if task_type == "检测":
    model_type = st.sidebar.selectbox(
        "选择模型",
        config.DETECTION_MODEL_LIST
    )
elif task_type == "分割":
    model_type = st.sidebar.selectbox(
        "选择模型",
        config.SEGMENT_MODEL_LIST
    )
elif task_type == "关键点":
    model_type = st.sidebar.selectbox(
        "选择模型",
        config.POSE_MODEL_LIST
    )
else:
    st.error("Currently only 'Detection' function is implemented")

confidence = float(st.sidebar.slider(
    "置信度", 30, 100, 50)) / 100

model_path = ""
if model_type:

    if task_type == "检测":
        model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
    elif task_type == "分割":
        model_path = Path(config.SEGMENT_MODEL_DIR, str(model_type))
    elif task_type == "关键点":
        model_path = Path(config.POSE_MODEL_DIR, str(model_type))
else:
    st.error("Please Select Model in Sidebar")

# load pretrained DL model
try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Unable to load model. Please check the specified path: {model_path}")

# image/video options
st.sidebar.header("Image/Video Config")
source_selectbox = st.sidebar.selectbox(
    "选择来源",
    config.SOURCES_LIST
)

source_img = None
if source_selectbox == config.SOURCES_LIST[0]: # Image
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]: # Video
    infer_uploaded_video(confidence, model)
elif source_selectbox == config.SOURCES_LIST[2]: # Webcam
    infer_uploaded_webcam(confidence, model)
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")