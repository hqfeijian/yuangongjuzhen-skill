# yuangongjuzhen-skill

员工矩阵系统 Claude Code Skill —— 通过 API Key 调用 RPA 任务管理接口，管理公众号矩阵任务与小红书 AI 创作任务，并支持检查 Autobot 客户端在线状态。

## 功能概览

- **公众号任务管理**：创建、查询、更新、删除公众号发布任务，支持预设快速填充参数
- **小红书 AI 创作任务管理**：创建、查询、更新、删除小红书 AI 创作任务
- **Autobot 状态检查**：检查 RPA 客户端是否在线
- **预设系统**：内置 11 种预设（通用、美食、科普冷知识、旅游、书单、热点、明星美女、人物、开源工具、软文推广、草稿），一键填充常用参数

## 获取 API Key

前往 [https://saas.rpabot.site/](https://saas.rpabot.site/) 注册账号，在管理后台的「API Key 管理」页面生成 API Key。

API Key 格式为 `sk_` + 32 位字符串。

## 安装

### 前置要求

- Python 3.8+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)

### 步骤

1. 将本仓库克隆到 Claude Code 的 skills 目录：

```bash
git clone https://github.com/<your-username>/yuangongjuzhen-skill.git ~/.claude/skills/yuangongjuzhen
```

2. 安装 Python 依赖：

```bash
pip install -r ~/.claude/skills/yuangongjuzhen/requirements.txt
```

3. 配置 API Key 环境变量：

在 `~/.claude/settings.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "yuangongjuzhen": {
        "env": {
          "RPA_API_KEY": "sk_your_api_key_here"
          }
      }
    }
  }
}
```

或在 `~/.claude/.env` 中设置：

```
RPA_API_KEY=sk_your_api_key_here
```

## 使用方式

安装完成后，在 Claude Code 对话中直接用自然语言触发，例如：

- "帮我创建一个美食主题的公众号任务"
- "查看我的公众号任务列表"
- "创建一个小红书AI创作任务"
- "检查 Autobot 是否在线"

Claude 会自动调用对应的命令。

## 命令参考

所有命令通过 `python {baseDir}/scripts/main.py <command>` 执行。

### 通用命令

| 命令 | 说明 |
|------|------|
| `list-presets` | 列出所有可用预设 |

### 公众号任务

| 命令 | 说明 |
|------|------|
| `create_mp_task` | 创建公众号任务 |
| `list_mp_tasks` | 查询公众号任务列表 |
| `get_mp_task` | 获取公众号任务详情 |
| `update_mp_task` | 更新公众号任务状态 |
| `delete_mp_task` | 删除公众号任务 |

### 小红书 AI 任务

| 命令 | 说明 |
|------|------|
| `create_xhs_aitask` | 创建小红书 AI 创作任务 |
| `list_xhs_aitasks` | 查询小红书 AI 任务列表 |
| `get_xhs_aitask` | 获取小红书 AI 任务详情 |
| `update_xhs_aitask` | 更新小红书 AI 任务状态 |
| `delete_xhs_aitask` | 删除小红书 AI 任务 |

### Autobot 状态

| 命令 | 说明 |
|------|------|
| `check_online` | 检查 Autobot 客户端在线状态 |

## 命令详细说明

### 创建公众号任务

```bash
# 使用预设（推荐）
python {baseDir}/scripts/main.py create_mp_task --subject "火锅美食推荐" --preset 美食

# 使用默认预设（通用）
python {baseDir}/scripts/main.py create_mp_task --subject "今日新闻"

# 预设 + 覆盖参数
python {baseDir}/scripts/main.py create_mp_task --subject "火锅" --preset 美食 --target_bite_seq "2"

# 仅创建草稿
python {baseDir}/scripts/main.py create_mp_task --subject "测试文章" --preset 草稿
```

**参数：**

| 参数 | 必需 | 说明 |
|------|------|------|
| `--subject` | 是 | 主题词，多条用 `\n` 分隔，最多 8 行 |
| `--preset` | 否 | 预设名称（中文），默认"通用" |
| `--target_bite_seq` | 否 | 比特浏览器窗口序号，覆盖预设值 |
| `--subject_type` | 否 | 主题分类（中文），覆盖预设值 |
| `--ai_model_code` | 否 | AI 模型编码 |
| `--image_from` | 否 | 图片来源：`network` / `origin` / `material_group` |
| `--material_group_id` | 否 | 素材组 ID |
| `--content_prefix` | 否 | 文章前缀（markdown 格式） |
| `--content_suffix` | 否 | 文章后缀（markdown 格式） |
| `--mp_publish` | 否 | `Y`=直接发布，`N`=保存草稿 |
| `--priority` | 否 | `0`=正常，`1`=加急 |
| `--auto_publish` | 否 | `Y`=立即推送，`N`=仅创建 |

### 创建小红书 AI 创作任务

```bash
python {baseDir}/scripts/main.py create_xhs_aitask \
  --input_content "职场穿搭分享\n夏日护肤攻略" \
  --target_bite_seq "1" \
  --auto_publish Y
```

**参数：**

| 参数 | 必需 | 说明 |
|------|------|------|
| `--input_content` | 是 | 输入内容，多条用 `\n` 分隔 |
| `--target_bite_seq` | 是 | 比特浏览器窗口序号 |
| `--content_prompt_id` | 否 | 文案提示词 ID，0=系统内置 |
| `--image_prompt_id` | 否 | 图片提示词 ID，0=系统内置 |
| `--need_publish` | 否 | `Y`=直接发布，`N`=草稿 |
| `--image_count` | 否 | 图片数量，默认 1 |
| `--priority` | 否 | `0`=正常，`1`=加急 |
| `--auto_publish` | 否 | `Y`=立即推送，`N`=仅创建 |

### 查询任务列表

```bash
# 公众号任务
python {baseDir}/scripts/main.py list_mp_tasks --page 1 --page_size 10 --publish_status 0

# 小红书 AI 任务
python {baseDir}/scripts/main.py list_xhs_aitasks --page 1 --page_size 10
```

**publish_status 状态值：**

| 值 | 含义 |
|----|------|
| 0 | 待生成 |
| 1 | 待发布 |
| 2 | 成功 |
| 3 | 失败 |
| 4 | 草稿 |
| 5 | 超时成功 |

### 获取/更新/删除任务

```bash
# 获取详情
python {baseDir}/scripts/main.py get_mp_task --task_id 123
python {baseDir}/scripts/main.py get_xhs_aitask --task_id 456

# 更新状态
python {baseDir}/scripts/main.py update_mp_task --task_id 123 --publish_status 3 --publish_reason "生成失败"
python {baseDir}/scripts/main.py update_xhs_aitask --task_id 456 --publish_status 2

# 删除
python {baseDir}/scripts/main.py delete_mp_task --task_id 123
python {baseDir}/scripts/main.py delete_xhs_aitask --task_id 456
```

## 预设列表

| 预设名 | 主题分类 | 比特浏览器窗口 | 发布方式 |
|--------|----------|---------------|----------|
| 通用 | 通用 | 1 | 直接发布 |
| 美食 | 美食 | 1 | 直接发布 |
| 科普冷知识 | 科普冷知识 | 1 | 直接发布 |
| 旅游 | 旅游 | 1 | 直接发布 |
| 书单 | 书单 | 1 | 直接发布 |
| 热点 | 热点 | 1 | 直接发布 |
| 明星美女 | 明星美女 | 1 | 直接发布 |
| 人物 | 人物 | 1 | 直接发布 |
| 开源工具 | 开源工具 | 2 | 直接发布 |
| 软文推广 | 软文推广 | 1 | 直接发布 |
| 草稿 | 通用 | 1 | 保存草稿 |

## 主题分类映射

用户使用中文分类名，系统自动转换为 API 编码：

| 中文名 | API 编码 |
|--------|----------|
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

## 错误处理

| 错误 | 说明 |
|------|------|
| 401 Unauthorized | `RPA_API_KEY` 未配置或无效/已禁用/已过期 |
| 积分不足 | 当前积分不足，需充值或减少任务数量 |
| 权限不足 | 需联系管理员开通机器人权限 |
| 任务不存在 | 任务 ID 不正确或无权访问 |
| 未知分类 | 使用了不存在的主题分类名 |

## 安全注意事项

- `RPA_API_KEY` 为敏感信息，**不要**在对话中暴露完整的 API Key
- 创建任务前建议先调用 `check_online` 确认 RPA 客户端在线，否则 `auto_publish=Y` 的任务无法立即执行
- 删除操作为软删除，已删除的任务无法恢复

## 项目结构

```
yuangongjuzhen-skill/
├── SKILL.md                  # Skill 定义文件（Claude Code 读取）
├── requirements.txt          # Python 依赖
├── README.md                 # 本文件
└── scripts/
    ├── __init__.py
    ├── main.py               # 命令入口与分发
    ├── client.py             # API 客户端封装
    ├── mp_task.py            # 公众号任务操作
    ├── xhs_aitask.py         # 小红书 AI 任务操作
    ├── presets.json          # 预设配置
    └── subject_type_map.json # 主题分类映射
```

## License

MIT
