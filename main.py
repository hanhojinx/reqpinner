import argparse
import sys
from pinner.parser import RequirementsParser
from pinner.resolver import VersionResolver
from pinner.client import PyPiClient
from pinner.writer import LockFileWriter

def main():
    parser = argparse.ArgumentParser(description="req-pinner: Pin versions with hashes.")
    parser.add_argument("input", help="Path to input requirements.txt")
    parser.add_argument("--output", "-o", default="requirements.lock", help="Path to output lock file")
    
    args = parser.parse_args()

    print(f"[*] Reading from {args.input}...")
    
    # 1. Parsing
    req_parser = RequirementsParser()
    try:
        requirements = req_parser.parse(args.input)
    except Exception as e:
        print(f"[Fatal] {e}")
        sys.exit(1)

    resolver = VersionResolver()
    client = PyPiClient()
    pinned_results = []

    # 2. Package connecting & Hashing
    print(f"[*] Resolving {len(requirements)} packages...")
    for req in requirements:
        print(f"    Processing {req.name}...", end=" ", flush=True)
        
        # Find the latest compatible version
        latest_version = resolver.resolve_latest_compatible(req)
        
        if latest_version:
            print(f"Found {latest_version}")
            # Fetch hash
            hashes = client.get_hashes_for_version(req.name, latest_version)
            pinned_results.append((req.name, latest_version, hashes))
        else:
            print("Failed to resolve version!")

    # 3. Write on File
    if pinned_results:
        writer = LockFileWriter()
        writer.write(args.output, pinned_results)
    else:
        print("[!] No packages were pinned.")

if __name__ == "__main__":
    main()