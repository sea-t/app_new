# GitHub Pages 自动部署设置

本项目已配置 GitHub Actions 自动部署 H5 版本到 GitHub Pages。

## 启用 GitHub Pages

### 1. 进入仓库设置

访问：https://github.com/sea-t/app_new/settings/pages

### 2. 配置 Pages 源

在 "Build and deployment" 部分：
- **Source**: 选择 `GitHub Actions`

### 3. 保存设置

配置完成后，每次推送到 `main` 分支都会自动触发部署。

## 访问地址

部署成功后，应用将可以通过以下地址访问：

**https://sea-t.github.io/app_new/**

## 工作流说明

### 触发条件

- 推送到 `main` 分支
- 手动触发（在 Actions 页面）

### 构建步骤

1. 检出代码
2. 安装 Node.js 18
3. 安装前端依赖
4. 构建 H5 版本
5. 部署到 GitHub Pages

### 查看构建状态

访问：https://github.com/sea-t/app_new/actions

可以看到每次构建的详细日志。

## 自定义域名（可选）

### 1. 准备域名

购买并配置域名的 DNS 记录：

```
类型: CNAME
主机记录: www (或其他子域名)
记录值: sea-t.github.io
```

### 2. 配置 GitHub Pages

在仓库设置的 Pages 页面：
- 在 "Custom domain" 输入你的域名
- 勾选 "Enforce HTTPS"

### 3. 添加 CNAME 文件

在项目中添加 `mobile/public/CNAME` 文件：

```
your-domain.com
```

重新部署后即可通过自定义域名访问。

## API 地址配置

### 开发环境

本地开发时使用 `localhost`：

```typescript
// mobile/src/config.ts
export const API_BASE_URL = 'http://localhost:8000'
```

### 生产环境

部署到 GitHub Pages 后，需要将后端也部署到公网服务器，然后修改配置：

```typescript
// mobile/src/config.ts
export const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-server.com'  // 生产环境 API 地址
  : 'http://localhost:8000'         // 开发环境 API 地址
```

## 后端部署建议

### 方案 1：使用云服务器

1. 购买云服务器（阿里云、腾讯云等）
2. 部署 FastAPI 应用
3. 配置 Nginx 反向代理
4. 配置 HTTPS 证书

### 方案 2：使用 Serverless

- **Vercel**：支持 Python，免费额度
- **Railway**：支持 Python，简单易用
- **Render**：免费套餐，自动部署

### 方案 3：使用 PaaS 平台

- **Heroku**（付费）
- **DigitalOcean App Platform**
- **AWS Elastic Beanstalk**

## 环境变量配置

### 使用 Vite 环境变量

创建 `.env.production` 文件：

```env
VITE_API_BASE_URL=https://your-api-server.com
```

修改 `config.ts`：

```typescript
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

### 在 GitHub Actions 中配置

编辑 `.github/workflows/deploy-h5.yml`：

```yaml
- name: Build H5
  run: |
    cd mobile
    npm run build:h5
  env:
    VITE_API_BASE_URL: ${{ secrets.API_BASE_URL }}
```

在仓库设置中添加 Secret：`API_BASE_URL`

## 常见问题

### 1. 部署后页面 404

**原因**：GitHub Pages 未正确配置

**解决**：
1. 检查 Settings → Pages 是否选择了 "GitHub Actions"
2. 查看 Actions 日志是否有错误
3. 确认 `vite.config.ts` 中的 `base` 路径正确

### 2. 资源加载失败

**原因**：base 路径配置错误

**解决**：
确保 `vite.config.ts` 中：
```typescript
base: process.env.NODE_ENV === 'production' ? '/app_new/' : '/'
```

### 3. API 请求失败

**原因**：
- 后端未部署
- CORS 配置错误
- API 地址错误

**解决**：
1. 部署后端到公网服务器
2. 配置后端 CORS 允许 GitHub Pages 域名
3. 更新前端 API 地址配置

### 4. 构建失败

**原因**：依赖安装或构建错误

**解决**：
1. 查看 Actions 日志
2. 本地测试 `npm run build:h5`
3. 检查 `package.json` 和依赖版本

## 监控和分析

### 添加 Google Analytics（可选）

在 `mobile/index.html` 中添加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 添加百度统计（可选）

```html
<!-- 百度统计 -->
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?YOUR_SITE_ID";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
```

## 性能优化

### 1. 启用 Gzip 压缩

GitHub Pages 默认启用，无需配置。

### 2. 代码分割

Vite 默认已配置代码分割。

### 3. 图片优化

- 使用 WebP 格式
- 压缩图片大小
- 使用 CDN

### 4. 缓存策略

在 `vite.config.ts` 中配置：

```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'vendor': ['vue'],
        'uni': ['@dcloudio/uni-app']
      }
    }
  }
}
```

## 下一步

1. ✅ 启用 GitHub Pages（按照上述步骤）
2. ⏳ 等待自动部署完成
3. 🌐 访问 https://sea-t.github.io/app_new/
4. 🚀 部署后端 API 到公网
5. 🔧 配置生产环境 API 地址

---

**提示**：首次推送后，GitHub Actions 会自动运行，大约 2-3 分钟后即可访问部署的应用。
