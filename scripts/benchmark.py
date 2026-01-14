"""
scripts/benchmark.py

Benchmark Jailbreak Shield's detection performance
"""

import pandas as pd
from jailbreak_shield import JailbreakShield
from tqdm import tqdm
import time
import os


def calculate_metrics(results_df):
    """Calculate precision, recall, F1"""
    
    tp = len(results_df[
        (results_df["expected_malicious"] == True) & 
        (results_df["detected_malicious"] == True)
    ])
    
    fp = len(results_df[
        (results_df["expected_malicious"] == False) & 
        (results_df["detected_malicious"] == True)
    ])
    
    fn = len(results_df[
        (results_df["expected_malicious"] == True) & 
        (results_df["detected_malicious"] == False)
    ])
    
    tn = len(results_df[
        (results_df["expected_malicious"] == False) & 
        (results_df["detected_malicious"] == False)
    ])
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "accuracy": accuracy,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn
    }


def main():
    """Benchmark Jailbreak Shield"""
    
    if not os.path.exists("data/jailbreaks.csv"):
        print("❌ data/jailbreaks.csv not found. Run collect_jailbreaks.py first.")
        return
    
    df = pd.read_csv("data/jailbreaks.csv")
    
    try:
        shield = JailbreakShield()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    results = []
    latencies = []
    
    print(f"Benchmarking Jailbreak Shield on {len(df)} examples...")
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        start = time.time()
        
        result = shield.defend(row["prompt"])
        
        latency = (time.time() - start) * 1000
        latencies.append(latency)
        
        results.append({
            "prompt": row["prompt"],
            "category": row["category"],
            "expected_malicious": row["malicious"],
            "detected_malicious": result["attack_detected"],
            "risk_score": result["risk_score"],
            "attack_type": result["attack_type"],
            "latency_ms": latency
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv("data/benchmark_results.csv", index=False)
    
    metrics = calculate_metrics(results_df)
    
    print("\n" + "="*50)
    print("🛡️  JAILBREAK SHIELD BENCHMARK RESULTS")
    print("="*50)
    print(f"\n📊 Detection Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']*100:.1f}%")
    print(f"  Precision: {metrics['precision']*100:.1f}%")
    print(f"  Recall:    {metrics['recall']*100:.1f}%")
    print(f"  F1 Score:  {metrics['f1_score']*100:.1f}%")
    
    print(f"\n🎯 Confusion Matrix:")
    print(f"  True Positives:  {metrics['true_positives']}")
    print(f"  False Positives: {metrics['false_positives']} ⚠️")
    print(f"  False Negatives: {metrics['false_negatives']} ⚠️")
    print(f"  True Negatives:  {metrics['true_negatives']}")
    
    print(f"\n⚡ Performance:")
    print(f"  Avg Latency: {sum(latencies)/len(latencies):.1f}ms")
    print(f"  Min Latency: {min(latencies):.1f}ms")
    print(f"  Max Latency: {max(latencies):.1f}ms")
    
    print(f"\n✅ Full results saved to data/benchmark_results.csv")


if __name__ == "__main__":
    main()
