import json
import os
from typing import Any, Dict, List
from datetime import datetime

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    加载JSON文件
    :param file_path: JSON文件路径
    :return: JSON数据字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load JSON file {file_path}: {str(e)}")

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """
    保存数据到JSON文件
    :param data: 要保存的数据
    :param file_path: 保存路径
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise Exception(f"Failed to save JSON file {file_path}: {str(e)}")

def get_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def create_dir_if_not_exists(dir_path: str) -> None:
    """
    如果目录不存在则创建
    :param dir_path: 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_project_root() -> str:
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_test_data_path(env: str = 'test') -> str:
    """
    获取测试数据目录路径
    :param env: 环境名称
    :return: 数据目录路径
    """
    return os.path.join(get_project_root(), 'data', env)

def clean_dir(dir_path: str) -> None:
    """
    清空目录内容
    :param dir_path: 目录路径
    """
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}: {str(e)}') 