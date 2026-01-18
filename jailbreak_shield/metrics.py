"""
jailbreak_shield/metrics.py

Metrics collection for monitoring and observability
Prometheus-compatible output
"""

import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Histogram:
    """Simple histogram for latency tracking"""
    buckets: List[float] = field(default_factory=lambda: [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0])
    counts: Dict[float, int] = field(default_factory=lambda: defaultdict(int))
    sum: float = 0
    count: int = 0
    
    def observe(self, value: float) -> None:
        """Record a value in the histogram"""
        self.sum += value
        self.count += 1
        for bucket in self.buckets:
            if value <= bucket:
                self.counts[bucket] += 1


@dataclass
class Counter:
    """Simple counter metric"""
    value: int = 0
    labels: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    def inc(self, label: Optional[str] = None) -> None:
        """Increment counter"""
        self.value += 1
        if label:
            self.labels[label] += 1


class MetricsCollector:
    """
    Metrics collector for Jailbreak Shield
    
    Tracks:
    - Request count and rate
    - Latency percentiles
    - Detection rates by category
    - Cache hit rates
    - Error rates
    
    Usage:
        metrics = MetricsCollector()
        
        with metrics.timer("layer1"):
            # do work
            pass
        
        metrics.record_detection("role_confusion", blocked=True)
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        
        # Counters
        self.requests_total = Counter()
        self.blocked_total = Counter()
        self.allowed_total = Counter()
        self.errors_total = Counter()
        
        # By category
        self.detections_by_category: Dict[str, int] = defaultdict(int)
        self.blocks_by_category: Dict[str, int] = defaultdict(int)
        
        # Histograms
        self.latency_layer1 = Histogram()
        self.latency_layer2 = Histogram()
        self.latency_total = Histogram()
        
        # Risk score distribution
        self.risk_scores: List[float] = []
        
        # Timing
        self._start_time = time.time()
    
    def record_request(self) -> None:
        """Record a new request"""
        with self._lock:
            self.requests_total.inc()
    
    def record_detection(
        self,
        category: Optional[str],
        blocked: bool,
        risk_score: float
    ) -> None:
        """Record a detection result"""
        with self._lock:
            if blocked:
                self.blocked_total.inc()
                if category:
                    self.blocks_by_category[category] += 1
            else:
                self.allowed_total.inc()
            
            if category:
                self.detections_by_category[category] += 1
            
            self.risk_scores.append(risk_score)
            # Keep only last 10000 scores
            if len(self.risk_scores) > 10000:
                self.risk_scores = self.risk_scores[-10000:]
    
    def record_latency(
        self,
        layer: str,
        duration_seconds: float
    ) -> None:
        """Record latency for a layer"""
        with self._lock:
            if layer == "layer1":
                self.latency_layer1.observe(duration_seconds)
            elif layer == "layer2":
                self.latency_layer2.observe(duration_seconds)
            else:
                self.latency_total.observe(duration_seconds)
    
    def record_error(self, error_type: str) -> None:
        """Record an error"""
        with self._lock:
            self.errors_total.inc(error_type)
    
    def timer(self, layer: str):
        """Context manager for timing operations"""
        return _Timer(self, layer)
    
    def get_stats(self) -> Dict:
        """Get current metrics as dictionary"""
        with self._lock:
            uptime = time.time() - self._start_time
            
            # Calculate averages
            layer1_avg = (
                self.latency_layer1.sum / self.latency_layer1.count
                if self.latency_layer1.count > 0 else 0
            )
            layer2_avg = (
                self.latency_layer2.sum / self.latency_layer2.count
                if self.latency_layer2.count > 0 else 0
            )
            
            # Calculate block rate
            total_processed = self.blocked_total.value + self.allowed_total.value
            block_rate = (
                self.blocked_total.value / total_processed
                if total_processed > 0 else 0
            )
            
            # Risk score stats
            avg_risk = (
                sum(self.risk_scores) / len(self.risk_scores)
                if self.risk_scores else 0
            )
            
            return {
                "uptime_seconds": round(uptime, 2),
                "requests": {
                    "total": self.requests_total.value,
                    "blocked": self.blocked_total.value,
                    "allowed": self.allowed_total.value,
                    "errors": self.errors_total.value,
                    "block_rate": round(block_rate, 4)
                },
                "latency": {
                    "layer1_avg_ms": round(layer1_avg * 1000, 3),
                    "layer2_avg_ms": round(layer2_avg * 1000, 3),
                    "layer1_count": self.latency_layer1.count,
                    "layer2_count": self.latency_layer2.count
                },
                "detections": {
                    "by_category": dict(self.detections_by_category),
                    "blocks_by_category": dict(self.blocks_by_category)
                },
                "risk_scores": {
                    "average": round(avg_risk, 2),
                    "samples": len(self.risk_scores)
                }
            }
    
    def to_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        # Request counters
        lines.append(f"jailbreak_shield_requests_total {self.requests_total.value}")
        lines.append(f"jailbreak_shield_blocked_total {self.blocked_total.value}")
        lines.append(f"jailbreak_shield_allowed_total {self.allowed_total.value}")
        lines.append(f"jailbreak_shield_errors_total {self.errors_total.value}")
        
        # Latency histograms
        for bucket in self.latency_layer1.buckets:
            count = self.latency_layer1.counts.get(bucket, 0)
            lines.append(f'jailbreak_shield_layer1_latency_bucket{{le="{bucket}"}} {count}')
        
        # By category
        for category, count in self.detections_by_category.items():
            lines.append(f'jailbreak_shield_detections{{category="{category}"}} {count}')
        
        return "\n".join(lines)


class _Timer:
    """Context manager for timing operations"""
    
    def __init__(self, collector: MetricsCollector, layer: str):
        self.collector = collector
        self.layer = layer
        self.start = None
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        duration = time.time() - self.start
        self.collector.record_latency(self.layer, duration)


# Global default metrics collector
default_metrics = MetricsCollector()
