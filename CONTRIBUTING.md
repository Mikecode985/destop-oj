# 贡献指南

感谢你愿意帮助改进本地 OJ。

## 开始之前

- 请先确认本地能运行：`python server.py --open`；
- 检查 Python：`python --version`；
- 检查 C++ 编译环境：`g++ --version`。

## 提交 Issue

请附上：

1. 你使用的系统（Windows / macOS / Linux）和 Python 版本；
2. 复现步骤；
3. 题号或页面名称；
4. 浏览器控制台报错、命令行报错或错误卡片截图；
5. 如果和判题有关，附上最小可复现代码。

请勿粘贴：

- API Key；
- Cookie、登录凭据；
- 个人路径、姓名、聊天记录等隐私信息。

## 提交 Pull Request

- 保持改动范围聚焦，一道题或一个功能一个 PR；
- 前端修改请运行 `node --check web/app.js`；
- 服务端修改请运行 `python -m py_compile server.py`；
- 尽量补上对应的验收脚本或说明；
- 不要提交 `data/progress.json`、`data/submissions.json`、日志和 AI Key。

## 题库修正

如果题目描述、样例或测试数据有误，请提供：

- 题号；
- 当前错误行为；
- 期望行为；
- 可用于验证的输入/输出；
- 如果方便，附上你的参考代码。

## 代码风格

- 前端保持原生 HTML / CSS / JavaScript，不引入构建步骤；
- Python 保持标准库优先，避免给本地运行增加额外依赖；
- 保持苹果风视觉和五视图结构；
- 不要覆盖用户的本地进度或提交记录。
