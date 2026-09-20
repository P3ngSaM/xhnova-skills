# XHNova Skills

将产品代码和业务资料整理为可导入 [Predictor 公司产品中心](https://www.xhnova.com/prodictor/company-products) 的标准 Markdown，供产品建档、销售交接与推广介绍使用。

当前提供 **company-product-packager**：整理产品名称、简介、目标客户、已实现功能、案例、报价、实施边界、介绍话术、推广建议和资料来源。缺少依据的案例、价格和效果保留为待确认，默认生成「整理中」档案。Skill 不需要 API Key，也不会发送推广消息。

当前版本 **1.1.0** 默认生成业务精简版：先讲客户价值和产品主流程，按需要区分可选扩展；工程证据集中放在来源字段。篇幅建议不改变 Markdown v1 格式或导入上限。需要详细版时可直接向 Agent 说明。

## 直接交给开发 Agent

把下面整段复制给开发 Agent，它会根据自己的环境选择一种安装方式：

```text
Install the Company Product Packager skill. If you're in Claude Code, run `claude plugin marketplace add P3ngSaM/xhnova-skills`, then `claude plugin install company-products@xhnova`. If you're in another agent, run `npx skills add P3ngSaM/xhnova-skills --skill company-product-packager` and select your agent. Use one installation method. You can read the skill directly at https://github.com/P3ngSaM/xhnova-skills/blob/main/skills/company-product-packager/SKILL.md (raw: https://raw.githubusercontent.com/P3ngSaM/xhnova-skills/main/skills/company-product-packager/SKILL.md). Then use this skill on the current project to generate a UTF-8 product-profile.md for Predictor's Company Products import. Include target customers, verified capabilities, introduction and promotion suggestions, implementation constraints, sources, and unknowns. Do not invent cases, prices, or results, and do not include secrets or customer personal data.
```

## 手动运行安装命令

只需选择一种方式，在你要整理的产品项目中执行。

Codex、Cursor 等支持 Agent Skills 的工具：

```sh
npx skills add P3ngSaM/xhnova-skills --skill company-product-packager
```

仅安装到当前项目的 Codex，可明确指定：

```sh
npx skills add P3ngSaM/xhnova-skills --skill company-product-packager --agent codex
```

Claude Code：

```sh
claude plugin marketplace add P3ngSaM/xhnova-skills
claude plugin install company-products@xhnova
```

如果当前会话未出现新 Skill，重新打开会话。Claude Code 插件中的 Skill 名称为 `company-products:company-product-packager`。

## 生成与导入

对开发 Agent 说：

> 请使用最新版 company-product-packager，根据当前项目和已有文档生成业务精简版产品 Markdown。突出客户价值和主流程，按需区分可选扩展；推广介绍能直接讲给客户，保留事实依据和交付边界。已有文件时另存新版本。

Skill 会参照 [格式约定](skills/company-product-packager/references/format.md)，生成供人阅读和系统导入的同一份产品资料。它可使用 Python 3 标准库脚本，无需安装第三方依赖：

```sh
python path/to/company-product-packager/scripts/package_product.py product.json --output product-profile.md
```

Windows 也可用 `py -3`。没有 Python 时，Agent 可按同一格式直接生成 Markdown。脚本默认不覆盖已有文件；确认要更新指定文件后可以加 `--force`。

进入公司产品页，点击「导入 Markdown」，选择文件并核对预览后确认。产品和原始文件一起保存；重复导入同一文件会打开已有档案。审核后将产品改为「在用」即可发起推广。

可阅读 [格式示例](skills/company-product-packager/assets/example.md)。示例产品为虚构演示，不代表客户案例或真实交付。

## 更新

通过 npx 安装：`npx skills update company-product-packager`。

通过 Claude Code 插件安装：先运行 `claude plugin marketplace update xhnova`，再运行 `claude plugin update company-products@xhnova`。

更新后新开 Agent 会话，避免沿用旧会话已加载的 Skill。要求 Agent 在交付时说明所用 Skill 版本；“再生成一版”默认另存新文件，保留之前的产品资料。

安装方式参考：[skills CLI](https://github.com/vercel-labs/skills)、[Claude Code 插件市场](https://code.claude.com/docs/en/plugin-marketplaces)。
