import requests
from typing import Dict, Optional, List

class PyPiClient:
    BASE_URL = "https://pypi.org/pypi"

    def get_package_metadata(self, package_name: str) -> Optional[Dict]:
        """
        Fetch package metadata from PyPI
        """
        url = f"{self.BASE_URL}/{package_name}/json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"[Warn] Package not found: {package_name}")
                return None
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            print(f"[Error] Network error for {package_name}: {e}")
            return None

    def get_hashes_for_version(self, package_name: str, version: str) -> List[str]:
        """
        Return SHA256 of an artifact of specific version(wheel, tar.gz)
        """
        url = f"{self.BASE_URL}/{package_name}/{version}/json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # format SHA256 hash
                hashes = []
                for url_info in data.get('urls', []):
                    digest = url_info.get('digests', {}).get('sha256')
                    if digest:
                        hashes.append(digest)
                return hashes
        except Exception:
            pass
        return []