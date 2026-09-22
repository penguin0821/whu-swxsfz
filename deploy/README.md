# 部署

线上是 **GitHub Pages**，从仓库**根目录**读取 `index.html`。所以构建产物必须落在仓库根的 `index.html`（`reinject6.py` 已经这样输出）。

预览地址形如：`https://<owner>.github.io/<repo>/`

## 前置

- 装好并登录 GitHub CLI：`gh auth login`（选 github.com、HTTPS、按提示完成设备码授权）。
- 仓库已开启 Pages：Settings → Pages → Source 选 `Deploy from a branch`，branch 选 `main`、目录选 `/ (root)`。
  用 API 开启：
  ```bash
  gh api repos/OWNER/REPO/pages -X POST -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
  ```

> 免费版 GitHub Pages 要求仓库**公开**。公开意味着内容在正式上线前就可被公网检索，请知悉后再决定。

## 两条更新路径

### 1. 常规：git push（环境正常时首选）

```bash
python3 reinject6.py          # 重新构建根目录 index.html
git add -A && git commit -m "site: update"
git push origin main          # 约 30s 后 Pages 自动重建
```

### 2. API 直传（git push 不可用时的兜底）

某些受管环境会拦截 git 的 https remote-helper（`git push` 报 `remote helper 'https' aborted session`）。这时走 GitHub API，不依赖 git 传输层：

- **只更新线上页面**（最常用，改完内容重新构建后）：
  ```bash
  ./deploy/deploy_index.sh index.html
  ```
  走 Contents API，只需 `gh` 已登录。

- **全量同步整个工作树**（首次上传、或大量文件变动）：
  ```bash
  python3 deploy/publish_all.py OWNER/REPO --branch main --root . --message "sync"
  ```
  走 Git Data API：逐个建 blob → 建一棵 tree（工作目录的精确快照）→ 建 commit → 前移分支指针。一次提交完成，且**绕开 git push**。大文件用 stdin 传，避开命令行长度上限。

  注意：`publish_all.py` 生成的 tree 是**精确快照**，本地没有的路径会在远端被删除，让仓库与本目录完全一致。它按 `.gitignore` 的设计跳过 `.git/`、`*.otf`、`.DS_Store` 等。

## 验证发布成功

```bash
# 等 Pages 重建完成
gh api repos/OWNER/REPO/pages -q .status        # 直到返回 built
```

再从**外网视角**打开预览 URL，确认标题、语言门、各 section 正常渲染。

## 迁移到正式托管

正式上线（校方域名 + ICP 备案 + 境内 CDN）的考量见 `../docs/CMS与演进路线.md` 第 3 节。GitHub Pages 适合当前的预览与内部查看阶段。
