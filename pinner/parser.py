from typing import List
from packaging.requirements import Requirement
import os

class RequirementsParser:
    def parse(self, file_path: str) -> List[Requirement]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")

        requirements = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('-'):
                    continue
                
                try:
                    req = Requirement(line)
                    requirements.append(req)
                except Exception as e:
                    print(f"[Warn] Could not parse line '{line}': {e}")
        
        return requirements