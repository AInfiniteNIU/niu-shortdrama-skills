<div align="center">

<img src="https://raw.githubusercontent.com/AInfiniteNIU/niu-brand/main/banner/ainfiniteniu-banner-1280.jpg" alt="AInfiniteNIU" width="640">

# 短剧创作者中心 skill 系统

**真人剧与 AI 漫剧两套，50 个 skill，从入驻投稿到写剧本、诊断退稿一站解决**

[**使用手册**](https://ainfiniteniu.github.io/niu-shortdrama-skills/) · [下载 zip](https://github.com/AInfiniteNIU/niu-shortdrama-skills/releases/latest) · [提建议](https://github.com/AInfiniteNIU/niu-shortdrama-skills/issues/new/choose)

</div>

> 非官方项目，与红果短剧、抖音及其关联公司无关。规则整理自红果短剧创作者中心帮助中心的公开文档（37 篇，截至 2026-11-17），金额、比例、日期以平台站内公告和签署的合同为准。

## 它是什么

一套给 AI 助手用的 skill（技能包），面向在红果短剧创作者中心工作的编剧、导演、演员与版权方。装上之后，你直接用中文提问或提需求，AI 会按平台规则回答、诊断或写稿：

| 你说 | 它做 |
| --- | --- |
| 首次投稿要交多少集？ | 按规则卡回答，并注明出处 |
| 帮我看看这份投稿包能不能投 | 逐项诊断，指出第几集第几行、违反哪条规则 |
| 帮我拆 30 集分集大纲 | 按平台体量与格式写，写完交给诊断 skill 自检 |
| 漫剧审核又被驳了，驳回原因在哪看 | 讲清楚平台上怎么操作 |

## 四层结构

| 层 | 做什么 | 真人剧 | AI 漫剧 |
| --- | --- | --- | --- |
| 第一层 路由 | 回答平台规则，把需求分发给下层；内置 157 条规则卡与 20 条冲突裁决 | `zhenren-hub` | `manju-hub` |
| 第二层 办事 | 入驻认证、投稿签约、撮合、上传审核、结算数据，只讲怎么操作 | 6 个 `zr-*` | 6 个 `mj-*` |
| 第三层 诊断 | 只诊断不写稿：投稿包、单集、开篇、节奏、红线、退稿、上线、资方视角、可生成性 | 8 个 `zr-dx-*` | 7 个 `mj-dx-*` |
| 第四层 创作 | 选题、主线、人物、大纲、开篇、分集、台词、改编、长线、改稿续写 | 10 个 `zr-cr-*` | 11 个 `mj-cr-*` |

完整的 skill 目录、典型工作流和规则速查见[使用手册](https://ainfiniteniu.github.io/niu-shortdrama-skills/)。

## 安装

**Claude Code**

```text
/plugin marketplace add AInfiniteNIU/niu-shortdrama-skills
/plugin install zhenren@ainfiniteniu-shortdrama
/plugin install manju@ainfiniteniu-shortdrama
```

只做真人剧装 `zhenren`，只做漫剧装 `manju`，两种都做就都装。

**其他支持 skill 的 AI 工具**：在 [Releases](https://github.com/AInfiniteNIU/niu-shortdrama-skills/releases/latest) 下载 zip，或克隆本仓库，把 `skills/` 下需要的文件夹整个放进你的 skills 目录。每个 skill 都内置了它要用到的规则卡，可以单独使用；同时装上对应的 hub，提问不准时它能自动转到正确的 skill。

## 两条约定

- **先说品类**：没说品类的短剧请求，默认按真人剧处理。做漫剧时，第一句话带上「漫剧」「AI剧」或「动态漫」最稳。
- **先诊断，再改稿**：第三层只出问题清单，不动稿；确认后再交第四层改。

## 格式机检脚本

部分 skill 内置 `scripts/check_script.py`，可以单独运行（Python 3，无需安装依赖）：

```bash
python3 skills/zr-dx-episode/scripts/check_script.py 剧本.txt --mode zr      # 真人剧：单集 600-800 字，上限 1200
python3 skills/zr-dx-episode/scripts/check_script.py 剧本.txt --mode qianbu  # 千部计划
python3 skills/zr-dx-episode/scripts/check_script.py 剧本.txt --mode mj      # AI 漫剧
python3 skills/zr-dx-episode/scripts/check_script.py 剧本.txt --mode zr --title 剧名
```

它检查集标题与字数、付费卡点等非剧本标注、AI 高频书面词、红线提示词和剧名规范，输出「必改 / 建议改 / 人工判断」三级清单。

## 触发测试

`tests/` 里有 112 条问法和两轮盲测结果：把 50 个 skill 的名称与描述交给没参与设计的独立模型，v1.4 正例命中 100/100、负例正确 12/12。改了 skill 的描述后，可以拿这套问法重跑。

## 时效

平台规则会变。规则卡注明了来源文档和状态（有效、已截止、已暂停、待核）。距 2026-11-17 超过 90 天，或平台公告改版时，请以站内最新文档为准；欢迎在 [Issues](https://github.com/AInfiniteNIU/niu-shortdrama-skills/issues) 报告已经过时的规则。

## 许可

本仓库内容采用 [CC BY-NC-SA 4.0](LICENSE) 许可：可以免费使用、修改和分享，但需要署名 AInfiniteNIU，不能用于商业用途，修改后的版本要用同样的许可发布。商业使用请联系作者获取授权。平台规则本身归平台所有，本仓库只做整理与引用。

AInfiniteNIU 名称与 ∞ 标识不在许可范围内，见 [niu-brand](https://github.com/AInfiniteNIU/niu-brand)。

<div align="center"><sub>AInfiniteNIU ∞ · 由编剧、互动影游创作者 INFINITE 制作 · <a href="https://github.com/AInfiniteNIU">更多工具</a></sub></div>
