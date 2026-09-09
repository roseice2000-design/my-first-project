# 房源预订网站

一个现代的、功能完整的房源预订网站，用于直接向客人展示和销售您的房源。

## 功能特点

✨ **主要功能**
- 🏠 展示房源信息（卧室、浴室、价格、设施等）
- 📅 日期选择和可用性检查
- 💰 实时价格计算
- 📝 在线预订表单
- ✅ 预订确认和编号
- 🔍 预订查询功能
- 📱 完全响应式设计
- 🎨 现代化UI界面

## 快速开始

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 生产环境运行
```bash
npm start
```

访问 http://localhost:3000 查看网站

## 项目结构

```
my-first-project/
├── server.js              # Express后端服务器
├── package.json           # 项目配置和依赖
├── public/
│   └── index.html        # 前端网站页面
└── README.md             # 本文件
```

## API端点

### 房源管理
- `GET /api/properties` - 获取所有房源
- `GET /api/properties/:id` - 获取单个房源详情

### 预订管理
- `POST /api/bookings` - 创建新预订
- `GET /api/bookings` - 获取所有预订（管理面板）
- `GET /api/bookings/:id` - 获取预订详情
- `DELETE /api/bookings/:id` - 取消预订

## 定制化

### 添加您的房源

编辑 `server.js` 中的 `properties` 数组，添加您的房源信息：

```javascript
{
  id: '3',
  name: '您的房源名称',
  location: '位置',
  price: 1000,
  currency: 'CNY',
  pricePerNight: 100,
  rating: 4.8,
  reviews: 50,
  description: '房源描述',
  bedrooms: 1,
  bathrooms: 1,
  guests: 2,
  amenities: ['WiFi', '空调', '厨房'],
  availableDates: {
    from: '2026-09-10',
    to: '2026-12-31'
  }
}
```

### 自定义样式

编辑 `public/index.html` 中的 CSS 部分，调整颜色、字体和布局

### 修改品牌信息

在 `public/index.html` 中修改：
- 网站标题和描述
- 联系信息
- 关于页面内容
- Logo和图片

## 部署

### 部署到云服务（Heroku示例）

```bash
# 创建Heroku应用
heroku create your-app-name

# 部署
git push heroku main

# 查看日志
heroku logs --tail
```

### 部署到其他平台

支持任何支持Node.js的平台：
- Vercel
- Railway
- Render
- DigitalOcean
- AWS
- 阿里云
- 腾讯云

## 数据持久化

当前使用内存存储。要使用数据库（推荐用于生产环境）：

**使用SQLite（推荐简单部署）**
```bash
npm install better-sqlite3
```

**使用MongoDB**
```bash
npm install mongodb
```

## 安全建议

- 🔒 添加用户认证
- 🛡️ 使用HTTPS
- 💳 集成支付系统（Stripe、支付宝等）
- 📧 设置真实的邮件通知
- 🔑 保护敏感配置（使用环境变量）
- ✅ 验证预订请求
- 📊 添加日志和监控

## 支付集成

要添加实际支付功能，集成以下服务：
- Stripe
- 支付宝
- 微信支付
- PayPal

## 邮件通知

配置邮件服务发送确认邮件：
- SendGrid
- Mailgun
- 腾讯云邮件
- 阿里云邮件

## 常见问题

**Q: 如何修改价格？**
A: 在 `server.js` 中编辑房源的 `pricePerNight` 属性

**Q: 如何添加图片？**
A: 在 `public/images` 目录添加图片，更新房源的 `image` 属性

**Q: 预订数据如何保存？**
A: 当前使用内存存储，重启后清空。要持久化数据，需要集成数据库

**Q: 如何发送邮件？**
A: 集成邮件服务（如SendGrid），在预订成功时发送确认邮件

## 后续功能建议

- [ ] 用户注册和登录
- [ ] 预订历史记录
- [ ] 评价和评论系统
- [ ] 搜索和过滤增强
- [ ] 日历视图
- [ ] 短期租赁和长期租赁选项
- [ ] 多语言支持
- [ ] SEO优化
- [ ] 支付集成
- [ ] 邮件通知
- [ ] SMS通知
- [ ] 数据库持久化

## 许可证

MIT

## 支持

如有问题，请联系：booking@property.com
