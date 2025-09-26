# Video Duplicate Finder 翻译工具

[Engliash](./README.md) | [中文](./README_CN.md) | [日本語](./README_JP.md)

这是一个用于翻译 `0x90d/videoduplicatefinder` 项目的 Python 脚本工具

## 如何为你的语言创建翻译版？
> [!TIP]
> 以下的操作都是在你的汉化仓库内完成的操作，并非本工具仓库

### 1. Fork 原始仓库 `https://github.com/0x90d/videoduplicatefinder`
建议你在 Fork 原始仓库时在名称尾部加入你的语言名称，例如：`CN`、`JP`、`FR` 等，这样方便其他用户识别你的翻译版

### 2. 克隆你的翻译仓库到本地，并进入目录
```bash
git clone https://github.com/<your-username>/videoduplicatefinder_<language>.git
cd videoduplicatefinder_<language>
```

### 3. 将本翻译工具作为子模块添加到你的翻译仓库中
```bash
git submodule add https://github.com/Chairowell/videoduplicatefinder-translator.git Translator
```
此时，你会在你的翻译仓库中看到一个名为 `Translator` 的目录，这就是本翻译工具的子模块

### 4. 在翻译仓库中提交子模块引用信息
```bash
git add .gitmodules Translator
git commit -m "Add Translator submodule"
git push
```