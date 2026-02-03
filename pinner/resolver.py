from typing import List, Optional
from packaging.version import parse as parse_version
from packaging.requirements import Requirement
from .client import PyPiClient

class VersionResolver:
    def __init__(self):
        self.client = PyPiClient()

    def resolve_latest_compatible(self, req: Requirement) -> Optional[str]:
        """
        Find the latest version that satisfies the requirement constraints(e.g. >=1.0)
        """
        metadata = self.client.get_package_metadata(req.name)
        if not metadata:
            return None

        # Fetch all released versions on PyPI
        releases = metadata.get('releases', {}).keys()
        
        valid_versions = []
        for v_str in releases:
            try:
                version = parse_version(v_str)
                # Exclude prerelease normally, include if stated else
                if not version.is_prerelease:
                    valid_versions.append(version)
            except Exception:
                continue
        
        # Version lining
        valid_versions.sort(reverse=True)

        # Latest version search corresponding to the specifier condition
        for version in valid_versions:
            # Allow all versions if req.specifier is empty
            if req.specifier.contains(version, prereleases=False):
                return str(version)
        
        return None