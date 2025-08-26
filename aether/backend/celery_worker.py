#!/usr/bin/env python3

"""
Celery Worker for Aether Agents

Run with: python celery_worker.py
"""

from app.core.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()