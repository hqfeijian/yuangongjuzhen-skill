"""小红书AI创作任务管理"""

from . import client


def create_xhs_aitask(
    input_content: str,
    target_bite_seq: str,
    content_prompt_id: int = None,
    image_prompt_id: int = None,
    need_publish: str = None,
    image_count: int = None,
    aspect_ratio: str = None,
    priority: int = None,
    auto_publish: str = None,
) -> dict:
    """创建小红书AI创作任务"""
    data = {
        "inputContent": input_content,
        "targetBiteSeq": target_bite_seq,
    }
    if content_prompt_id is not None:
        data["contentPromptId"] = content_prompt_id
    if image_prompt_id is not None:
        data["imagePromptId"] = image_prompt_id
    if need_publish is not None:
        data["needPublish"] = need_publish
    if image_count is not None:
        data["imageCount"] = image_count
    if aspect_ratio is not None:
        data["aspectRatio"] = aspect_ratio
    if priority is not None:
        data["priority"] = priority
    if auto_publish is not None:
        data["autoPublish"] = auto_publish
    return client.post("/rpa/external/xhs-aiclone/add", data)


def list_xhs_aitasks(
    page: int = 1,
    page_size: int = 10,
    publish_status: int = None,
) -> dict:
    """查询小红书AI任务列表"""
    data = {"pageNum": page, "pageSize": page_size}
    if publish_status is not None:
        data["publishStatus"] = publish_status
    return client.post("/rpa/external/xhs-aiclone/list", data)


def get_xhs_aitask(task_id: int) -> dict:
    """获取小红书AI任务详情"""
    return client.post("/rpa/external/xhs-aiclone/detail", {"seq": str(task_id)})


def update_xhs_aitask(
    task_id: int,
    publish_status: int,
    publish_reason: str = None,
) -> dict:
    """更新小红书AI任务状态"""
    data = {"id": task_id, "publishStatus": publish_status}
    if publish_reason is not None:
        data["publishReason"] = publish_reason
    return client.post("/rpa/external/xhs-aiclone/update", data)


def delete_xhs_aitask(task_id: int) -> dict:
    """删除小红书AI任务"""
    return client.delete(f"/rpa/external/xhs-aiclone/{task_id}")
