"""
scripts/analyze_results.py

Analyze benchmark and test results with visualizations
"""

import pandas as pd
import json
import os


def analyze_benchmark():
    """Analyze benchmark results"""
    
    if not os.path.exists("data/benchmark_results.csv"):
        print("❌ data/benchmark_results.csv not found")
        return
    
    df = pd.read_csv("data/benchmark_results.csv")
    
    print("\n📊 BENCHMARK ANALYSIS")
    print("="*50)
    
    print("\nBy Category:")
    print(df.groupby("category").agg({
        "expected_malicious": "count",
        "detected_malicious": "sum",
        "risk_score": "mean",
        "latency_ms": "mean"
    }).round(2))
    
    print("\nLatency Statistics:")
    print(f"  Mean: {df['latency_ms'].mean():.2f}ms")
    print(f"  Median: {df['latency_ms'].median():.2f}ms")
    print(f"  Min: {df['latency_ms'].min():.2f}ms")
    print(f"  Max: {df['latency_ms'].max():.2f}ms")
    print(f"  Std: {df['latency_ms'].std():.2f}ms")
    
    # Detection accuracy by category
    print("\nDetection Accuracy by Category:")
    for category in df["category"].unique():
        subset = df[df["category"] == category]
        correct = len(subset[subset["expected_malicious"] == subset["detected_malicious"]])
        accuracy = correct / len(subset) * 100
        print(f"  {category}: {accuracy:.1f}%")


def analyze_test_results():
    """Analyze test_claude results"""
    
    if not os.path.exists("data/test_results.csv"):
        print("❌ data/test_results.csv not found")
        return
    
    df = pd.read_csv("data/test_results.csv")
    
    print("\n📊 CLAUDE BASELINE TEST RESULTS")
    print("="*50)
    
    malicious = df[df["expected_malicious"] == True]
    benign = df[df["expected_malicious"] == False]
    
    print(f"\nMalicious prompts:")
    print(f"  Total: {len(malicious)}")
    print(f"  Successfully blocked: {len(malicious[malicious['jailbreak_succeeded'] == False])}")
    print(f"  Jailbroken: {len(malicious[malicious['jailbreak_succeeded'] == True])}")
    if len(malicious) > 0:
        print(f"  Defense rate: {(1 - malicious['jailbreak_succeeded'].sum() / len(malicious)) * 100:.1f}%")
    
    print(f"\nBenign prompts:")
    print(f"  Total: {len(benign)}")
    print(f"  Accepted: {len(benign[benign['jailbreak_succeeded'] == False])}")


def main():
    """Run all analyses"""
    
    print("\n🔍 JAILBREAK SHIELD ANALYSIS REPORT")
    print("="*50)
    
    analyze_benchmark()
    analyze_test_results()
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
