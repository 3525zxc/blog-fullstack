# 林间漫记 · 全栈个人博客

前端（HTML/CSS/原生 JS）+ Flask + SQLAlchemy + MySQL 的个人博客系统。
在原有高保真原型基础上接入真实后端：文章、评论、留言、点赞收藏、站点设置全部落库。

## 目录结构

```
blog-fullstack/
├── server/                  # Flask 后端
│   ├── app.py               # 应用工厂 + 入口（gunicorn server.app:app）
│   ├── config.py            # 配置（环境变量 / .env）
│   ├── extensions.py        # db / cors 实例
│   ├── models.py            # ORM 模型（文章/评论/留言/分类/设置/管理员/点赞收藏）
│   ├── seed.py              # 演示数据（首次启动自动写入）
│   └── routes/              # REST API（auth/posts/comments/guests/categories/settings/admin/bootstrap）
├── web/                     # 前端静态站点（Flask 同源托管）
│   ├── index.html 等 13 个页面
│   └── assets/（css + js，data.js 为 API 客户端）
├── Dockerfile               # suga.app 等容器平台构建用
├── Procfile                 # 兼容 Procfile 平台
├── requirements.txt
└── .env.example             # 环境变量模板（复制为 .env 填写）
```

## 一、本地运行

```bash
# 1. 安装依赖（Python 3.10+）
pip install -r requirements.txt

# 2. 配置数据库连接（默认连本机 MySQL 的 linblog 库）
cp .env.example .env
# 编辑 .env 填入你的 MySQL 账号密码

# 3. 启动（首次启动自动建表并写入演示数据）
python server/app.py
# 打开 http://127.0.0.1:5000
```

- 默认管理员：**admin / admin123**（登录后请尽快修改，见下文）
- 前端页面与 API 同源，无需单独起前端服务
- 数据库为空时自动建表 + 写入 8 篇演示文章、评论、留言

## 二、数据库配置（MySQL）

连接优先级：**环境变量 `DATABASE_URL` > `.env` 文件 > 默认本机 MySQL**。

```bash
# 方式一：整串连接串（推荐，sqlpub 控制台可直接拼）
DATABASE_URL=mysql+pymysql://用户名:密码@主机:3306/库名?charset=utf8mb4

# 方式二：离散变量（config.py 自动拼装，密码会做 URL 编码）
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DB=linblog
```

字符集固定 `utf8mb4`；连接池已按小规格配置（pool_size 3 / max_overflow 2 / pool_recycle 280s），
兼容 sqlpub 免费版 30 连接上限。生产环境请把 `SECRET_KEY` 改成随机长字符串。

### 修改管理员密码

```bash
python -m server.seed  # 仅建表播种，不改密码
# 改密码：进入项目根目录执行
python -c "import sys; sys.path.insert(0,'.'); from server.app import app; from server.models import Admin; from server.extensions import db
ctx=app.app_context(); ctx.push()
a=Admin.query.filter_by(username='admin').first(); a.set_password('新密码'); db.session.commit(); print('done')"
```

## 三、部署到 suga.app（suga.app）

suga.app 是容器型 PaaS，支持从 GitHub 自动构建 Docker 镜像。

**1. 推送代码到 GitHub**

```bash
cd blog-fullstack
git init && git add . && git commit -m "init"
git remote add origin https://github.com/你的账号/你的仓库.git
git push -u origin main
```
（`.gitignore` 已排除 `.env`、`data/`、`__pycache__` 等，不会泄露本地配置）

**2. 在 suga.app 创建服务**

1. 注册/登录 suga.app，进入控制台
2. 添加服务 → **Container** → Image 选择 **Build from GitHub**
3. 安装 Suga GitHub App 并授权你的仓库，选择仓库和分支（main）
4. Build Method 选择 **Dockerfile**（项目根目录已提供，路径保持默认）
5. **Config → Public Networking → Port 填 `8000`**（Dockerfile 中 gunicorn 监听的端口，读取平台注入的 `PORT`，默认 8000）
6. **Config → Environment Variables** 添加：

   | 变量 | 值 |
   |---|---|
   | `DATABASE_URL` | `mysql+pymysql://sqlpub用户:sqlpub密码@主机:端口/库名?charset=utf8mb4` |
   | `SECRET_KEY` | 随机长字符串（如 `openssl rand -hex 32` 的输出） |
   | `TOKEN_TTL` | 可选，登录有效期秒数，默认 7 天 |

7. 点击 Apply，suga 自动构建镜像并滚动发布，完成后获得 `https://xxx.suga.app` 域名（自动 TLS）

**3. 验证**

- 打开域名 → 首页正常显示 8 篇演示文章
- 访问 `/admin/login.html` → admin / admin123 登录 → 仪表盘有数据
- 发布一篇文章 → 前台首页立即出现
- 健康检查端点：`/healthz` 返回 `{"ok":true}`

> 注意：免费版内存 256MB，本应用 2 workers 足够；数据在 MySQL 中，容器重建不丢数据。
> 若构建日志报端口/绑定问题，确认应用监听 `0.0.0.0`（Dockerfile 已配置）。

## 四、接入 sqlpub 免费 MySQL（sqlpub.com）

**1. 申请实例**

1. 打开 https://sqlpub.com 注册账号
2. 控制台 → 共享实例 → 创建：填写数据库名称、数据库用户，版本选默认（8.4），资源类型选**免费版**（500MB / 30 连接 / 36000 次请求每小时）
3. 创建成功后保存连接信息：**公网连接地址（主机:端口）、数据库名称、账号、密码**（密码只显示一次，务必保存；泄露到公开环境会被永久锁定）

**2. 拼装连接串**

```
mysql+pymysql://数据库账号:数据库密码@公网地址:端口/数据库名称?charset=utf8mb4
```
示例（地址端口以控制台实际为准）：
```
mysql+pymysql://mydb_user:Abt3xyz@mysql2.sqlpub.com:3307/mydb?charset=utf8mb4
```
密码含特殊字符时无需手动编码，config.py 会用 `quote_plus` 自动处理（仅方式二离散变量需要，方式一请手工 URL 编码）。

**3. 两种用法**

- **本地开发**：把连接串写进 `.env` 的 `DATABASE_URL`，`python server/app.py` 启动，首次启动自动在 sqlpub 上建表播种
- **线上部署**：把同一串填到 suga.app 的 Environment Variables（见上）

**4. 验证建表**

用 sqlpub 的网页工作台（或 Navicat）执行 `SHOW TABLES;`，应看到
`posts / comments / guests / categories / subs / settings / admins / post_likes / post_collects / comment_likes / guest_likes` 共 11 张表。

## 五、API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/bootstrap` | 首屏全量数据（设置/分类/文章/评论/留言/点赞态） |
| GET | `/api/posts?cat=&main=&tag=&q=&status=` | 文章列表（访客仅见已发布） |
| GET/POST | `/api/posts/<id>` · `/api/posts` | 详情 / 新建（需登录） |
| PUT/PATCH/DELETE | `/api/posts/<id>` · `/status` | 改/改状态/删（需登录） |
| POST | `/api/posts/<id>/view` `/like` `/collect` | 浏览/点赞/收藏 |
| GET/POST | `/api/posts/<id>/comments` · `/api/comments` | 评论列表 / 发表 |
| POST | `/api/comments/<id>/like` | 评论点赞 |
| PATCH/DELETE | `/api/comments/<id>/status` · `/api/comments/<id>` | 审核/删除（需登录） |
| GET/POST | `/api/guests` · `/api/guests/<id>/like` | 留言板 |
| GET | `/api/categories` | 分类（含文章数） |
| POST/DELETE | `/api/categories/subs` | 二级分类增删（需登录） |
| GET/PUT | `/api/settings` | 站点设置 |
| POST | `/api/auth/login` | 登录，返回 token |
| GET/POST | `/api/admin/export` · `/import` · `/reset` | 导出/导入/重置（需登录） |

管理接口通过请求头 `Authorization: Bearer <token>` 鉴权；点赞/收藏通过 `X-Client-Id` 头标识浏览器。

## 六、常见问题

- **`upstream connect error ... Connection refused`（suga 域名打不开）**：
  边缘代理连不上容器，说明**应用没在监听端口**。按此顺序排查：
  1. 看 suga 的 Logs——如果有 `Cannot add or update a child row: a foreign key constraint fails`，
     是 MySQL 外键校验导致的启动崩溃（本版本已修复：种子数据按依赖顺序分组插入；
     历史版本需升级到当前代码）
  2. 如果有 `Can't connect to MySQL server`，是 `MYSQL_*` 环境变量配错了
  3. 如果日志有 `Running on 0.0.0.0:8000`/`Listening at`，应用是好的，
     检查 **Public Networking 端口是否为 8000**
  4. 部署是否还在 Building/Pending 状态，等几分钟再试
- **启动报 `Can't connect to MySQL server`**：检查 `.env`/环境变量的账号密码与主机端口，确认 sqlpub 实例状态正常、本机防火墙放行。本地可先跑 `python -m server.check_db` 自检。
- **本地自检数据库**：`python -m server.check_db`（读取 .env，直连测试，成功/失败都有明确提示）
- **健康检查**：`/healthz` 会同时探测数据库，返回 `{"ok":true,"db":"up"}` 为正常；`"db":"down"` 说明库连不上
- **中文乱码**：连接串必须带 `charset=utf8mb4`（`.env` 方式自动带上）；数据库/表/列默认已按 utf8mb4 创建。
- **想清空重来**：后台「站点设置 → 重置为演示数据」，或直接 TRUNCATE 所有表后重启（空库自动重新播种）。
- **修改管理员密码**：见上文「修改管理员密码」命令。
- **前后端分离部署**：后端 API 已开 CORS（`CORS_ORIGINS` 可限制来源）；把 `web/` 单独静态托管，前端 `data.js` 中 `apiBase()` 改为后端地址即可。
