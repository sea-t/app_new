# Android App 打包指南

本文档介绍如何将 uni-app 项目打包成 Android APK 安装包。

## 方式一：使用 HBuilderX 云打包（推荐新手）

### 1. 准备工作

1. 下载并安装 [HBuilderX](https://www.dcloud.io/hbuilderx.html)
2. 注册 [DCloud 开发者账号](https://dev.dcloud.net.cn/)

### 2. 获取 AppID

1. 登录 [DCloud 开发者中心](https://dev.dcloud.net.cn/)
2. 创建应用，获取 AppID
3. 将 AppID 填写到 `mobile/src/manifest.json` 中的 `appid` 字段

### 3. 配置应用信息

编辑 `mobile/src/manifest.json`：

```json
{
  "name": "待办清单",
  "appid": "__UNI__XXXXXXX",  // 填写你的 AppID
  "description": "移动端待办清单应用",
  "versionName": "1.0.0",
  "versionCode": "100"
}
```

### 4. 使用 HBuilderX 打包

1. 用 HBuilderX 打开 `mobile` 目录
2. 点击菜单：发行 → 原生 App-云打包
3. 选择 Android 平台
4. 配置打包参数：
   - 使用 DCloud 公用证书（测试用）
   - 或上传自己的证书（正式发布）
5. 点击打包，等待完成
6. 下载生成的 APK 文件

### 优点
- ✅ 简单快速，无需配置环境
- ✅ 自动处理依赖和配置
- ✅ 适合快速测试

### 缺点
- ❌ 需要网络连接
- ❌ 每天有打包次数限制（免费版）
- ❌ 无法完全自定义原生代码

---

## 方式二：本地离线打包（推荐进阶）

### 1. 环境准备

#### 必需软件
- [Android Studio](https://developer.android.com/studio)
- JDK 11 或更高版本
- Node.js 18+

#### 下载 uni-app 离线 SDK

```bash
# 下载 Android 离线 SDK
wget https://native-res.dcloud.net.cn/uni-app-sdk/uni-app-sdk-android-release.zip
unzip uni-app-sdk-android-release.zip
```

### 2. 构建前端资源

```bash
cd mobile
npm install
npm run build:h5  # 构建 H5 资源包
```

### 3. 配置 Android 项目

1. 用 Android Studio 打开离线 SDK 中的示例项目
2. 将构建的前端资源复制到 Android 项目的 `assets` 目录
3. 修改 `dcloud_control.xml` 配置应用信息

### 4. 生成签名证书

```bash
# 生成 keystore 文件
keytool -genkey -v -keystore app.keystore -alias app -keyalg RSA -keysize 2048 -validity 10000

# 按提示输入信息
# 密码、姓名、组织等
```

### 5. 配置签名

在 Android Studio 中配置签名：
1. Build → Generate Signed Bundle / APK
2. 选择 APK
3. 选择或创建 keystore
4. 输入密码和别名
5. 选择 release 构建类型
6. 点击 Finish

### 6. 构建 APK

```bash
cd android-project
./gradlew assembleRelease
```

生成的 APK 位于：`app/build/outputs/apk/release/app-release.apk`

### 优点
- ✅ 完全控制打包过程
- ✅ 可以自定义原生代码
- ✅ 无打包次数限制
- ✅ 可以集成到 CI/CD

### 缺点
- ❌ 配置复杂
- ❌ 需要学习 Android 开发知识
- ❌ 环境配置耗时

---

## 方式三：GitHub Actions 自动打包（未来支持）

目前项目已配置 H5 自动部署，Android 自动打包需要：

### 准备工作

1. **生成签名证书**（参考方式二第4步）

2. **将证书转为 Base64**
   ```bash
   base64 app.keystore > keystore.base64
   ```

3. **配置 GitHub Secrets**
   
   在仓库设置中添加以下 Secrets：
   - `ANDROID_KEYSTORE_BASE64`: keystore 的 base64 编码
   - `KEYSTORE_PASSWORD`: keystore 密码
   - `KEY_ALIAS`: 密钥别名
   - `KEY_PASSWORD`: 密钥密码

4. **获取 DCloud AppID**
   
   在 `manifest.json` 中配置 AppID

5. **创建 GitHub Actions 工作流**（待实现）

### 注意事项
- 需要完整的离线 SDK 集成
- 需要配置原生 Android 项目结构
- 首次配置较为复杂

---

## 签名证书说明

### 测试证书 vs 正式证书

#### 测试证书
- 使用 DCloud 提供的公用证书
- 仅用于开发测试
- 无法发布到应用商店
- 所有使用公用证书的应用签名相同

#### 正式证书
- 自己生成的 keystore 文件
- 用于正式发布
- 每个应用唯一
- **必须妥善保管，丢失无法找回**

### 生成正式证书

```bash
keytool -genkey -v \
  -keystore app.keystore \
  -alias app \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# 参数说明：
# -keystore: 证书文件名
# -alias: 密钥别名
# -keyalg: 加密算法
# -keysize: 密钥长度
# -validity: 有效期（天）
```

### 查看证书信息

```bash
keytool -list -v -keystore app.keystore
```

---

## API 地址配置

打包 App 时需要修改 API 地址为实际的服务器地址。

编辑 `mobile/src/config.ts`：

```typescript
// 开发环境
export const API_BASE_URL = 'http://localhost:8000'

// 生产环境（打包 App 时使用）
// export const API_BASE_URL = 'https://your-server.com'
```

建议使用环境变量：

```typescript
export const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'
```

---

## 常见问题

### 1. 打包后白屏

**原因**：资源路径配置错误

**解决**：
- 检查 `manifest.json` 配置
- 确保前端资源正确放置在 `assets` 目录
- 检查 `dcloud_control.xml` 配置

### 2. 网络请求失败

**原因**：
- API 地址配置错误
- 服务器未启动
- 跨域问题

**解决**：
- 修改 `config.ts` 中的 API 地址
- 确保服务器可访问
- 配置后端 CORS

### 3. 签名错误

**原因**：证书配置错误

**解决**：
- 检查 keystore 路径
- 确认密码和别名正确
- 重新生成证书

### 4. 构建失败

**原因**：依赖或环境问题

**解决**：
- 更新 Android Studio 和 SDK
- 清理项目：`./gradlew clean`
- 检查 Gradle 配置

---

## 发布到应用商店

### 准备材料

1. **APK 文件**（已签名）
2. **应用图标**（多种尺寸）
3. **应用截图**（至少 3 张）
4. **应用描述**
5. **隐私政策**
6. **软件著作权**（部分应用商店需要）

### 主要应用商店

- **华为应用市场**：https://developer.huawei.com/
- **小米应用商店**：https://dev.mi.com/
- **OPPO 软件商店**：https://open.oppomobile.com/
- **vivo 应用商店**：https://dev.vivo.com.cn/
- **应用宝（腾讯）**：https://open.tencent.com/

### 发布流程

1. 注册开发者账号
2. 实名认证
3. 创建应用
4. 上传 APK
5. 填写应用信息
6. 提交审核
7. 等待审核通过
8. 发布上线

---

## 推荐方案

### 开发测试阶段
→ **方式一：HBuilderX 云打包**
- 快速验证功能
- 无需复杂配置

### 正式发布阶段
→ **方式二：本地离线打包**
- 使用自己的签名证书
- 完全控制打包过程
- 可以发布到应用商店

### 持续集成阶段
→ **方式三：GitHub Actions**（需要额外配置）
- 自动化构建
- 版本管理
- 团队协作

---

## 下一步

1. ✅ 先使用 H5 版本测试功能（已自动部署）
2. 📱 功能确认后，使用 HBuilderX 云打包测试 App
3. 🔐 生成正式签名证书
4. 📦 使用离线打包生成正式 APK
5. 🚀 发布到应用商店

有任何问题，请参考：
- [uni-app 官方文档](https://uniapp.dcloud.net.cn/)
- [Android 开发文档](https://developer.android.com/)
