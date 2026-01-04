"""
🤖 Robot Chatbot System - Main Application
Version: 1.0
"""

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime

# Memory System import
from app.storage.memory import (
    get_memory_manager,
    initialize_memory_system,
    save_message,
    add_customer_if_not_exists,
    get_statistics,
    set_operator_handoff,
    is_operator_handoff_active,
    MemoryManager
)

# ===========================================
# INITIALIZE MEMORY SYSTEM
# ===========================================

print("\n" + "="*60)
print("🚀 CHATBOT SYSTEM STARTING...")
print("="*60)

memory_manager = MemoryManager()

# ===========================================
# FASTAPI APP
# ===========================================

app = FastAPI(
    title="AI Chatbot API",
    description="Professional Chatbot System with Memory",
    version="3.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# MODELS
# ===========================================

class MessageRequest(BaseModel):
    user_id: str
    message: str
    company_id: str = "default"
    platform: str = "telegram"
    username: str = "Unknown"
    session_id: Optional[str] = None

class MessageResponse(BaseModel):
    message_id: str
    response: str
    timestamp: str
    handoff_required: bool = False

class CustomerInfo(BaseModel):
    user_id: str
    company_id: str
    platform: str
    username: str
    created_at: str
    last_seen: str
    total_messages: int

class StatisticsResponse(BaseModel):
    total_messages: int
    total_customers: int
    total_conversations: int
    operator_handoffs: int
    today_messages: int
    uptime_hours: float
    platform_stats: Dict[str, int]
    timestamp: str

class OperatorHandoffRequest(BaseModel):
    company_id: str
    platform: str
    user_id: str
    status: bool
    operator_name: Optional[str] = None
    reason: Optional[str] = None

# ===========================================
# HEALTH CHECK
# ===========================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Sistem statusunu göstər"""
    stats = get_statistics()
    return f"""
    <html>
        <head>
            <title>🤖 AI Chatbot System</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .card {{ background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
                .stat-item {{ background: white; padding: 15px; border-radius: 5px; }}
                .success {{ color: green; }}
                .warning {{ color: orange; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 AI Chatbot System</h1>
                <p><strong>Status:</strong> <span class="success">✅ ACTIVE</span></p>
                
                <div class="card">
                    <h2>📊 System Statistics</h2>
                    <div class="stats">
                        <div class="stat-item">
                            <h3>Total Messages</h3>
                            <p>{stats.get('total_messages', 0)}</p>
                        </div>
                        <div class="stat-item">
                            <h3>Total Customers</h3>
                            <p>{stats.get('total_customers', 0)}</p>
                        </div>
                        <div class="stat-item">
                            <h3>Operator Handoffs</h3>
                            <p>{stats.get('operator_handoffs', 0)}</p>
                        </div>
                        <div class="stat-item">
                            <h3>Today Messages</h3>
                            <p>{stats.get('today_messages', 0)}</p>
                        </div>
                        <div class="stat-item">
                            <h3>Uptime</h3>
                            <p>{stats.get('uptime_hours', 0):.1f} hours</p>
                        </div>
                        <div class="stat-item">
                            <h3>Last Update</h3>
                            <p>{stats.get('last_update', 'N/A')}</p>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🔗 API Endpoints</h2>
                    <ul>
                        <li><a href="/docs">📚 API Documentation (Swagger)</a></li>
                        <li><a href="/redoc">📖 API Documentation (ReDoc)</a></li>
                        <li><strong>POST</strong> /api/chat - Send message</li>
                        <li><strong>GET</strong> /api/stats - Get statistics</li>
                        <li><strong>POST</strong> /api/handoff - Operator handoff</li>
                        <li><strong>GET</strong> /api/customer/{user_id} - Get customer info</li>
                    </ul>
                </div>
                
                <p>Version: 3.1 | Memory System: ✅ Active</p>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "memory_system": "active",
        "version": "3.1"
    }

# ===========================================
# CHAT ENDPOINTS
# ===========================================

@app.post("/api/chat", response_model=MessageResponse)
async def chat_message(request: MessageRequest, background_tasks: BackgroundTasks):
    """
    Mesaj qəbul et və cavab yarat
    
    Background task olaraq mesajı yadda saxlayır
    """
    # 1. Müştəri yoxdursa əlavə et
    add_customer_if_not_exists(
        company_id=request.company_id,
        platform=request.platform,
        user_id=request.user_id,
        username=request.username
    )
    
    # 2. Operator handoff statusunu yoxla
    handoff_active = is_operator_handoff_active(
        company_id=request.company_id,
        platform=request.platform,
        user_id=request.user_id
    )
    
    # 3. AI cavabını yarat (burada sadə bir rule-based sistem var)
    ai_response = generate_response(request.message, handoff_active)
    
    # 4. Background task olaraq mesajı yadda saxla
    background_tasks.add_task(
        save_message,
        user_id=request.user_id,
        message=request.message,
        response=ai_response,
        company_id=request.company_id,
        platform=request.platform,
        username=request.username
    )
    
    # 5. Profili analiz et və yenilə
    background_tasks.add_task(
        memory_manager.analyze_and_update_profile,
        company_id=request.company_id,
        platform=request.platform,
        user_id=request.user_id,
        text=request.message
    )
    
    return MessageResponse(
        message_id="temp_" + str(int(datetime.now().timestamp())),
        response=ai_response,
        timestamp=datetime.now().isoformat(),
        handoff_required=handoff_active
    )

def generate_response(message: str, handoff_active: bool = False) -> str:
    """AI cavabını generasiya et"""
    message_lower = message.lower()
    
    if handoff_active:
        return "Operator ilə əlaqə saxlanılır. Zəhmət olmasa gözləyin..."
    
    # Sadə rule-based cavablar
    if "salam" in message_lower or "salamlar" in message_lower:
        return "Salam! Sizə necə kömək edə bilərəm?"
    
    elif "necəsən" in message_lower or "nə var nə yox" in message_lower:
        return "Çox sağ olun, yaxşıyam! Siz necəsiniz?"
    
    elif "qiymət" in message_lower or "bahalı" in message_lower or "ucuz" in message_lower:
        return "Məhsullarımızın qiymətləri model və konfiqurasiyadan asılıdır. Hansı məhsulla maraqlanırsınız?"
    
    elif "çatdırılma" in message_lower or "kargo" in message_lower:
        return "Çatdırılma 1-3 iş günü ərzində edilir. Bakı daxili pulsuzdur."
    
    elif "zəmanət" in message_lower or "garantiya" in message_lower:
        return "Bütün məhsullarımız 2 il rəsmi zəmanət altındadır."
    
    elif "saat" in message_lower or "vaxt" in message_lower:
        return "Həftə içi 09:00 - 18:00 saatları arasında xidmət göstəririk."
    
    elif "təşəkkür" in message_lower or "sağ ol" in message_lower:
        return "Rica edirəm! Hər zaman kömək etməyə hazırıq."
    
    else:
        return "Başa düşdüm! Sualınızı operatorlarımıza yönləndirirəm. Tez bir zamanda sizinlə əlaqə saxlayacağıq."

# ===========================================
# STATISTICS ENDPOINTS
# ===========================================

@app.get("/api/stats", response_model=StatisticsResponse)
async def get_system_stats():
    """Sistem statistikasını gətir"""
    stats = get_statistics()
    return StatisticsResponse(**stats)

# ===========================================
# OPERATOR HANDOFF ENDPOINTS
# ===========================================

@app.post("/api/handoff")
async def set_handoff_status(request: OperatorHandoffRequest):
    """Operator handoff statusunu təyin et"""
    set_operator_handoff(
        company_id=request.company_id,
        platform=request.platform,
        user_id=request.user_id,
        status=request.status
    )
    
    return {
        "status": "success",
        "message": f"Operator handoff {'aktiv edildi' if request.status else 'deaktiv edildi'}",
        "user_id": request.user_id,
        "operator": request.operator_name,
        "reason": request.reason,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/handoff/{company_id}/{platform}/{user_id}")
async def get_handoff_status(company_id: str, platform: str, user_id: str):
    """Operator handoff statusunu gətir"""
    status = is_operator_handoff_active(company_id, platform, user_id)
    
    return {
        "user_id": user_id,
        "company_id": company_id,
        "platform": platform,
        "handoff_active": status,
        "timestamp": datetime.now().isoformat()
    }

# ===========================================
# CUSTOMER ENDPOINTS
# ===========================================

@app.get("/api/customer/{user_id}")
async def get_customer_info(user_id: str, company_id: str = "default", platform: str = "telegram"):
    """Müştəri məlumatlarını gətir"""
    customer_key = f"{company_id}_{platform}_{user_id}"
    
    # Fayldan oxu
    customers_data = memory_manager._load_json(memory_manager.CUSTOMERS_FILE, {})
    
    if customer_key in customers_data:
        customer = customers_data[customer_key]
        return {
            "status": "success",
            "customer": customer,
            "timestamp": datetime.now().isoformat()
        }
    
    raise HTTPException(status_code=404, detail="Müştəri tapılmadı")

@app.get("/api/customer/{user_id}/messages")
async def get_customer_messages(user_id: str, limit: int = 20):
    """Müştərinin mesajlarını gətir"""
    messages = memory_manager.get_customer_messages(user_id, limit)
    
    return {
        "status": "success",
        "user_id": user_id,
        "message_count": len(messages),
        "messages": messages,
        "timestamp": datetime.now().isoformat()
    }

# ===========================================
# SYSTEM MAINTENANCE
# ===========================================

@app.post("/api/cleanup")
async def cleanup_data(days: int = 30):
    """Köhnə məlumatları təmizlə"""
    memory_manager.cleanup_old_data(days)
    
    return {
        "status": "success",
        "message": f"Son {days} gündən qabaq məlumatlar təmizləndi",
        "timestamp": datetime.now().isoformat()
    }

# ===========================================
# ERROR HANDLING
# ===========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": f"Daxili server xətası: {str(exc)}",
            "timestamp": datetime.now().isoformat()
        }
    )

# ===========================================
# STARTUP EVENT
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Server başlayanda işə düşür"""
    print("\n" + "="*60)
    print("🚀 FASTAPI SERVER STARTED")
    print("="*60)
    print(f"📊 Memory System: ✅ ACTIVE")
    print(f"🌐 API Available at: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print("="*60)

# ===========================================
# MAIN ENTRY POINT
# ===========================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )