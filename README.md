# CareerAgent

> 基于 LangGraph + RAG 的 AI 岗位匹配与求职分析 Agent

CareerAgent 是一个面向求职场景的 AI Agent 应用，旨在帮助求职者快速理解招聘 JD，并结合个人简历分析岗位匹配情况。

用户输入岗位 JD 后，系统通过 LangGraph 驱动 Agent，根据岗位要求自主调用 JD 分析、简历检索、技能匹配等工具，同时利用 RAG 从个人简历知识库中检索相关项目经历和技术能力，最终生成岗位匹配分析结果。

项目采用前后端分离架构：

- 后端：Python + FastAPI + LangChain + LangGraph + DeepSeek + RAG + Chroma
- 前端：Vue 3 + TypeScript + Vite + Element Plus + Axios

---

## ✨ 核心功能

### 1. AI 岗位 JD 分析

输入招聘岗位 JD，Agent 自动提取：

- 岗位名称
- 技术技能
- 工作职责
- 学历要求
- 工作经验
- 加分技能

例如：

```text
AI Agent 开发工程师

技术要求：
Python
LangChain
LangGraph
RAG
FastAPI

经验要求：
具有 Agent 项目开发经验
```

系统会将非结构化 JD 转换为结构化岗位信息。

---

### 2. 简历 RAG 检索

系统将用户 PDF 简历构建成向量知识库。

处理流程：

```text
PDF 简历
   ↓
PyPDFLoader
   ↓
文本解析
   ↓
RecursiveCharacterTextSplitter
   ↓
文本 Chunk
   ↓
BGE Embedding
   ↓
Chroma Vector Store
```

当前使用的 Embedding 模型：

```text
BAAI/bge-small-zh-v1.5
```

当用户分析岗位时，系统会根据岗位要求检索简历中相关的：

- 技术技能
- 项目经历
- 工作经历
- 技术栈
- 相关实践经验

从而让 LLM 基于用户真实简历内容进行分析，而不是完全依赖模型自身推测。

---

### 3. Agent Tool Calling

项目使用 LangChain Tool Calling，让 LLM 可以根据当前上下文判断是否需要调用工具。

当前项目包含：

- 天气查询工具
- 计算器工具
- 搜索工具
- JD 分析工具
- 简历 RAG 检索工具
- 技能匹配工具

工具通过 LangChain `@tool` 暴露给 LLM。

例如：

```python
@tool
def analyze_jd(jd_text: str) -> str:
    ...
```

然后通过：

```python
llm_with_tools = llm.bind_tools(tools)
```

将工具提供给 Agent。

---

### 4. LangGraph Agent 工作流

使用 LangGraph 构建 Agent 工作流。

核心流程：

```text
                 ┌─────────────┐
                 │    Agent    │
                 └──────┬──────┘
                        │
                 是否需要调用 Tool？
                    /        \
                  是          否
                  ↓            ↓
            ┌──────────┐      END
            │  Tools   │
            └────┬─────┘
                 │
                 ↓
               Agent
```

Agent 根据 LLM 返回的 `tool_calls` 判断下一步。

核心路由逻辑：

```python
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

---

### 5. Agent Memory

项目使用 LangGraph Checkpointer 保存 Agent 状态。

通过：

```python
config = {
    "configurable": {
        "thread_id": "demo_user_001"
    }
}
```

区分不同会话。

当前开发阶段使用：

```text
InMemorySaver
```

实现 Agent 会话状态保存。

---

### 6. 简历在线上传

前端提供「我的简历」页面，用户可以上传新的 PDF 简历。

上传流程：

```text
新的 PDF 简历
      ↓
文件格式校验
      ↓
文件大小校验
      ↓
保存 data/resume.pdf
      ↓
删除旧 resume Collection
      ↓
重新解析 PDF
      ↓
重新文本切分
      ↓
重新生成 Embedding
      ↓
重新创建 Chroma Collection
      ↓
新的简历立即用于岗位分析
```

当前限制：

```text
文件格式：PDF
最大大小：10 MB
```

---

### 7. Markdown 分析结果

Agent 返回的分析结果使用 Markdown 格式。

前端使用：

- `markdown-it`
- `DOMPurify`

进行 Markdown 渲染和 HTML 安全处理。

支持：

- 标题
- 无序列表
- 有序列表
- 表格
- 代码
- 引用
- 链接

---

### 8. Word 分析报告

项目支持将岗位分析结果生成 Word 报告。

目标流程：

```text
Agent 分析
    ↓
生成分析结果
    ↓
点击「下载 Word」
    ↓
POST /report/download
    ↓
FastAPI 生成 DOCX
    ↓
浏览器下载
```

Word 报告生成使用：

```text
python-docx
```

---

# 🎯 项目目标

CareerAgent 希望解决传统求职过程中以下问题：

```text
招聘 JD
   ↓
人工阅读
   ↓
判断岗位要求
   ↓
翻阅简历
   ↓
寻找相关经历
   ↓
人工判断匹配程度
   ↓
整理技能缺口
```

通过 Agent 将这一过程自动化：

```text
招聘 JD
   ↓
AI Agent
   ├── JD 分析
   ├── 简历 RAG 检索
   ├── 技能匹配
   └── 综合分析
         ↓
岗位匹配报告
```

---

# 🏗️ 系统架构

```text
┌──────────────────────────────────────────────┐
│                  Vue 3 Frontend              │
│                                              │
│  岗位分析 │ 分析历史 │ 我的简历              │
│                                              │
│  JD 输入 / 分析结果 / 简历上传 / 报告下载    │
└──────────────────────┬───────────────────────┘
                       │ HTTP
                       ↓
┌──────────────────────────────────────────────┐
│                  FastAPI                     │
│                                              │
│  /chat                                       │
│  /resume/upload                              │
│  /report/download                            │
└──────────────────────┬───────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────┐
│                LangGraph Agent               │
│                                              │
│              ┌─────────────┐                 │
│              │    Agent    │                 │
│              └──────┬──────┘                 │
│                     ↓                        │
│              Tool Calling                    │
│                     ↓                        │
│              ┌─────────────┐                 │
│              │    Tools    │                 │
│              └──────┬──────┘                 │
│                     ↓                        │
│                   Agent                      │
└───────────────┬──────────────────┬───────────┘
                │                  │
                ↓                  ↓
       ┌────────────────┐  ┌─────────────────┐
       │   DeepSeek     │  │   Resume RAG    │
       │      LLM       │  │                 │
       └────────────────┘  │ BGE Embedding   │
                           │       ↓         │
                           │    Chroma        │
                           └─────────────────┘
```

---

# 🔄 核心业务流程

用户输入：

```text
帮我分析这个 Agent 开发岗位我匹配多少，
有哪些优势和不足？
```

系统执行：

```text
① 用户输入问题
        ↓
② LangGraph Agent 接收消息
        ↓
③ LLM 判断需要调用哪些工具
        ↓
④ 调用 JD Analyzer
        ↓
⑤ 提取岗位要求
        ↓
⑥ 调用 Resume Search
        ↓
⑦ Chroma 检索简历相关内容
        ↓
⑧ Skill Matcher 进行匹配
        ↓
⑨ LLM 综合分析
        ↓
⑩ 返回岗位分析报告
```

---

# 🤖 Agent 工作流

## Agent State

项目使用统一的 Agent State 保存工作过程中的信息：

```python
from typing import TypedDict, Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):

    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    jd_text: str

    job_analysis: JobAnalysis

    skill_match: SkillMatchResult

    final_report: str
```

State 可以保存：

- 对话消息
- JD 文本
- JD 分析结果
- 技能匹配结果
- 最终分析报告

---

## Agent Node

Agent 节点负责调用 LLM：

```python
llm_with_tools = llm.bind_tools(tools)


def agent_node(state):
    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }
```

---

## Tool Node

LangGraph 使用 ToolNode 执行实际工具。

执行过程：

```text
LLM
 ↓
生成 tool_calls
 ↓
ToolNode
 ↓
执行 Python Tool
 ↓
返回 ToolMessage
 ↓
Agent
 ↓
继续判断
```

---

## Workflow

核心工作流：

```text
StateGraph
    │
    ├── agent
    │
    └── tools
          │
          └────→ agent
```

条件路由：

```text
Agent
  │
  ├── 有 tool_calls → Tools
  │                    │
  │                    ↓
  │                  Agent
  │
  └── 无 tool_calls → END
```

---

# 🧠 RAG 简历检索

## 1. PDF 加载

使用：

```python
from langchain_community.document_loaders import PyPDFLoader
```

加载：

```text
data/resume.pdf
```

---

## 2. 文本切分

使用：

```python
RecursiveCharacterTextSplitter
```

当前配置：

```python
chunk_size=500
chunk_overlap=100
```

将完整简历切分成多个文本 Chunk。

---

## 3. Embedding

使用：

```text
BAAI/bge-small-zh-v1.5
```

将文本转换成向量。

---

## 4. Chroma

向量数据库：

```text
Chroma
```

数据目录：

```text
data/chroma
```

Collection：

```text
resume
```

---

## 5. 相似度检索

核心方法：

```python
search_resume(
    query,
    k=3
)
```

例如：

```text
查询：

岗位要求和技能：
Python、FastAPI、LangChain、RAG、Agent
```

系统会从简历向量库中检索最相关的内容。

---

# 📄 简历更新机制

当用户上传新的 PDF 简历时：

```text
PDF
 ↓
UploadFile
 ↓
格式校验
 ↓
大小校验
 ↓
保存 resume.pdf
 ↓
删除旧 resume Collection
 ↓
重新加载
 ↓
重新切分
 ↓
Embedding
 ↓
Chroma
```

核心代码：

```python
def rebuild_resume_vector_store():

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    vector_store.delete_collection()

    chunks = load_resume(RESUME_PATH)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )

    return vector_store
```

项目只删除：

```text
resume
```

Collection，而不是整个：

```text
data/chroma
```

从而避免影响未来其他向量数据。

---

# 🧩 技能匹配

岗位分析结果和简历检索结果会进一步交给 Skill Matcher。

匹配过程：

```text
JD
 ↓
岗位技能
 ↓
+
简历相关内容
 ↓
Skill Matcher
 ↓
已掌握技能
技能缺口
相关经历
加分项
```

示例：

```text
已掌握：

- Python
- FastAPI
- LangChain
- LangGraph
- RAG

技能缺口：

- Redis
- Kubernetes

相关经历：

- CloudSmart AI Agent
- 智媒运营 Agent
```

---

# 🛠️ 技术栈

## 后端

| 技术 | 用途 |
|---|---|
| Python | 后端开发 |
| FastAPI | REST API |
| Uvicorn | ASGI Server |
| LangChain | LLM / Tool 集成 |
| LangGraph | Agent 工作流 |
| DeepSeek | 大语言模型 |
| Chroma | 向量数据库 |
| HuggingFace Embeddings | 文本向量化 |
| PyPDFLoader | PDF 简历解析 |
| Pydantic | 数据模型与校验 |
| python-docx | Word 报告生成 |

---

## 前端

| 技术 | 用途 |
|---|---|
| Vue 3 | 前端框架 |
| TypeScript | 类型系统 |
| Vite | 构建工具 |
| Element Plus | UI 组件 |
| Axios | HTTP 请求 |
| markdown-it | Markdown 渲染 |
| DOMPurify | HTML 安全处理 |

---

# 📁 项目结构

```text
demo/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── agent/
│   │   │   └── llm.py
│   │   │
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── resume.py
│   │   │   └── report.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── graph/
│   │   │   ├── nodes.py
│   │   │   ├── router.py
│   │   │   ├── state.py
│   │   │   ├── tools_node.py
│   │   │   └── workflow.py
│   │   │
│   │   ├── models/
│   │   │   ├── jd.py
│   │   │   └── skill_match.py
│   │   │
│   │   ├── rag/
│   │   │   ├── loader.py
│   │   │   ├── embedding.py
│   │   │   ├── vector_store.py
│   │   │   ├── manager.py
│   │   │   ├── qa.py
│   │   │   └── test_retriever.py
│   │   │
│   │   ├── report/
│   │   │   └── word_generator.py
│   │   │
│   │   └── tools/
│   │       ├── calculator.py
│   │       ├── search.py
│   │       ├── weather.py
│   │       ├── jd_analyzer.py
│   │       ├── resume_search.py
│   │       └── skill_matcher.py
│   │
│   ├── data/
│   │   ├── resume.pdf
│   │   └── chroma/
│   │
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── App.vue
│   │   └── main.ts
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

> 项目目录会随着开发继续迭代，上述结构以当前项目架构为准。

---

# 💻 环境要求

推荐环境：

```text
Python >= 3.11
Node.js >= 18
npm >= 9
```

当前开发环境：

```text
Windows
Python 3.14
Vue 3
Vite
```

---

# 🚀 快速开始

## 1. 获取项目

```bash
git clone <your-repository-url>

cd demo
```

---

# 🔧 后端配置

进入后端目录：

```powershell
cd backend
```

创建虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.venv\Scripts\Activate.ps1
```

如果使用 uv：

```powershell
uv venv
```

安装依赖：

```powershell
uv pip install -r requirements.txt
```

或者：

```powershell
pip install -r requirements.txt
```

---

# 🔑 配置 DeepSeek API

在：

```text
backend/.env
```

配置：

```env
OPENAI_API_KEY=你的DeepSeek_API_Key
```

项目通过 OpenAI-compatible API 调用 DeepSeek：

```python
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=settings.openai_api_key,
    base_url="https://api.deepseek.com",
    temperature=0
)
```

> 不要将真实 API Key 提交到 GitHub。

建议在：

```text
.gitignore
```

中加入：

```text
.env
.venv/
__pycache__/
data/chroma/
```

---

# ▶️ 启动后端

进入：

```powershell
cd backend
```

启动：

```powershell
uvicorn app.main:app --reload
```

默认地址：

```text
http://127.0.0.1:8000
```

Swagger API 文档：

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 启动前端

新开一个终端。

进入：

```powershell
cd frontend
```

安装依赖：

```powershell
npm install
```

启动：

```powershell
npm run dev
```

默认地址：

```text
http://localhost:5173
```

---

# 🔌 前后端通信

前端通过 Axios 调用 FastAPI：

```text
Vue 3
  ↓
Axios
  ↓
FastAPI
  ↓
LangGraph
  ↓
LLM / Tools / RAG
```

后端默认地址：

```text
http://127.0.0.1:8000
```

前端默认地址：

```text
http://localhost:5173
```

---

# 📡 API 接口

## 岗位分析

```http
GET /chat
```

参数：

```text
message
```

示例：

```text
GET /chat?message=帮我分析这个AI Agent开发岗位
```

返回：

```json
{
  "answer": "岗位分析结果..."
}
```

---

## 上传简历

```http
POST /resume/upload
```

请求：

```text
multipart/form-data
```

参数：

```text
file
```

限制：

```text
PDF
≤ 10MB
```

返回：

```json
{
  "success": true,
  "filename": "resume.pdf",
  "size": 123456,
  "message": "简历及向量知识库更新成功"
}
```

---

## 下载 Word 报告

```http
POST /report/download
```

请求：

```json
{
  "content": "岗位分析 Markdown 内容"
}
```

返回：

```text
application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

---

# 🧪 测试

## 测试 RAG 检索

进入：

```text
backend
```

运行：

```powershell
python -m app.rag.test_retriever
```

---

## 测试简历向量库重建

```powershell
python -m app.rag.test_rebuild
```

---

## 测试技能匹配

```powershell
python -m app.tools.test_skill_matcher
```

---

## 测试 Word 生成

```powershell
python -m app.report.test_word
```

---

# ⚙️ 结构化输出处理

岗位分析使用 Pydantic：

```python
class JobAnalysis(BaseModel):

    job_title: str

    technical_skills: list[str]

    responsibilities: list[str]

    education: str

    experience: str

    bonus_skills: list[str]
```

由于当前 DeepSeek API 环境下没有使用原生：

```python
llm.with_structured_output(...)
```

项目采用：

```text
Prompt
 ↓
要求 LLM 输出 JSON
 ↓
json.loads()
 ↓
Pydantic Validation
```

保证最终数据结构符合预期。

---

# 🛡️ Agent 稳定性

Agent Tool Calling 存在潜在循环问题：

```text
Agent
 ↓
Tool
 ↓
Agent
 ↓
Tool
 ↓
Agent
 ↓
...
```

后续可以增加：

- Tool 调用次数限制
- 重复 Tool 检测
- 超时控制
- 错误日志
- Request ID
- Tool 调用链追踪

提高 Agent 在实际生产环境中的稳定性。

---

# 🌟 项目亮点

## 1. 完整 Agent 应用链路

项目不是简单的：

```python
llm.invoke(...)
```

而是构建了：

```text
LLM
 +
Tool Calling
 +
LangGraph
 +
RAG
 +
Memory
 +
FastAPI
 +
Vue3
```

组成完整的 Agent 应用。

---

## 2. Agent + RAG

将 Agent 的工具调用能力与简历 RAG 结合：

```text
岗位 JD
    ↓
Agent
    ↓
JD Analyzer
    ↓
Resume Search
    ↓
Chroma
    ↓
相关简历内容
    ↓
Skill Matcher
    ↓
最终分析
```

---

## 3. 动态简历知识库

用户上传新的简历后，可以自动重新生成：

```text
PDF
 ↓
Chunk
 ↓
Embedding
 ↓
Chroma
```

无需修改代码。

---

## 4. 前后端分离

前端：

```text
Vue3 + TypeScript + Element Plus
```

后端：

```text
FastAPI + LangGraph
```

通过 REST API 解耦。

---

## 5. 面向真实业务场景

项目不是简单的聊天机器人，而是围绕实际求职场景设计：

```text
岗位 JD
 +
个人简历
 ↓
岗位匹配分析
```

可以进一步扩展为完整的 AI 求职助手。

---


# 📌 简历项目描述

如果将 CareerAgent 写进简历，可以使用以下描述：

### CareerAgent —— AI 岗位匹配与求职分析 Agent

**技术栈：**

```text
Python / FastAPI / LangChain / LangGraph /
DeepSeek / RAG / Chroma / BGE Embedding /
Vue3 / TypeScript / Element Plus
```

**项目描述：**

> 基于 LangGraph 构建 AI 岗位匹配 Agent，针对求职场景实现 JD 解析、简历 RAG 检索、技能匹配与分析报告生成。通过 Tool Calling 让 Agent 根据上下文自主调用 JD 分析、简历检索等工具，并使用 Chroma + BGE Embedding 构建简历向量知识库，实现岗位要求与用户项目经历的语义匹配；后端基于 FastAPI 提供 REST API，前端使用 Vue3 + Element Plus 实现岗位分析及简历管理界面。

**核心工作：**

- 使用 LangGraph 构建 Agent 状态图，通过 `StateGraph`、条件路由及 `ToolNode` 实现 Agent → Tool → Agent 的循环工作流。
- 基于 LangChain Tool Calling 实现 JD 分析、简历检索、技能匹配等工具，并根据上下文动态决定工具调用。
- 使用 PyPDFLoader + RecursiveCharacterTextSplitter 对 PDF 简历进行解析和 Chunk 切分，结合 BGE Embedding 和 Chroma 构建简历 RAG 知识库。
- 实现简历在线上传与向量库重建机制，新简历上传后自动更新 RAG 数据源。
- 使用 Pydantic 对 LLM JSON 输出进行结构化校验，提高 Agent 输出稳定性。
- 使用 FastAPI 构建后端 API，Vue3 + Element Plus 构建岗位分析及简历管理界面。

---

# 🎓 项目学习重点

通过本项目主要实践了以下 Agent 开发能力：

```text
                    CareerAgent
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
   LLM 接入        Tool Calling         RAG
        │               │                │
    DeepSeek        LangChain         Chroma
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                    LangGraph
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
           State              Workflow
              │                   │
              └─────────┬─────────┘
                        ↓
                     FastAPI
                        ↓
                      Vue3
```

---

# 📄 License

本项目主要用于个人学习、Agent 开发实践以及求职作品展示。

如用于商业用途，请根据项目依赖组件及第三方模型服务的相关许可协议进行确认。
