"""公众号任务管理"""

from . import client


def create_mp_task(
    subject: str,
    target_bite_seq: str,
    subject_type: str = None,
    ai_model_code: str = None,
    image_from: str = None,
    material_group_id: int = None,
    content_prefix: str = None,
    content_suffix: str = None,
    mp_publish: str = None,
    priority: int = None,
    auto_publish: str = None,
) -> dict:
    """创建公众号任务"""
    data = {
        "subject": subject,
        "targetBiteSeq": target_bite_seq,
    }
    if subject_type is not None:
        data["subjectType"] = subject_type
    if ai_model_code is not None:
        data["aiModelCode"] = ai_model_code
    if image_from is not None:
        data["imageFrom"] = image_from
    if material_group_id is not None:
        data["materialGroupId"] = material_group_id
    if content_prefix is not None:
        data["contentPrefix"] = content_prefix
    if content_suffix is not None:
        data["contentSuffix"] = content_suffix
    if mp_publish is not None:
        data["mpPublish"] = mp_publish
    if priority is not None:
        data["priority"] = priority
    if auto_publish is not None:
        data["autoPublish"] = auto_publish
    return client.post("/rpa/external/mptask/add", data)


def list_mp_tasks(
    page: int = 1,
    page_size: int = 10,
    publish_status: int = None,
) -> dict:
    """查询公众号任务列表"""
    data = {"pageNum": page, "pageSize": page_size}
    if publish_status is not None:
        data["mpPublishStatus"] = publish_status
    return client.post("/rpa/external/mptask/list", data)


def get_mp_task(task_id: int) -> dict:
    """获取公众号任务详情"""
    return client.post(f"/rpa/external/mptask/detail?taskId={task_id}")


def update_mp_task(
    task_id: int,
    publish_status: int,
    publish_reason: str = None,
) -> dict:
    """更新公众号任务状态"""
    data = {"id": task_id, "mpPublishStatus": publish_status}
    if publish_reason is not None:
        data["mpPublishReason"] = publish_reason
    return client.post("/rpa/external/mptask/update", data)


def delete_mp_task(task_id: int) -> dict:
    """删除公众号任务"""
    return client.delete(f"/rpa/external/mptask/{task_id}")
