"""RPA外部API客户端封装"""

import os
import json
import requests

BASE_URL = "http://127.0.0.1:48081"
HEADER_API_KEY = "X-API-Key"
ENV_API_KEY = "RPA_API_KEY"


def get_api_key() -> str:
    """从环境变量获取API Key"""
    api_key = os.environ.get(ENV_API_KEY, "")
    if not api_key:
        raise ValueError(
            f"环境变量 {ENV_API_KEY} 未配置。"
            f"请在 ~/.openclaw/openclaw.json 的 skills.entries.yuangongjuzhen.env 中配置，"
            f"或在 ~/.openclaw/.env 中设置 {ENV_API_KEY}=sk_xxxx"
        )
    return api_key


def _headers() -> dict:
    return {HEADER_API_KEY: get_api_key(), "Content-Type": "application/json"}


def post(path: str, data: dict = None) -> dict:
    """发送POST请求"""
    url = f"{BASE_URL}{path}"
    resp = requests.post(url, json=data or {}, headers=_headers(), timeout=30)
    return resp.json()


def get(path: str) -> dict:
    """发送GET请求"""
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, headers=_headers(), timeout=30)
    return resp.json()


def put(path: str, data: dict = None) -> dict:
    """发送PUT请求"""
    url = f"{BASE_URL}{path}"
    resp = requests.put(url, json=data or {}, headers=_headers(), timeout=30)
    return resp.json()


def delete(path: str) -> dict:
    """发送DELETE请求"""
    url = f"{BASE_URL}{path}"
    resp = requests.delete(url, headers=_headers(), timeout=30)
    return resp.json()
