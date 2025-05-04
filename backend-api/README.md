# Homelette Backend

Homelette是一个针对大学生短期租房需求的移动应用平台，该平台旨在为租房双方缺乏便捷的沟通渠道。

Homelette后端基于**Flask+MariaDB**实现

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

## 系统架构

```
客户端 (React Native)
    ↓ ↑
    HTTP/WebSocket
    ↓ ↑
Flask   ─→   Redis    
    ↓ ↑                
MariaDB
```

## API文档

### 用户认证 API

| 功能 | 方法 | URL | 参数 |
|------|------|-----|------|
| 注册 | POST | `/api/auth/register` | email, password, first_name, last_name, major, graduation_year |
| 登录 | POST | `/api/auth/login` | email, password |

### 用户管理 API

| 功能 | 方法 | URL | 参数 |
|------|------|-----|------|
| 获取用户资料 | GET | `/api/users/{user_id}` | 路径参数: user_id |
| 更新用户资料 | PUT | `/api/users/{user_id}` | 路径参数: user_id<br>请求体: 要更新的字段 |

### 房源管理 API

| 功能 | 方法 | URL | 参数 |
|------|------|-----|------|
| 获取房源列表 | GET | `/api/listings` | price_min, price_max, bedrooms, city, start_date, end_date |
| 获取房源详情 | GET | `/api/listings/{listing_id}` | listing_id |
| 创建房源 | POST | `/api/listings` | 请求体: address, property, listing 信息 |
| 更新房源 | PUT | `/api/listings/{listing_id}` | listing_id<br>请求体: 要更新的字段 |
| 删除房源 | DELETE | `/api/listings/{listing_id}` | listing_id |
| 上传图片 | POST | `/api/listings/upload-image` | image 文件 |

### 房源兴趣 API

| 功能 | 方法 | URL | 参数 |
|------|------|-----|------|
| 获取感兴趣的房源 | GET | `/api/users/{user_id}/interests` | user_id |
| 添加感兴趣的房源 | POST | `/api/users/{user_id}/interests/{listing_id}` | user_id, listing_id |
| 移除感兴趣的房源 | DELETE | `/api/users/{user_id}/interests/{listing_id}` | user_id, listing_id |