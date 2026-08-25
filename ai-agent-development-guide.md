# AI Agent 开发指南

## 一、什么是 AI Agent

AI Agent 不是简单的聊天机器人，而是一个能够利用大模型进行决策，并调用外部工具完成多步任务的程序。

一个典型的 Agent 可以抽象为：

> 用户请求 → 理解任务 → 规划步骤 → 调用工具 → 获取结果 → 判断是否继续 → 输出结果

Agent 的核心组成通常包括：

- 大语言模型（LLM）
- Prompt 和上下文
- 工具（Tool）
- 状态和记忆（Memory）
- 工作流或编排逻辑（Workflow/Orchestration）
- 安全控制和评估机制

## 二、开发 AI Agent 的主要流程

### 1. 明确业务问题

首先定义：

- Agent 要解决什么问题？
- 输入和输出是什么？
- 哪些步骤可以交给模型，哪些必须由程序控制？
- 是否需要调用数据库、API、搜索、文件系统等工具？
- 是否允许自动执行，还是必须人工确认？

适合优先落地的场景包括：

- 企业知识库问答
- 工单分类和处理
- 数据库查询助手
- 自动生成报告
- 代码审查助手
- 客服流程自动化

### 2. 选择模型

根据任务选择模型，不要一味追求最大模型：

- 复杂推理：使用能力更强的模型
- 分类、抽取、改写：使用更快、更便宜的模型
- 高并发场景：考虑小模型或本地模型
- 敏感数据：考虑私有化部署

常见模型来源包括：

- OpenAI、Anthropic、Google 等云端 API
- 阿里通义、智谱、DeepSeek、百度等国内模型
- Llama、Qwen 等开源模型
- Ollama、vLLM 等本地部署方案

### 3. 设计 Prompt 和输出格式

Prompt 应明确：

- 角色和职责
- 可用工具
- 约束条件
- 异常处理方式
- 输出 JSON 结构
- 何时需要人工确认

生产系统中应尽量使用结构化输出，而不是直接解析自然语言。例如：

```json
{
  "action": "query_order",
  "arguments": {
    "order_id": "123456"
  },
  "need_confirmation": false
}
```

### 4. 设计工具系统

工具是 Agent 区别于普通问答机器人的关键。工具可以是：

- Java 方法
- REST API
- 数据库查询
- 搜索引擎
- 文件处理程序
- 企业内部系统
- 消息队列
- MCP Server

工具设计注意事项：

- 参数必须明确
- 权限必须受控
- 结果格式统一
- 操作尽量幂等
- 高风险操作需要人工确认
- 不要让模型直接执行任意 SQL 或 Shell

### 5. 管理状态和记忆

常见状态包括：

- 当前会话历史
- 当前任务上下文
- 已执行的步骤
- 工具调用结果
- 用户偏好
- 长期业务记忆

不要把所有历史消息无限塞给模型，应采用：

- 摘要
- 截断
- 重要信息提取
- 向量检索
- 数据库存储
- 短期记忆和长期记忆分离

### 6. 接入 RAG

如果 Agent 需要访问企业文档、产品资料或制度规范，通常需要 RAG（检索增强生成）：

1. 文档解析
2. 文本切分
3. 向量化
4. 存入向量数据库
5. 根据问题检索
6. 将相关内容交给模型回答

常见向量数据库包括：

- Milvus
- Qdrant
- pgvector
- Elasticsearch
- Redis

### 7. 编排 Agent 流程

常见模式包括：

- 单 Agent + 多工具
- 固定工作流 + 少量模型判断
- 多 Agent 协作
- Planner-Executor
- ReAct
- 人机协同流程

实际项目中建议优先使用“工作流 + Agent 节点”，不要一开始就做完全自主、多 Agent 系统。

### 8. 增加安全和评估机制

上线前至少考虑：

- Prompt Injection
- 越权调用工具
- 敏感数据泄漏
- 虚构答案
- 恶意文件和网页内容
- 无限循环
- 成本失控
- 接口超时
- 重复执行订单、付款等操作

应建立测试集，评估：

- 答案准确率
- 工具调用正确率
- 任务完成率
- 幻觉率
- 平均响应时间
- 单次调用成本
- 人工介入比例

## 三、主流语言和框架

### Python

目前 AI Agent 生态最丰富，适合快速验证、AI 算法、数据处理、RAG 和多 Agent 系统。

常见框架：

- LangChain
- LangGraph
- LlamaIndex
- AutoGen
- CrewAI
- OpenAI Agents SDK
- Semantic Kernel

其中 LangGraph 更适合构建有状态、可控、可恢复的 Agent 流程。

### TypeScript / JavaScript

适合 Web 产品、Node.js 服务和实时交互应用。

常见选择：

- Vercel AI SDK
- LangChain.js
- OpenAI Agents SDK
- Mastra

### Java

Java 适合企业级 Agent 应用，尤其适合已有 Spring Boot、微服务、权限体系、数据库和内部系统集成能力的团队。

本节仅用于技术生态对比；如果已有 Java/Spring Boot 基础但后续希望专注 Python Agent，请直接按照第四部分学习，本项目后续不采用 Java 或 Java Agent 框架。

推荐关注：

- Spring AI
- LangChain4j
- Spring Boot
- Spring WebFlux
- Spring Security
- Resilience4j
- MCP Java SDK

简单选择建议：

- 想快速学习 AI 生态：补充 Python
- 想结合企业项目落地：Java + Spring AI 或 LangChain4j
- 想做前端交互产品：TypeScript

## 四、有 Java/Spring Boot 基础程序员的 Python + LangChain/LangGraph 学习路线

后续开发统一使用 Python、LangChain 和 LangGraph，不使用 Java 语言或 Java Agent 框架。Java/Spring Boot 经验仍然有价值：数据库、事务、并发、权限、微服务和监控等工程能力可以直接迁移。

如果你的目标是“开始编写真正的 AI Agent”，我更推荐：

> **LangGraph 为主，LangChain 作为组件库。**

简单区分：

- **LangChain**：适合快速调用模型、Prompt、工具、检索、RAG、结构化输出。
- **LangGraph**：适合编排 Agent 的状态、步骤、循环、分支、人工介入、错误重试和多 Agent 协作。

可以这样理解：

> **LangChain 是零件库，LangGraph 是流程控制器。**

### 第一阶段：补齐 Python 与异步编程基础

重点学习函数、类、异常、类型标注、虚拟环境、包管理、`async/await`、HTTP 请求、JSON、日志和 pytest。能读懂并修改一个小型 Python 项目即可，不必先学习数据科学或模型训练。

### 第二阶段：掌握大模型 API 与 LangChain Core

使用 OpenAI 兼容 API 完成普通对话、流式输出、多轮消息、Prompt 模板、结构化输出和 Token/费用统计。然后学习 LangChain 的 `ChatModel`、消息、Runnable、Parser 和回调机制，理解模型的不确定性与上下文窗口限制。

### 第三阶段：用 LangGraph 构建有状态工作流

掌握 `StateGraph`、节点、边、条件分支、循环、`MessagesState`、checkpoint 和 `thread_id`。先实现“输入 → 模型 → 输出”的单 Agent，再加入重试、最大步数、超时和人工确认。当前仓库的 CLI 对话 Agent 就是这一阶段的最小实践。

### 第四阶段：工具调用与可靠执行

用 Python 函数或 LangChain Tool 接入 REST API、数据库、文件和业务服务，学习参数校验、结构化结果、权限控制、幂等性、错误恢复和审计日志。让模型负责选择工具，让代码负责真正执行；付款、删除、状态变更等高风险操作必须人工确认。

### 第五阶段：RAG 与记忆

完成文档解析、切分、Embedding、向量库检索、引用回答和“无法确认时明确说不知道”。区分短期会话状态、摘要记忆与长期业务记忆，避免把全部历史消息无限发送给模型。

### 第六阶段：Agent 编排、MCP 与评估

学习 Planner-Executor、ReAct、子图和多 Agent 协作，但优先采用“工作流 + Agent 节点”。了解 MCP 工具协议，并建立包含答案质量、工具调用、权限边界、幻觉、延迟和成本的评测集。

### 第七阶段：生产化部署

补齐配置管理、密钥保护、缓存、并发控制、重试/熔断、链路追踪、Prompt 版本、数据脱敏、权限审计、Docker 部署和模型降级。为每个 Agent 设置最大步数、超时和预算，防止死循环与成本失控。

## 五、最重要的实践建议

1. 先做工作流，再做自主 Agent。能用固定流程解决的问题，不要交给模型自由发挥。
2. 不要一开始训练模型。大多数项目首先需要的是 API、Prompt、工具调用和 RAG。
3. 让模型负责判断，让代码负责执行。权限、事务、金额、库存和状态变更必须由程序控制。
4. 所有高风险操作都要可审计、可撤销、可人工确认。
5. 不要只测试答案质量，还要测试工具调用、权限边界和重复执行问题。
6. Agent 必须有最大步数、超时和预算限制，避免死循环和成本失控。
7. 优先构建单 Agent。多 Agent 会增加通信、调试、成本和错误传播问题。

## 六、推荐的 Python 技术栈

- Python 3.11+
- LangChain、LangGraph、langchain-openai
- python-dotenv、pytest
- PostgreSQL + pgvector 或 Qdrant
- Redis（可选）
- FastAPI（需要提供 Web API 时）
- Docker、OpenTelemetry
- OpenAI、DeepSeek 或 OpenRouter 等 OpenAI 兼容 API

## 七、学习路线总结

> Python 基础 → 模型 API → LangChain Core → LangGraph 状态图 → Tool Calling → RAG → MCP/评估 → 生产部署

重点补充的是 Python 生态、大模型交互、LangGraph 工作流、非确定性系统设计和评估方法；原有 Java 工程能力继续用于设计可靠的 Agent 系统。
