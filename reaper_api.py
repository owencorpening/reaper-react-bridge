#!/usr/bin/env python3
"""REAPER API - ExtState communication"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import configparser

logger = logging.getLogger(__name__)

class ReaperAPI:
    def __init__(self):
        self.extstate_file = self._find_extstate_file()
        self._cache: Dict[str, Dict[str, float]] = {}
        logger.info(f"ReaperAPI initialized: {self.extstate_file}")
    
    def _find_extstate_file(self) -> Optional[Path]:
        possible_paths = [
            Path.home() / ".config" / "REAPER" / "reaper-extstate.ini",
            Path.home() / "Library" / "Application Support" / "REAPER" / "reaper-extstate.ini",
            Path(os.getenv("APPDATA", "")) / "REAPER" / "reaper-extstate.ini",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        logger.warning("REAPER ExtState not found")
        return possible_paths[0]
    
    def is_connected(self) -> bool:
        if not self.extstate_file:
            return False
        try:
            if not self.extstate_file.exists():
                self.extstate_file.parent.mkdir(parents=True, exist_ok=True)
                self.extstate_file.touch()
            return os.access(self.extstate_file, os.W_OK)
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False
    
    def set_parameter(self, effect: str, param: str, value: float) -> bool:
        try:
            config = configparser.ConfigParser()
            if self.extstate_file and self.extstate_file.exists():
                config.read(self.extstate_file)
            
            if effect not in config:
                config.add_section(effect)
            
            config.set(effect, param, str(value))
            
            with open(self.extstate_file, 'w') as f:
                config.write(f)
            
            if effect not in self._cache:
                self._cache[effect] = {}
            self._cache[effect][param] = value
            
            logger.debug(f"Set [{effect}] {param} = {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set {effect}.{param}: {e}")
            return False
    
    def get_parameter(self, effect: str, param: str, default: float = 0.0) -> float:
        try:
            if effect in self._cache and param in self._cache[effect]:
                return self._cache[effect][param]
            
            config = configparser.ConfigParser()
            if self.extstate_file and self.extstate_file.exists():
                config.read(self.extstate_file)
            
            if effect in config and param in config[effect]:
                value = float(config[effect][param])
                if effect not in self._cache:
                    self._cache[effect] = {}
                self._cache[effect][param] = value
                return value
            
            return default
        except Exception as e:
            logger.error(f"Failed to get {effect}.{param}: {e}")
            return default
