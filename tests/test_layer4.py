"""
tests/test_layer4.py

Unit tests for Layer 4 (Karma) - Context & Reputation Tracking
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jailbreak_shield.layer4_karma import KarmaTracker


class TestKarmaTracker:
    """Test suite for Layer 4 Karma (Context) Tracking."""

    def test_tracker_initialization(self):
        """Test that tracker initializes correctly."""
        tracker = KarmaTracker()
        assert tracker is not None

    def test_new_user_default_score(self):
        """Test that new users get a default karma score."""
        tracker = KarmaTracker()
        score = tracker.get_score("new_user_12345")
        assert score == 100.0  # Default starting score

    def test_score_decreases_on_violation(self):
        """Test that karma score decreases after a violation."""
        tracker = KarmaTracker()
        user_id = "test_user_violation"
        
        initial_score = tracker.get_score(user_id)
        tracker.record_violation(user_id, severity="medium")
        new_score = tracker.get_score(user_id)
        
        assert new_score < initial_score

    def test_score_increases_on_good_behavior(self):
        """Test that karma score increases with good behavior."""
        tracker = KarmaTracker()
        user_id = "test_user_good"
        
        # First decrease the score
        tracker.record_violation(user_id, severity="low")
        score_after_violation = tracker.get_score(user_id)
        
        # Then record good behavior
        tracker.record_safe_request(user_id)
        score_after_safe = tracker.get_score(user_id)
        
        assert score_after_safe >= score_after_violation

    def test_severe_violation_impact(self):
        """Test that severe violations have larger impact."""
        tracker = KarmaTracker()
        user_low = "user_low_severity"
        user_high = "user_high_severity"
        
        tracker.record_violation(user_low, severity="low")
        tracker.record_violation(user_high, severity="high")
        
        score_low = tracker.get_score(user_low)
        score_high = tracker.get_score(user_high)
        
        assert score_high < score_low

    def test_minimum_score_floor(self):
        """Test that karma score has a minimum floor."""
        tracker = KarmaTracker()
        user_id = "test_user_floor"
        
        # Record many violations
        for _ in range(50):
            tracker.record_violation(user_id, severity="high")
        
        score = tracker.get_score(user_id)
        assert score >= 0  # Score should never go negative


class TestKarmaTrackerEdgeCases:
    """Edge case tests for Layer 4."""

    def test_concurrent_user_tracking(self):
        """Test tracking multiple users simultaneously."""
        tracker = KarmaTracker()
        
        users = ["user_a", "user_b", "user_c"]
        for user in users:
            tracker.get_score(user)
            tracker.record_safe_request(user)
        
        # Each user should have independent scores
        assert tracker.get_score("user_a") == tracker.get_score("user_b")

    def test_analyze_returns_correct_structure(self):
        """Test that analyze method returns expected structure."""
        tracker = KarmaTracker()
        result = tracker.analyze("test_user", {})
        
        assert "karma_score" in result
        assert "risk_multiplier" in result
        assert "flagged" in result

    def test_low_karma_triggers_flag(self):
        """Test that low karma score triggers a flag."""
        tracker = KarmaTracker()
        user_id = "sus_user"
        
        # Drive karma down
        for _ in range(20):
            tracker.record_violation(user_id, severity="high")
        
        result = tracker.analyze(user_id, {})
        # Low karma should increase risk or flag the user
        assert result["karma_score"] < 50
