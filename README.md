# 移动端待办清单应用

一个基于 uni-app + FastAPI 的全栈待办清单应用，支持 H5、小程序和 App 多端运行。

## 项目结构

```
app_new/
├── mobile/          # uni-app 前端项目
│   ├── src/
│   │   ├── api/     # API 接口封装
│   │   ├── pages/   # 页面
│   │   ├── config.ts
│   │   └── ...
│   └── package.json
├── server/          # FastAPI 后端项目
│   ├── main.py
│   ├── requirements.txt
│   └── app.db      # SQLite 数据库（运行后自动生成）
└── README.md
```

## 技术栈

### 前端
- **框架**: uni-app (Vue3 + Vite + TypeScript)
- **UI 组件**: @dcloudio/uni-ui
- **支持平台**: H5、微信小程序、App

### 后端
- **框架**: FastAPI
- **ORM**: SQLModel
- **数据库**: SQLite
- **API 文档**: Swagger (自动生成)

## 环境要求

- **Node.js**: 18+ (推荐 18.x 或 20.x)
- **Python**: 3.11+
- **pnpm/npm**: 最新版本

## 快速开始

### 1. 启动后端服务

```bash
# 进入后端目录
cd server

# 安装 Python 依赖
pip3 install -r requirements.txt

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务启动后：
- API 地址: http://localhost:8000
- Swagger 文档: http://localhost:8000/docs
- 数据库文件会自动创建在 `server/app.db`

### 2. 启动前端项目

#### H5 开发模式

```bash
# 进入前端目录
cd mobile

# 安装依赖（首次运行）
npm install

# 启动 H5 开发服务器
npm run dev:h5
```

访问 http://localhost:5173 即可看到应用。

#### 微信小程序开发模式

```bash
# 在 mobile 目录下运行
npm run dev:mp-weixin
```

然后：
1. 打开微信开发者工具
2. 导入项目，选择 `mobile/dist/dev/mp-weixin` 目录
3. 即可预览和调试小程序

#### App 开发模式

```bash
# 在 mobile 目录下运行
npm run dev:app
```

使用 HBuilderX 打开项目进行 App 调试。

## 功能说明

### 已实现功能

1. **列表页** (`/pages/items/list`)
   - 展示所有待办项（按创建时间倒序）
   - 支持下拉刷新
   - 空状态提示
   - 跳转到新增页面

2. **新增页** (`/pages/items/create`)
   - 输入待办标题（最多 100 字符）
   - 表单校验
   - 提交后返回列表并自动刷新

### API 接口

- `GET /api/items` - 获取待办列表
- `POST /api/items` - 创建新待办项
  - 请求体: `{ "title": "待办标题" }`

## 配置说明

### 修改 API 地址

如果后端服务不在 `localhost:8000`，可以修改前端配置：

编辑 `mobile/src/config.ts`:

```typescript
export const API_BASE_URL = 'http://your-server-ip:8000'
```

### 数据持久化

- 数据存储在 SQLite 数据库文件 `server/app.db` 中
- 重启服务后数据不会丢失
- 如需清空数据，删除 `app.db` 文件即可

## 开发说明

### 前端目录结构

```
mobile/src/
├── api/
│   ├── http.ts       # 请求封装
│   └── items.ts      # 待办项 API
├── pages/
│   └── items/
│       ├── list.vue    # 列表页
│       └── create.vue  # 新增页
├── config.ts         # 配置文件
├── pages.json        # 页面配置
└── main.ts           # 入口文件
```

### 后端 API 设计

使用 FastAPI + SQLModel 实现 RESTful API：

- 自动生成 OpenAPI 文档
- 类型安全的数据模型
- 自动请求验证
- CORS 跨域支持

## 常见问题

### 1. 前端请求失败

- 确保后端服务已启动
- 检查 `mobile/src/config.ts` 中的 API 地址是否正确
- 查看浏览器控制台的网络请求错误信息

### 2. 小程序无法请求

- 小程序需要配置合法域名（开发阶段可在微信开发者工具中关闭域名校验）
- 修改 `config.ts` 中的 API 地址为服务器实际地址

### 3. npm 安装依赖失败

- 尝试使用国内镜像源：`npm config set registry https://registry.npmmirror.com`
- 或使用 pnpm：`pnpm install`

## 后续扩展

可以继续添加的功能：

- [ ] 待办项完成/未完成状态切换
- [ ] 删除待办项
- [ ] 编辑待办项
- [ ] 待办项分类
- [ ] 用户认证
- [ ] 数据同步

## License

MIT


## 自动部署

### H5 版本自动部署

本项目已配置 GitHub Actions，每次推送到 `main` 分支会自动部署 H5 版本到 GitHub Pages。

**部署地址**：https://sea-t.github.io/app_new/

**设置步骤**：
1. 进入仓库设置：Settings → Pages
2. Source 选择：`GitHub Actions`
3. 保存后自动部署

详细说明请查看：[GitHub Pages 部署指南](docs/GITHUB_PAGES_SETUP.md)

### Android App 打包

提供三种打包方式：

1. **HBuilderX 云打包**（推荐新手）- 简单快速
2. **本地离线打包**（推荐进阶）- 完全控制
3. **GitHub Actions 自动打包**（未来支持）- 需要额外配置

详细说明请查看：[Android 打包指南](docs/ANDROID_BUILD_GUIDE.md)

## 项目文档

- [README.md](README.md) - 项目说明和快速开始
- [GitHub Pages 部署指南](docs/GITHUB_PAGES_SETUP.md) - H5 自动部署配置
- [Android 打包指南](docs/ANDROID_BUILD_GUIDE.md) - App 打包完整教程

## 在线演示

- **H5 版本**：https://sea-t.github.io/app_new/ （部署后可访问）
- **API 文档**：http://localhost:8000/docs （本地运行后可访问）
