#!/usr/bin/env python3
"""
Demo Camera Simulator
Simulates Hikvision camera responses for testing without real hardware
"""

from flask import Flask, Response, request
import sys

sim_app = Flask(__name__)

# Simulated vulnerable camera response
VULNERABLE_USERS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<UserList version="1.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
    <User version="1.0">
        <id>1</id>
        <userName>admin</userName>
        <password>YWRtaW4xMjM=</password>
    </User>
</UserList>"""

VULNERABLE_CONFIG_XML = """<?xml version="1.0" encoding="UTF-8"?>
<DeviceInfo version="1.0">
    <deviceName>Test Camera</deviceName>
    <deviceID>12345678</deviceID>
    <model>DS-2CD2142FWD-I</model>
</DeviceInfo>"""

@sim_app.route('/')
def index():
    return "Hikvision Camera Simulator - Demo Mode", 200

@sim_app.route('/Security/users')
def users():
    # Simulate vulnerable endpoint with magic auth
    auth = request.args.get('auth', '')
    if auth == 'YWRtaW46MTEK':  # Magic auth string
        return Response(VULNERABLE_USERS_XML, mimetype='text/xml')
    return "Unauthorized", 401

@sim_app.route('/System/configurationFile')
def config():
    # Simulate vulnerable config endpoint
    auth = request.args.get('auth', '')
    if auth == 'YWRtaW46MTEK':
        return Response(VULNERABLE_CONFIG_XML, mimetype='text/xml')
    return "Unauthorized", 401

@sim_app.route('/onvif-http/snapshot')
def snapshot():
    # Return a simple response (no actual image)
    auth = request.args.get('auth', '')
    if auth == 'YWRtaW46MTEK':
        return "Snapshot data here", 200
    return "Unauthorized", 401

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"🎭 Starting Camera Simulator on http://127.0.0.1:{port}")
    print(f"📝 Test with: http://127.0.0.1:{port}")
    print(f"⚠️  This is a SIMULATOR - not a real camera")
    sim_app.run(host='0.0.0.0', port=port, debug=False)
