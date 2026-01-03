from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager

# ==================== 数据模型 ====================

class ItemBase(SQLModel):
    title: str = Field(index=True, max_length=100)

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    created_at: datetime

# ==================== 数据库配置 ====================

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # 开发环境可以看到 SQL 日志
)

def create_db_and_tables():
    """创建数据库表"""
    SQLModel.metadata.create_all(engine)

# ==================== FastAPI 应用 ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建表
    create_db_and_tables()
    yield
    # 关闭时的清理工作（如果需要）

app = FastAPI(
    title="待办清单 API",
    description="移动端待办清单后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== CORS 配置 ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 默认端口
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== API 路由 ====================

@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "待办清单 API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/items", response_model=List[ItemRead])
def get_items():
    """获取所有待办项（按创建时间倒序）"""
    with Session(engine) as session:
        statement = select(Item).order_by(Item.created_at.desc())
        items = session.exec(statement).all()
        return items

@app.post("/api/items", response_model=ItemRead)
def create_item(item: ItemCreate):
    """创建新的待办项"""
    if not item.title or not item.title.strip():
        raise HTTPException(status_code=400, detail="标题不能为空")
    
    if len(item.title) > 100:
        raise HTTPException(status_code=400, detail="标题不能超过 100 个字符")
    
    with Session(engine) as session:
        db_item = Item(title=item.title.strip())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

# ==================== 运行说明 ====================
# 运行命令：uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API 文档：http://localhost:8000/docs
