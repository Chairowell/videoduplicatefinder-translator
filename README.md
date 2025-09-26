# Video Duplicate Finder Translation Tool

[Engliash](./README.md) | [中文](./README_CN.md) | [日本語](./README_JP.md)

This is a **Python script tool** for translating the `0x90d/videoduplicatefinder` project.

## How to Create a Translation for Your Language

> [!TIP]
> The following operations are performed within **your translation repository**, not in this tool's repository.

### 1. Fork the Original Repository: `https://github.com/0x90d/videoduplicatefinder`

It's recommended that you add your language name to the end of the repository name when forking it, for example: `CN`, `JP`, `FR`, etc. This will make it easier for other users to identify your translated version.

### 2. Clone Your Translation Repository Locally and Enter the Directory

```bash
git clone https://github.com/<your-username>/videoduplicatefinder_<language>.git
cd videoduplicatefinder_<language>
```

### 3. Add This Translation Tool as a Submodule to Your Translation Repository

```bash
git submodule add https://github.com/Chairowell/videoduplicatefinder-translator.git Translator
```

At this point, you will see a directory named **`Translator`** in your translation repository, which is the submodule for this translation tool.

### 4. Commit the Submodule Reference Information in Your Translation Repository

```bash
git add .gitmodules Translator
git commit -m "Add Translator submodule"
git push
```