---
name: yuangongjuzhen
description: 员工矩阵系统，公众号矩阵与小红书AI任务管理Skill。通过API Key调用RPA任务管理接口，创建、查询、更新和删除公众号任务与小红书AI创作任务，并支持检查Autobot客户端在线状态。
version: 1.2.0
metadata:
  openclaw:
    requires:
      env: ["RPA_API_KEY"]
    os: ["darwin", "linux", "win32"]
user-invocable: true
---

# 员工矩阵任务管理 Skill

此Skill允许你通过RPA系统的外部API管理公众号任务和小红书AI创作任务。所有操作均通过API Key认证，Key从环境变量 `RPA_API_KEY` 获取。

## 前提条件

- 必须配置环境变量 `RPA_API_KEY`（你的RPA系统API Key，格式为 `sk_` + 32位字符串）
- API Key可在RPA管理后台的"API Key管理"页面生成
- 如果未配置 `RPA_API_KEY`，所有命令将返回错误提示

## API基础信息

- **Base URL**: `http://127.0.0.1:48081`
- **认证方式**: 所有请求通过 `X-API-Key` Header 传递 `RPA_API_KEY`

## 预设功能

创建公众号任务时可使用预设快速填充常用参数。预设名和主题分类统一使用**中文**，内部自动转换为API编码。

### 列出所有预设
```bash
python {baseDir}/scripts/main.py list-presets
```

### 主题分类映射

用户使用中文分类名，系统自动转换为API编码：

| 中文名 | API编码 |
|--------|---------|
| 通用 | general |
| 美食 | meishi |
| 科普冷知识 | lengzhishi |
| 旅游 | lvyou |
| 书单 | booklist |
| 热点 | redian |
| 明星美女 | mingxing_meinv |
| 人物 | renwu |
| 开源工具 | opensource_tool |
| 软文推广 | ads_article |

### 可用预设

| 预设名 | subject_type | target_bite_seq | mp_publish |
|--------|-------------|-----------------|------------|
| 通用 | 通用 | 1 | Y |
| 美食 | 美食 | 1 | Y |
| 科普冷知识 | 科普冷知识 | 1 | Y |
| 旅游 | 旅游 | 1 | Y |
| 书单 | 书单 | 1 | Y |
| 热点 | 热点 | 1 | Y |
| 明星美女 | 明星美女 | 1 | Y |
| 人物 | 人物 | 1 | Y |
| 开源工具 | 开源工具 | 2 | Y |
| 软文推广 | 软文推广 | 1 | Y |
| 草稿 | 通用 | 1 | N |

---

## 可用命令

所有命令通过 `{baseDir}/scripts/main.py` 执行。

---

### 1. 创建公众号任务 (create_mp_task)

创建一个新的公众号发布任务。

**简化用法（推荐）：**
```bash
# 使用预设
python {baseDir}/scripts/main.py create_mp_task --subject "火锅美食推荐" --preset 美食

# 使用默认预设(通用)
python {baseDir}/scripts/main.py create_mp_task --subject "今日新闻"

# 预设+覆盖参数
python {baseDir}/scripts/main.py create_mp_task --subject "火锅" --preset 美食 --target_bite_seq "2"

# 仅创建草稿
python {baseDir}/scripts/main.py create_mp_task --subject "测试文章" --preset 草稿
```

**参数:**
- `subject` (string, 必需): 主题词，一条一行，最多8行。换行符分隔多个子任务主题。
- `preset` (string, 可选): 预设名称（中文），默认"通用"。
- `target_bite_seq` (string, 可选): 比特浏览器窗口序号，覆盖预设值
- `subject_type` (string, 可选): 主题分类（中文），覆盖预设值。可选值: 通用、美食、科普冷知识、旅游、书单、热点、明星美女、人物、开源工具、软文推广
- `ai_model_code` (string, 可选): AI模型编码，不填则使用系统默认模型
- `image_from` (string, 可选): 图片来源，覆盖预设值。可选值: network, origin, material_group
- `material_group_id` (int, 可选): 素材组ID
- `content_prefix` (string, 可选): 文章前缀，markdown格式
- `content_suffix` (string, 可选): 文章后缀，markdown格式
- `mp_publish` (string, 可选): Y=直接发布, N=保存草稿，覆盖预设值
- `priority` (int, 可选): 0=正常, 1=加急，覆盖预设值
- `auto_publish` (string, 可选): Y=立即推送, N=仅创建，覆盖预设值

**返回示例:**
```json
{
  "code": 200,
  "msg": "任务创建成功",
  "data": null
}
```

---

### 2. 查询公众号任务列表 (list_mp_tasks)

分页查询当前用户的公众号任务列表。

**参数:**
- `page` (integer, 可选): 页码，默认1。
- `page_size` (integer, 可选): 每页数量，默认10。
- `publish_status` (integer, 可选): 按发布状态筛选。可选值: 0(待生成), 1(待发布), 2(成功), 3(失败), 4(草稿), 5(超时成功)。

**返回示例:**
```json
{
  "code": 200,
  "msg": "查询成功",
  "rows": [
    {
      "id": 123,
      "subject": "主题词",
      "targetBiteSeq": "1",
      "mpPublishStatus": 0,
      "autoPublish": "Y",
      "createTime": "2026-05-25 10:00:00"
    }
  ],
  "total": 1
}
```

---

### 3. 获取公众号任务详情 (get_mp_task)

获取单个公众号任务的详细信息，包含子任务列表。

**参数:**
- `task_id` (integer, 必需): 任务ID。

**返回示例:**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "id": 123,
    "subject": "主题词1\n主题词2",
    "targetBiteSeq": "1",
    "mpPublishStatus": 0,
    "autoPublish": "Y",
    "subTaskList": [
      {"id": 456, "subject": "主题词1", "mpPublishStatus": 0},
      {"id": 457, "subject": "主题词2", "mpPublishStatus": 0}
    ]
  }
}
```

---

### 4. 更新公众号任务状态 (update_mp_task)

更新公众号任务的发布状态。

**参数:**
- `task_id` (integer, 必需): 任务ID。
- `publish_status` (integer, 必需): 发布状态。可选值: 0(待生成), 1(待发布), 2(成功), 3(失败), 4(草稿), 5(超时成功)。
- `publish_reason` (string, 可选): 失败原因，仅在状态为3(失败)时填写。

**返回示例:**
```json
{"code": 200, "msg": "操作成功"}
```

---

### 5. 删除公众号任务 (delete_mp_task)

删除指定公众号任务（软删除）。

**参数:**
- `task_id` (integer, 必需): 任务ID。

**返回示例:**
```json
{"code": 200, "msg": "操作成功"}
```

---

### 6. 创建小红书AI创作任务 (create_xhs_aitask)

创建一个新的小红书AI创作任务。

**参数:**
- `input_content` (string, 必需): 输入内容，可以是关键词或小红书笔记链接。多条内容用换行符分隔，每条生成一个任务。
- `target_bite_seq` (string, 必需): 比特浏览器窗口序号。
- `content_prompt_id` (integer, 可选): 文案提示词ID，0=系统内置。默认0。
- `image_prompt_id` (integer, 可选): 图片提示词ID，0=系统内置。默认0。
- `need_publish` (string, 可选): Y=直接发布, N=保存草稿。默认"Y"。
- `image_count` (integer, 可选): 图片数量，默认1。
- `priority` (integer, 可选): 0=正常, 1=加急。默认0。
- `auto_publish` (string, 可选): Y=创建后立即推送RPA客户端执行, N=仅创建不推送。默认"Y"。

**返回示例:**
```json
{
  "code": 200,
  "msg": "成功新增2条任务"
}
```

**示例调用:**
```bash
python {baseDir}/scripts/main.py create_xhs_aitask --input_content "职场穿搭分享\n夏日护肤攻略" --target_bite_seq "1" --auto_publish Y
```

---

### 7. 查询小红书AI任务列表 (list_xhs_aitasks)

分页查询当前用户的小红书AI创作任务列表。

**参数:**
- `page` (integer, 可选): 页码，默认1。
- `page_size` (integer, 可选): 每页数量，默认10。
- `publish_status` (integer, 可选): 按发布状态筛选。可选值: 0(待生成), 1(待发布), 2(成功), 3(失败), 4(草稿), 5(超时成功)。

---

### 8. 获取小红书AI任务详情 (get_xhs_aitask)

获取单个小红书AI创作任务的详细信息。

**参数:**
- `task_id` (integer, 必需): 任务ID。

---

### 9. 更新小红书AI任务状态 (update_xhs_aitask)

更新小红书AI创作任务的发布状态。

**参数:**
- `task_id` (integer, 必需): 任务ID。
- `publish_status` (integer, 必需): 发布状态。
- `publish_reason` (string, 可选): 失败原因。

---

### 10. 删除小红书AI任务 (delete_xhs_aitask)

删除指定小红书AI创作任务。

**参数:**
- `task_id` (integer, 必需): 任务ID。

---

### 11. 检查Autobot在线状态 (check_online)

检查当前用户的RPA Autobot客户端是否在线。

**参数:** 无

**返回示例:**
```json
{
  "code": 200,
  "msg": "操作成功",
  "online": true
}
```

---

## 错误处理

- **401 Unauthorized**: `RPA_API_KEY` 未配置或无效/已禁用/已过期。请提示用户检查API Key配置。
- **积分不足**: 返回 `积分不足，当前积分=X，需要=Y`。请提示用户充值或减少任务数量。
- **权限不足**: 返回 `请先联系管理员开通机器人权限`。请提示用户联系管理员开通对应机器人。
- **任务不存在**: 返回 `任务不存在或无权访问`。请提示用户检查任务ID是否正确。
- **未知分类**: 返回可用中文分类名列表。请提示用户使用正确的中文分类名。
- **网络错误**: 请提示用户检查网络连接和API服务是否可用。

## 安全注意事项

- `RPA_API_KEY` 为敏感信息，**绝对不要**在对话中显示完整的API Key值。
- 创建任务前建议先调用 `check_online` 确认RPA客户端在线，若不在线则 `auto_publish=Y` 的任务将无法立即执行。
- 删除操作为软删除，已删除的任务无法恢复。