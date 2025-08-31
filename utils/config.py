"""
🎓 Klaro Unified Configuration System
====================================

Manages configuration for the integrated Klaro educational app,
combining settings from both quiz-bot and teaching assistant components.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """Configuration for content databases."""
    textbooks_path: str
    book_registry_path: str
    faiss_index_path: str
    knowledge_base_path: str
    pyqs_path: str
    solutions_path: str


@dataclass
class AIConfig:
    """Configuration for AI processing."""
    openai_api_key: str
    openai_model: str
    temperature: float
    max_tokens: int
    cost_optimization: bool


@dataclass
class HandwritingConfig:
    """Configuration for handwriting generation."""
    font_family: str
    font_size: int
    ink_color: str
    paper_texture: bool
    output_dpi: int
    style_variation: bool


@dataclass
class VoiceConfig:
    """Configuration for voice processing."""
    wake_word: str
    language: str
    audio_sample_rate: int
    energy_threshold: int
    pause_threshold: float


@dataclass
class ExportConfig:
    """Configuration for output exports."""
    output_dir: str
    default_formats: list
    include_sources: bool
    pdf_quality: str
    image_quality: int


class KlaroConfig:
    """
    Unified configuration manager for Klaro educational app.
    
    Combines configuration from:
    - Quiz-bot textbook management
    - Klaro AI processing
    - Handwriting generation
    - Voice processing
    - Export systems
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration."""
        # Load environment variables
        load_dotenv()
        
        # Set project root
        self.project_root = Path(__file__).parent.parent
        
        # Load configuration file if provided
        self.config_file = None
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                self.config_file = json.load(f)
        
        # Initialize all configuration sections
        self._init_database_config()
        self._init_ai_config()
        self._init_handwriting_config()
        self._init_voice_config()
        self._init_export_config()
        self._init_app_config()
    
    def _init_database_config(self):
        """Initialize database configuration."""
        base_data_path = self.project_root / "data"
        
        self.database = DatabaseConfig(
            textbooks_path=str(base_data_path / "textbooks"),
            book_registry_path=str(base_data_path / "book_registry.json"),
            faiss_index_path=str(base_data_path / "indexes" / "faiss_index"),
            knowledge_base_path=str(base_data_path / "indexes" / "knowledge_base"),
            pyqs_path=str(base_data_path / "pyqs"),
            solutions_path=str(base_data_path / "solutions")
        )
        
        # Create directories if they don't exist
        for path_attr in ['textbooks_path', 'pyqs_path', 'solutions_path']:
            path = getattr(self.database, path_attr)
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def _init_ai_config(self):
        """Initialize AI configuration."""
        self.ai = AIConfig(
            openai_api_key=os.getenv('OPENAI_API_KEY', ''),
            openai_model=self._get_config_value('ai.model', 'gpt-4'),
            temperature=self._get_config_value('ai.temperature', 0.7),
            max_tokens=self._get_config_value('ai.max_tokens', 2000),
            cost_optimization=self._get_config_value('ai.cost_optimization', True)
        )
    
    def _init_handwriting_config(self):
        """Initialize handwriting configuration."""
        self.handwriting = HandwritingConfig(
            font_family=self._get_config_value('handwriting.font_family', 'Kalam'),
            font_size=self._get_config_value('handwriting.font_size', 14),
            ink_color=self._get_config_value('handwriting.ink_color', '#2E4057'),
            paper_texture=self._get_config_value('handwriting.paper_texture', True),
            output_dpi=self._get_config_value('handwriting.output_dpi', 300),
            style_variation=self._get_config_value('handwriting.style_variation', True)
        )
    
    def _init_voice_config(self):
        """Initialize voice configuration."""
        self.voice = VoiceConfig(
            wake_word=self._get_config_value('voice.wake_word', 'klaro'),
            language=self._get_config_value('voice.language', 'en-US'),
            audio_sample_rate=self._get_config_value('voice.audio_sample_rate', 16000),
            energy_threshold=self._get_config_value('voice.energy_threshold', 4000),
            pause_threshold=self._get_config_value('voice.pause_threshold', 1.0)
        )
    
    def _init_export_config(self):
        """Initialize export configuration."""
        self.export = ExportConfig(
            output_dir=str(self.project_root / "outputs"),
            default_formats=self._get_config_value('export.default_formats', ['png', 'pdf']),
            include_sources=self._get_config_value('export.include_sources', True),
            pdf_quality=self._get_config_value('export.pdf_quality', 'high'),
            image_quality=self._get_config_value('export.image_quality', 95)
        )
        
        # Create output directory
        Path(self.export.output_dir).mkdir(parents=True, exist_ok=True)
    
    def _init_app_config(self):
        """Initialize general app configuration."""
        self.app = {
            'name': 'Klaro',
            'version': '2.0.0',
            'description': 'Unified Educational App with AI Solutions',
            'debug': self._get_config_value('app.debug', False),
            'log_level': self._get_config_value('app.log_level', 'INFO'),
            'session_timeout': self._get_config_value('app.session_timeout', 3600),
            'max_concurrent_users': self._get_config_value('app.max_concurrent_users', 100)
        }
        
        # Web app specific settings
        self.web = {
            'host': self._get_config_value('web.host', 'localhost'),
            'port': self._get_config_value('web.port', 8501),
            'theme': self._get_config_value('web.theme', 'light'),
            'page_title': 'Klaro - Educational AI Assistant',
            'page_icon': '🎓'
        }
    
    def _get_config_value(self, key: str, default: Any) -> Any:
        """Get configuration value with fallback to default."""
        if not self.config_file:
            return default
        
        # Navigate nested keys (e.g., 'ai.model' -> config_file['ai']['model'])
        value = self.config_file
        for k in key.split('.'):
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate configuration settings."""
        validation_results = {}
        
        # Check OpenAI API key
        validation_results['openai_api_key'] = bool(self.ai.openai_api_key)
        
        # Check required directories exist
        validation_results['textbooks_directory'] = Path(self.database.textbooks_path).exists()
        validation_results['output_directory'] = Path(self.export.output_dir).exists()
        
        # Check book registry exists
        validation_results['book_registry'] = Path(self.database.book_registry_path).exists()
        
        return validation_results
    
    def create_default_config_file(self, output_path: str):
        """Create a default configuration file."""
        default_config = {
            "ai": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
                "cost_optimization": True
            },
            "handwriting": {
                "font_family": "Kalam",
                "font_size": 14,
                "ink_color": "#2E4057",
                "paper_texture": True,
                "output_dpi": 300,
                "style_variation": True
            },
            "voice": {
                "wake_word": "klaro",
                "language": "en-US",
                "audio_sample_rate": 16000,
                "energy_threshold": 4000,
                "pause_threshold": 1.0
            },
            "export": {
                "default_formats": ["png", "pdf"],
                "include_sources": True,
                "pdf_quality": "high",
                "image_quality": 95
            },
            "app": {
                "debug": False,
                "log_level": "INFO",
                "session_timeout": 3600,
                "max_concurrent_users": 100
            },
            "web": {
                "host": "localhost",
                "port": 8501,
                "theme": "light"
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✅ Default configuration saved to: {output_path}")
    
    @property
    def OPENAI_API_KEY(self) -> str:
        """Get OpenAI API key."""
        return self.ai.openai_api_key
    
    @property
    def OPENAI_MODEL(self) -> str:
        """Get OpenAI model name."""
        return self.ai.openai_model
    
    @property
    def TEXTBOOKS_PATH(self) -> str:
        """Get textbooks directory path."""
        return self.database.textbooks_path
    
    @property
    def BOOK_REGISTRY_PATH(self) -> str:
        """Get book registry file path."""
        return self.database.book_registry_path
    
    @property
    def FAISS_INDEX_PATH(self) -> str:
        """Get FAISS index directory path."""
        return self.database.faiss_index_path
    
    @property
    def KNOWLEDGE_BASE_PATH(self) -> str:
        """Get knowledge base directory path."""
        return self.database.knowledge_base_path
    
    @property
    def OUTPUT_DIR(self) -> str:
        """Get output directory path."""
        return self.export.output_dir
    
    @property
    def HANDWRITING_CONFIG(self) -> Dict[str, Any]:
        """Get handwriting configuration as dictionary."""
        return {
            'font_family': self.handwriting.font_family,
            'font_size': self.handwriting.font_size,
            'ink_color': self.handwriting.ink_color,
            'paper_texture': self.handwriting.paper_texture,
            'output_dpi': self.handwriting.output_dpi,
            'style_variation': self.handwriting.style_variation
        }


# Global config instance
config = None

def get_config(config_path: Optional[str] = None) -> KlaroConfig:
    """Get global configuration instance."""
    global config
    if config is None:
        config = KlaroConfig(config_path)
    return config


# Convenience properties for quick access
def get_openai_key() -> str:
    return get_config().OPENAI_API_KEY

def get_textbooks_path() -> str:
    return get_config().TEXTBOOKS_PATH

def get_output_dir() -> str:
    return get_config().OUTPUT_DIR
