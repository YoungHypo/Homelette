# Homelette Backend

基于Flask+MariaDB的Homelette项目后端API实现

## 快速开始

1. 克隆仓库:
```
git clone https://github.com/YoungHypo/Homelette.git
cd backend
```

2. 使用Docker Compose启动服务:
```
docker-compose up -d
```

服务将在 http://localhost:5001 上运行

## API文档

### 用户认证 API

| 功能 | 方法 | URL | 认证 | 请求参数 | 描述 |
|------|------|-----|------|----------|------|
| 注册 | POST | `/api/auth/register` | 不需要 | ```{"email": "user@example.com", "password": "password123", "first_name": "John", "last_name": "Doe", "major": "Computer Science", "graduation_year": 2024}``` | 创建新用户账户 |
| 登录 | POST | `/api/auth/login` | 不需要 | ```{"email": "user@example.com", "password": "password123"}``` | 验证用户并获取JWT令牌 |

### 用户管理 API

| 功能 | 方法 | URL | 认证 | 请求参数 | 描述 |
|------|------|-----|------|----------|------|
| 获取用户资料 | GET | `/api/users/{user_id}` | JWT令牌 | - | 获取指定用户的个人资料 |
| 更新用户资料 | PUT | `/api/users/{user_id}` | JWT令牌 | 要更新的字段 | 更新当前用户的个人资料 |

### 房源管理 API

| 功能 | 方法 | URL | 认证 | 请求参数 | 描述 |
|------|------|-----|------|----------|------|
| 获取房源列表 | GET | `/api/listings` | 不需要 | `price_min`, `price_max`, `bedrooms`, `city`, `start_date`, `end_date` | 获取所有房源，支持多种筛选条件 |
| 获取房源详情 | GET | `/api/listings/{listing_id}` | 不需要 | - | 获取特定房源的详细信息 |
| 创建房源 | POST | `/api/listings` | JWT令牌 | 房源、房产和地址信息 | 创建新的房源信息 |
| 更新房源 | PUT | `/api/listings/{listing_id}` | JWT令牌 | 要更新的字段 | 更新特定房源的信息 |
| 删除房源 | DELETE | `/api/listings/{listing_id}` | JWT令牌 | - | 删除特定房源 |
| 上传图片 | POST | `/api/listings/upload-image` | JWT令牌 | `image`文件(表单) | 上传房源图片 |

### 房源兴趣 API

| 功能 | 方法 | URL | 认证 | 请求参数 | 描述 |
|------|------|-----|------|----------|------|
| 获取感兴趣的房源 | GET | `/api/users/{user_id}/interests` | JWT令牌 | - | 获取用户标记为感兴趣的所有房源 |
| 添加感兴趣的房源 | POST | `/api/users/{user_id}/interests/{listing_id}` | JWT令牌 | - | 将特定房源标记为感兴趣 |
| 移除感兴趣的房源 | DELETE | `/api/users/{user_id}/interests/{listing_id}` | JWT令牌 | - | 取消对特定房源的兴趣标记 |