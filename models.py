from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import json
from pathlib import Path
from datetime import datetime
import uuid

class DatabaseConfig(BaseModel):
    dbname: str = "projects_db"
    user: str = "postgres"
    password: str = ""
    host: str = "localhost"
    port: str = "5432"
    table_name: str = "ge_tracker"

class ModelConfig(BaseModel):
    name: str = "openrouter/optimus-alpha"
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)

class UIConfig(BaseModel):
    theme: str = "cyberpunk"
    loading_animation: bool = True
    spinner_type: str = "dots"

class FileProcessingConfig(BaseModel):
    max_file_size_mb: int = Field(default=10, gt=0)
    skip_binary_files: bool = True

class PathsConfig(BaseModel):
    index_dir: str = ".ge_tracker"
    index_filename: str = "ge_tracker.json"

class LoggingConfig(BaseModel):
    level: str = "INFO"
    log_to_file: bool = True
    log_dir: str = "logs"
    log_to_console: bool = False

class OSRSScraperConfig(BaseModel):
    """Configuration for OSRS Grand Exchange scraping"""
    base_url: str = "https://secure.runescape.com/m=itemdb_oldschool/top100"
    list_types: Dict[str, int] = Field(
        default_factory=lambda: {
            "most_traded": 0,
            "price_rises": 2,
            "price_falls": 3
        }
    )
    time_scales: Dict[str, int] = Field(
        default_factory=lambda: {
            "last_7_days": 0,
            "last_30_days": 1,
            "last_90_days": 2,
            "last_180_days": 3
        }
    )
    results_dir: str = "results"
    sleep_time: float = 1.0
    timeout: int = 30000  # Timeout in milliseconds
    max_retries: int = 3
    concurrent_requests: int = 3  # Number of concurrent requests
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    @classmethod
    def from_config_file(cls, config_path: str = None):
        """Load configuration from a JSON file"""
        if config_path is None:
            config_path = Path(__file__).parent / "ge_tracker.json"
            
        try:
            with open(config_path) as f:
                config_data = json.load(f)
                return cls(**config_data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default configuration if file doesn't exist or is invalid
            return cls()

class ItemTradeCount(BaseModel):
    """Model for an individual item's trade count data"""
    name: str
    url: str
    min: str
    max: str
    median: str
    total: str
    item_id: Optional[int] = None
    
    # Additional fields for price rises/falls
    price: Optional[str] = None
    change: Optional[str] = None
    category: Optional[str] = None  # most_traded, price_rises, or price_falls
    
class TradeCountCollection(BaseModel):
    """Collection of trade count data indexed by time period"""
    data: Dict[str, List[ItemTradeCount]]

class AppConfig(BaseModel):
    verbose: bool = False
    use_db: bool = False
    use_index_file_with_db: bool = False
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    file_processing: FileProcessingConfig = Field(default_factory=FileProcessingConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    osrs_scraper: OSRSScraperConfig = Field(default_factory=OSRSScraperConfig)
    
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
    "ModelConfig",
    "UIConfig",
    "FileProcessingConfig",
    "PathsConfig",
    "LoggingConfig",
    "OSRSScraperConfig",
    "ItemTradeCount",
    "TradeCountCollection",
    "AppConfig",
    "AIEvent",
    "ModelEvent",
    "DataEvent",
    "ErrorEvent",
]