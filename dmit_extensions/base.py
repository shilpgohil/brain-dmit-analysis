from typing import Dict, Any

class DMITExtensionBase:
    """Base class for all DMIT extensions"""
    def analyze(self, features: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement the analyze method") 