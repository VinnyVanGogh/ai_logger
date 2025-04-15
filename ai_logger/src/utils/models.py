from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class DatabaseConfig(BaseModel):
    """Configuration for database connection"""
    use_db: bool = False
    dbname: str = "ai_logger_db"
    user: str = "postgres"
    password: str = ""
    host: str = "localhost"
    port: str = "5432"
    table_name: str = "ai_logs"

class LoggingConfig(BaseModel):
    """Configuration for logging settings"""
    level: str = "INFO"
    log_to_file: bool = True
    log_dir: str = "logs"
    log_to_console: bool = False

class AppConfig(BaseModel):
    """Main application configuration"""
    verbose: bool = False
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
class AIEvent(BaseModel):
    """Base model for all AI-related events"""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    event_type: str
    component: str
    file_name: Optional[str] = None
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    details: Dict[Any, Any] = {}
    
class ModelEvent(AIEvent):
    """Events specific to model execution"""
    model_name: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    latency_ms: Optional[float] = None
    
class DataEvent(AIEvent):
    """Events related to data processing"""
    data_source: str
    record_count: Optional[int] = None
    
class ErrorEvent(AIEvent):
    """Error events that occur during processing"""
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    severity: str = "ERROR"
    
__all__ = [
    "DatabaseConfig",
    "LoggingConfig",
    "AppConfig",
    "AIEvent",
    "ModelEvent",
    "DataEvent",
    "ErrorEvent",
]