"""员工矩阵任务管理 Skill 入口"""

import argparse
import json
import os
import sys

from . import client
from . import mp_task
from . import xhs_aitask

PRESETS_FILE = os.path.join(os.path.dirname(__file__), "presets.json")
SUBJECT_TYPE_MAP_FILE = os.path.join(os.path.dirname(__file__), "subject_type_map.json")


def load_presets() -> dict:
    with open(PRESETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_subject_type_map() -> dict:
    with open(SUBJECT_TYPE_MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_subject_type(cn_name: str) -> str:
    """中文分类名转API编码，不存在则报错"""
    mapping = load_subject_type_map()
    if cn_name not in mapping:
        available = "、".join(mapping.keys())
        raise ValueError(f"未知主题分类 '{cn_name}'，可用分类: {available}")
    return mapping[cn_name]


def merge_preset_args(preset: dict, overrides: dict) -> dict:
    """合并预设参数和用户覆盖参数，用户参数优先"""
    merged = {}
    for k, v in preset.items():
        if v is not None:
            merged[k] = v
    for k, v in overrides.items():
        if v is not None:
            merged[k] = v
    return merged


def main():
    parser = argparse.ArgumentParser(
        description="员工矩阵任务管理 - 通过API Key管理公众号与小红书AI任务"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # === 预设 ===
    subparsers.add_parser("list-presets", help="列出所有可用预设")

    # === 公众号任务 ===
    p_create_mp = subparsers.add_parser("create_mp_task", help="创建公众号任务")
    p_create_mp.add_argument("--subject", required=True, help="主题词，多条用\\n分隔")
    p_create_mp.add_argument("--preset", default="通用", help="预设名称(默认'通用')")
    p_create_mp.add_argument("--target_bite_seq", default=None, help="比特浏览器窗口序号(覆盖预设)")
    p_create_mp.add_argument("--subject_type", default=None, help="主题分类中文(覆盖预设)，如: 美食、旅游、热点等")
    p_create_mp.add_argument("--ai_model_code", default=None, help="AI模型编码(覆盖预设)")
    p_create_mp.add_argument("--image_from", default=None, help="图片来源(覆盖预设)")
    p_create_mp.add_argument("--material_group_id", type=int, default=None, help="素材组ID(覆盖预设)")
    p_create_mp.add_argument("--content_prefix", default=None, help="文章前缀(覆盖预设)")
    p_create_mp.add_argument("--content_suffix", default=None, help="文章后缀(覆盖预设)")
    p_create_mp.add_argument("--mp_publish", default=None, help="Y=直接发布,N=草稿(覆盖预设)")
    p_create_mp.add_argument("--priority", type=int, default=None, help="0=正常,1=加急(覆盖预设)")
    p_create_mp.add_argument("--auto_publish", default=None, help="Y=立即推送,N=仅创建(覆盖预设)")

    p_list_mp = subparsers.add_parser("list_mp_tasks", help="查询公众号任务列表")
    p_list_mp.add_argument("--page", type=int, default=1, help="页码")
    p_list_mp.add_argument("--page_size", type=int, default=10, help="每页数量")
    p_list_mp.add_argument("--publish_status", type=int, default=None, help="发布状态筛选")

    p_get_mp = subparsers.add_parser("get_mp_task", help="获取公众号任务详情")
    p_get_mp.add_argument("--task_id", type=int, required=True, help="任务ID")

    p_update_mp = subparsers.add_parser("update_mp_task", help="更新公众号任务状态")
    p_update_mp.add_argument("--task_id", type=int, required=True, help="任务ID")
    p_update_mp.add_argument("--publish_status", type=int, required=True, help="发布状态")
    p_update_mp.add_argument("--publish_reason", default=None, help="失败原因")

    p_delete_mp = subparsers.add_parser("delete_mp_task", help="删除公众号任务")
    p_delete_mp.add_argument("--task_id", type=int, required=True, help="任务ID")

    # === 小红书AI任务 ===
    p_create_xhs = subparsers.add_parser("create_xhs_aitask", help="创建小红书AI创作任务")
    p_create_xhs.add_argument("--input_content", required=True, help="输入内容，多条用\\n分隔")
    p_create_xhs.add_argument("--target_bite_seq", required=True, help="比特浏览器窗口序号")
    p_create_xhs.add_argument("--content_prompt_id", type=int, default=None, help="文案提示词ID")
    p_create_xhs.add_argument("--image_prompt_id", type=int, default=None, help="图片提示词ID")
    p_create_xhs.add_argument("--need_publish", default=None, help="Y=直接发布,N=草稿")
    p_create_xhs.add_argument("--image_count", type=int, default=None, help="图片数量")
    p_create_xhs.add_argument("--priority", type=int, default=None, help="0=正常,1=加急")
    p_create_xhs.add_argument("--auto_publish", default=None, help="Y=立即推送,N=仅创建")

    p_list_xhs = subparsers.add_parser("list_xhs_aitasks", help="查询小红书AI任务列表")
    p_list_xhs.add_argument("--page", type=int, default=1, help="页码")
    p_list_xhs.add_argument("--page_size", type=int, default=10, help="每页数量")
    p_list_xhs.add_argument("--publish_status", type=int, default=None, help="发布状态筛选")

    p_get_xhs = subparsers.add_parser("get_xhs_aitask", help="获取小红书AI任务详情")
    p_get_xhs.add_argument("--task_id", type=int, required=True, help="任务ID")

    p_update_xhs = subparsers.add_parser("update_xhs_aitask", help="更新小红书AI任务状态")
    p_update_xhs.add_argument("--task_id", type=int, required=True, help="任务ID")
    p_update_xhs.add_argument("--publish_status", type=int, required=True, help="发布状态")
    p_update_xhs.add_argument("--publish_reason", default=None, help="失败原因")

    p_delete_xhs = subparsers.add_parser("delete_xhs_aitask", help="删除小红书AI任务")
    p_delete_xhs.add_argument("--task_id", type=int, required=True, help="任务ID")

    # === 通用 ===
    subparsers.add_parser("check_online", help="检查Autobot客户端在线状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        result = dispatch(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({"code": 401, "msg": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"code": 500, "msg": f"请求失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)


def dispatch(args) -> dict:
    """根据命令分发到对应的处理函数"""
    cmd = args.command

    # 预设
    if cmd == "list-presets":
        presets = load_presets()
        mapping = load_subject_type_map()
        return {"code": 200, "presets": list(presets.keys()), "subject_type_map": mapping}

    # 公众号任务
    if cmd == "create_mp_task":
        presets = load_presets()
        preset_name = args.preset
        if preset_name not in presets:
            return {
                "code": 400,
                "msg": f"预设 '{preset_name}' 不存在，可用预设: {', '.join(presets.keys())}",
            }
        preset = presets[preset_name]

        overrides = {
            "target_bite_seq": args.target_bite_seq,
            "subject_type": args.subject_type,
            "ai_model_code": args.ai_model_code,
            "image_from": args.image_from,
            "material_group_id": args.material_group_id,
            "content_prefix": args.content_prefix,
            "content_suffix": args.content_suffix,
            "mp_publish": args.mp_publish,
            "priority": args.priority,
            "auto_publish": args.auto_publish,
        }
        merged = merge_preset_args(preset, overrides)

        # subject_type 中文转API编码
        merged["subject_type"] = resolve_subject_type(merged["subject_type"])

        return mp_task.create_mp_task(
            subject=args.subject.replace("\\n", "\n"),
            **merged,
        )
    elif cmd == "list_mp_tasks":
        return mp_task.list_mp_tasks(
            page=args.page,
            page_size=args.page_size,
            publish_status=args.publish_status,
        )
    elif cmd == "get_mp_task":
        return mp_task.get_mp_task(task_id=args.task_id)
    elif cmd == "update_mp_task":
        return mp_task.update_mp_task(
            task_id=args.task_id,
            publish_status=args.publish_status,
            publish_reason=args.publish_reason,
        )
    elif cmd == "delete_mp_task":
        return mp_task.delete_mp_task(task_id=args.task_id)

    # 小红书AI任务
    elif cmd == "create_xhs_aitask":
        return xhs_aitask.create_xhs_aitask(
            input_content=args.input_content.replace("\\n", "\n"),
            target_bite_seq=args.target_bite_seq,
            content_prompt_id=args.content_prompt_id,
            image_prompt_id=args.image_prompt_id,
            need_publish=args.need_publish,
            image_count=args.image_count,
            priority=args.priority,
            auto_publish=args.auto_publish,
        )
    elif cmd == "list_xhs_aitasks":
        return xhs_aitask.list_xhs_aitasks(
            page=args.page,
            page_size=args.page_size,
            publish_status=args.publish_status,
        )
    elif cmd == "get_xhs_aitask":
        return xhs_aitask.get_xhs_aitask(task_id=args.task_id)
    elif cmd == "update_xhs_aitask":
        return xhs_aitask.update_xhs_aitask(
            task_id=args.task_id,
            publish_status=args.publish_status,
            publish_reason=args.publish_reason,
        )
    elif cmd == "delete_xhs_aitask":
        return xhs_aitask.delete_xhs_aitask(task_id=args.task_id)

    # 通用
    elif cmd == "check_online":
        return client.get("/rpa/external/online")

    else:
        return {"code": 400, "msg": f"未知命令: {cmd}"}


if __name__ == "__main__":
    main()
