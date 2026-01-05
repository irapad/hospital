#!/usr/bin/env python3
"""
Camera Security Management Application
Integrates with HIKScript for Hikvision camera security testing
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os
import json
import threading
from pathlib import Path

# Add hikscript-lib to path (not needed in production - library is self-contained)
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hikscript-lib'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///camera_security.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False, unique=True)
    port = db.Column(db.Integer, default=80)
    location = db.Column(db.String(200))
    is_vulnerable = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    credentials = db.Column(db.Text)  # JSON stored as text
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='unknown')  # unknown, vulnerable, secure, checking

    scans = db.relationship('ScanResult', backref='camera', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'port': self.port,
            'location': self.location,
            'is_vulnerable': self.is_vulnerable,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'credentials': json.loads(self.credentials) if self.credentials else None,
            'notes': self.notes,
            'status': self.status
        }

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    scan_type = db.Column(db.String(50))  # vulnerability_check, rtsp_test, snapshot, etc.
    result = db.Column(db.Text)  # JSON stored as text
    success = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'scan_date': self.scan_date.isoformat(),
            'scan_type': self.scan_type,
            'result': json.loads(self.result) if self.result else None,
            'success': self.success
        }

class ShodanScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    query = db.Column(db.String(200))
    location_filter = db.Column(db.String(200))
    results_count = db.Column(db.Integer, default=0)
    results_file = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'scan_date': self.scan_date.isoformat(),
            'query': self.query,
            'location_filter': self.location_filter,
            'results_count': self.results_count,
            'results_file': self.results_file
        }

# Routes
@app.route('/')
def index():
    """Dashboard home page"""
    stats = {
        'total_cameras': Camera.query.count(),
        'vulnerable_cameras': Camera.query.filter_by(is_vulnerable=True).count(),
        'secure_cameras': Camera.query.filter_by(status='secure').count(),
        'unknown_cameras': Camera.query.filter_by(status='unknown').count(),
        'recent_scans': ScanResult.query.order_by(ScanResult.scan_date.desc()).limit(10).all()
    }
    return render_template('index.html', stats=stats)

@app.route('/cameras')
def cameras():
    """List all cameras"""
    cameras = Camera.query.all()
    return render_template('cameras.html', cameras=cameras)

@app.route('/cameras/add', methods=['GET', 'POST'])
def add_camera():
    """Add a new camera"""
    if request.method == 'POST':
        ip_address = request.form.get('ip_address')
        port = request.form.get('port', 80, type=int)
        location = request.form.get('location', '')
        notes = request.form.get('notes', '')

        if Camera.query.filter_by(ip_address=ip_address).first():
            flash('Camera with this IP already exists!', 'error')
            return redirect(url_for('add_camera'))

        camera = Camera(
            ip_address=ip_address,
            port=port,
            location=location,
            notes=notes
        )
        db.session.add(camera)
        db.session.commit()

        flash('Camera added successfully!', 'success')
        return redirect(url_for('cameras'))

    return render_template('add_camera.html')

@app.route('/cameras/<int:camera_id>')
def camera_detail(camera_id):
    """Camera details page"""
    camera = Camera.query.get_or_404(camera_id)
    return render_template('camera_detail.html', camera=camera)

@app.route('/cameras/<int:camera_id>/delete', methods=['POST'])
def delete_camera(camera_id):
    """Delete a camera"""
    camera = Camera.query.get_or_404(camera_id)
    db.session.delete(camera)
    db.session.commit()
    flash('Camera deleted successfully!', 'success')
    return redirect(url_for('cameras'))

@app.route('/api/cameras/<int:camera_id>/check', methods=['POST'])
def check_camera(camera_id):
    """Check camera vulnerability"""
    camera = Camera.query.get_or_404(camera_id)

    # Update status to checking
    camera.status = 'checking'
    db.session.commit()

    # Run vulnerability check in background thread
    def run_check():
        from hikscript_wrapper import check_single_camera
        result = check_single_camera(camera.ip_address, camera.port)

        camera.is_vulnerable = result.get('vulnerable', False)
        camera.status = 'vulnerable' if result.get('vulnerable') else 'secure'
        camera.last_checked = datetime.utcnow()

        if result.get('credentials'):
            camera.credentials = json.dumps(result['credentials'])

        # Save scan result
        scan = ScanResult(
            camera_id=camera.id,
            scan_type='vulnerability_check',
            result=json.dumps(result),
            success=True
        )
        db.session.add(scan)
        db.session.commit()

    thread = threading.Thread(target=run_check)
    thread.start()

    return jsonify({'status': 'checking', 'message': 'Vulnerability check started'})

@app.route('/api/cameras')
def api_cameras():
    """API endpoint for cameras list"""
    cameras = Camera.query.all()
    return jsonify([camera.to_dict() for camera in cameras])

@app.route('/scan')
def scan():
    """Shodan scan page"""
    scans = ShodanScan.query.order_by(ShodanScan.scan_date.desc()).all()
    return render_template('scan.html', scans=scans)

@app.route('/api/scan/shodan', methods=['POST'])
def scan_shodan():
    """Run Shodan scan"""
    api_key = request.json.get('api_key')
    city = request.json.get('city', '')
    country = request.json.get('country', '')
    limit = request.json.get('limit', 100)

    if not api_key:
        return jsonify({'error': 'Shodan API key is required'}), 400

    def run_scan():
        from hikscript_wrapper import run_shodan_scan
        results = run_shodan_scan(api_key, city, country, limit)

        # Save scan record
        scan = ShodanScan(
            query='App-webs+200+OK',
            location_filter=f"{city},{country}" if city or country else "Global",
            results_count=len(results),
            results_file=results.get('file_path', '')
        )
        db.session.add(scan)

        # Add cameras from results
        for target in results.get('targets', []):
            ip = target.split(':')[0]
            port = int(target.split(':')[1]) if ':' in target else 80

            if not Camera.query.filter_by(ip_address=ip).first():
                camera = Camera(
                    ip_address=ip,
                    port=port,
                    location=results.get('location', 'Unknown')
                )
                db.session.add(camera)

        db.session.commit()

    thread = threading.Thread(target=run_scan)
    thread.start()

    return jsonify({'status': 'scanning', 'message': 'Shodan scan started'})

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    # Use debug mode only in development
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
