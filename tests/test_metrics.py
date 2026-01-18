"""
tests/test_metrics.py

Unit tests for Metrics Collector
"""

import pytest
import time
from jailbreak_shield.metrics import MetricsCollector


class TestMetricsCollector:
    """Tests for MetricsCollector class"""
    
    def test_record_request(self):
        """Test request recording"""
        metrics = MetricsCollector()
        
        metrics.record_request()
        metrics.record_request()
        
        stats = metrics.get_stats()
        assert stats["requests"]["total"] == 2
    
    def test_record_detection(self):
        """Test detection recording"""
        metrics = MetricsCollector()
        
        metrics.record_detection("role_confusion", blocked=True, risk_score=85)
        metrics.record_detection("context_injection", blocked=False, risk_score=30)
        
        stats = metrics.get_stats()
        assert stats["requests"]["blocked"] == 1
        assert stats["requests"]["allowed"] == 1
        assert stats["detections"]["by_category"]["role_confusion"] == 1
    
    def test_record_latency(self):
        """Test latency recording"""
        metrics = MetricsCollector()
        
        metrics.record_latency("layer1", 0.001)
        metrics.record_latency("layer1", 0.002)
        
        stats = metrics.get_stats()
        assert stats["latency"]["layer1_count"] == 2
        assert stats["latency"]["layer1_avg_ms"] > 0
    
    def test_timer_context_manager(self):
        """Test timer context manager"""
        metrics = MetricsCollector()
        
        with metrics.timer("layer1"):
            time.sleep(0.01)
        
        stats = metrics.get_stats()
        assert stats["latency"]["layer1_count"] == 1
        assert stats["latency"]["layer1_avg_ms"] >= 10
    
    def test_block_rate_calculation(self):
        """Test block rate calculation"""
        metrics = MetricsCollector()
        
        metrics.record_detection(None, blocked=True, risk_score=80)
        metrics.record_detection(None, blocked=True, risk_score=90)
        metrics.record_detection(None, blocked=False, risk_score=10)
        metrics.record_detection(None, blocked=False, risk_score=20)
        
        stats = metrics.get_stats()
        assert stats["requests"]["block_rate"] == 0.5
    
    def test_risk_score_average(self):
        """Test average risk score calculation"""
        metrics = MetricsCollector()
        
        metrics.record_detection(None, blocked=False, risk_score=20)
        metrics.record_detection(None, blocked=False, risk_score=40)
        metrics.record_detection(None, blocked=True, risk_score=60)
        
        stats = metrics.get_stats()
        assert stats["risk_scores"]["average"] == 40
    
    def test_prometheus_output(self):
        """Test Prometheus format output"""
        metrics = MetricsCollector()
        
        metrics.record_request()
        metrics.record_detection("role_confusion", blocked=True, risk_score=80)
        
        prometheus = metrics.to_prometheus()
        
        assert "jailbreak_shield_requests_total 1" in prometheus
        assert "jailbreak_shield_blocked_total 1" in prometheus
    
    def test_uptime_tracking(self):
        """Test uptime tracking"""
        metrics = MetricsCollector()
        time.sleep(0.1)
        
        stats = metrics.get_stats()
        assert stats["uptime_seconds"] >= 0.1
