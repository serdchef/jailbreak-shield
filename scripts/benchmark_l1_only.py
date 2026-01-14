"""
scripts/benchmark_l1_only.py

Benchmark Jailbreak Shield Layer 1 only (no API key required)
"""

import pandas as pd
from jailbreak_shield import JailbreakShield
from tqdm import tqdm
import time


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
    """Benchmark Jailbreak Shield Layer 1"""
    
    df = pd.read_csv("data/jailbreaks.csv")
    
    # Initialize Shield with Layer 2 disabled
    shield = JailbreakShield(layer2_enabled=False)
    
    results = []
    latencies = []
    
    print(f"🛡️  Benchmarking Layer 1 on {len(df)} examples...")
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        start = time.time()
        
        result = shield.defend(row["prompt"])
        
        latency = (time.time() - start) * 1000
        latencies.append(latency)
        
        results.append({
            "prompt": row["prompt"][:50] + "..." if len(row["prompt"]) > 50 else row["prompt"],
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
    
    print("\n" + "="*60)
    print("🛡️  JAILBREAK SHIELD - LAYER 1 BENCHMARK RESULTS")
    print("="*60)
    print(f"\n📊 DETECTION PERFORMANCE:")
    print(f"  Accuracy:  {metrics['accuracy']*100:.1f}%")
    print(f"  Precision: {metrics['precision']*100:.1f}%")
    print(f"  Recall:    {metrics['recall']*100:.1f}%")
    print(f"  F1 Score:  {metrics['f1_score']*100:.1f}%")
    
    print(f"\n🎯 CONFUSION MATRIX:")
    print(f"  True Positives:  {metrics['true_positives']}")
    print(f"  False Positives: {metrics['false_positives']}")
    print(f"  False Negatives: {metrics['false_negatives']}")
    print(f"  True Negatives:  {metrics['true_negatives']}")
    
    print(f"\n⚡ PERFORMANCE:")
    print(f"  Avg Latency: {sum(latencies)/len(latencies):.2f}ms")
    print(f"  Min Latency: {min(latencies):.2f}ms")
    print(f"  Max Latency: {max(latencies):.2f}ms")
    print(f"  Total Time:  {sum(latencies)/1000:.2f}s")
    
    print(f"\n✅ Full results saved to: data/benchmark_results.csv")
    print("="*60)
    
    # Summary by category
    print("\n📈 RESULTS BY CATEGORY:")
    for category in results_df["category"].unique():
        cat_df = results_df[results_df["category"] == category]
        accuracy = (cat_df["expected_malicious"] == cat_df["detected_malicious"]).mean()
        print(f"  {category:20s}: {accuracy*100:5.1f}% accuracy ({len(cat_df)} samples)")


if __name__ == "__main__":
    main()
