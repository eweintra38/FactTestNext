#!/usr/bin/env python3
"""
Simple test script to demonstrate the FactTest pipeline with a small subset of data.
"""
import json
import random
import numpy as np
from scipy.stats import entropy

# Create a small test dataset
test_data = [
    ["What is the capital of France?", "Paris"],
    ["What is the capital of Germany?", "Berlin"],
    ["What is the capital of Italy?", "Rome"],
    ["What is the capital of Spain?", "Madrid"],
    ["What is the capital of Japan?", "Tokyo"]
]

def simulate_model_responses(question, correct_answer, num_samples=5):
    """Simulate model responses for a given question."""
    responses = []
    
    # Simulate responses with some variability
    # 70% chance correct, 30% chance of common alternatives
    alternatives = ["London", "New York", "Washington", "Moscow", "Beijing"]
    
    for _ in range(num_samples):
        if random.random() < 0.7:  # 70% chance correct
            responses.append(correct_answer)
        else:  # 30% chance incorrect
            responses.append(random.choice(alternatives))
    
    return responses

def calculate_certainty_score(responses):
    """Calculate certainty score using entropy."""
    # Count occurrences
    response_counts = {}
    for response in responses:
        response_counts[response] = response_counts.get(response, 0) + 1
    
    # Calculate entropy
    frequencies = list(response_counts.values())
    response_entropy = entropy(frequencies)
    
    # Return negative entropy (higher certainty = lower entropy = higher score)
    return -response_entropy

def main():
    print("=== FactTest Demo: Vanilla Entropy Method ===\n")
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Generate certainty scores for each question
    certainty_scores = []
    
    print("Generating certainty scores for each question:")
    print("-" * 50)
    
    for question, correct_answer in test_data:
        responses = simulate_model_responses(question, correct_answer)
        certainty = calculate_certainty_score(responses)
        certainty_scores.append(certainty)
        
        print(f"Question: {question}")
        print(f"Correct: {correct_answer}")
        print(f"Model responses: {responses}")
        print(f"Certainty score: {certainty:.3f}")
        print()
    
    # Calibration: find threshold
    print("=== Calibration Results ===")
    certainty_scores.sort()
    print(f"Certainty scores (sorted): {[f'{s:.3f}' for s in certainty_scores]}")
    
    # Simple threshold selection (for demo purposes)
    alpha = 0.05  # Significance level
    threshold_index = int((1 - alpha) * len(certainty_scores))
    threshold = certainty_scores[threshold_index] if threshold_index < len(certainty_scores) else certainty_scores[-1]
    
    print(f"Alpha (significance level): {alpha}")
    print(f"Threshold: {threshold:.3f}")
    
    # Evaluation simulation
    print("\n=== Evaluation Simulation ===")
    
    # Generate test questions and evaluate
    test_questions = [
        ["What is the capital of Brazil?", "Brasilia"],
        ["What is the capital of Australia?", "Canberra"],
        ["What is the capital of Canada?", "Ottawa"]
    ]
    
    total_predictions = 0
    correct_predictions = 0
    abstained = 0
    
    print("Evaluating test questions:")
    print("-" * 30)
    
    for question, correct_answer in test_questions:
        responses = simulate_model_responses(question, correct_answer)
        certainty = calculate_certainty_score(responses)
        
        if certainty >= threshold:
            # Model is confident, make prediction
            most_common = max(set(responses), key=responses.count)
            is_correct = most_common == correct_answer
            total_predictions += 1
            if is_correct:
                correct_predictions += 1
            
            print(f"Question: {question}")
            print(f"Prediction: {most_common} ({'Correct' if is_correct else 'Incorrect'})")
            print(f"Certainty: {certainty:.3f} (>= {threshold:.3f})")
        else:
            # Model abstains
            abstained += 1
            print(f"Question: {question}")
            print(f"Model abstained (certainty: {certainty:.3f} < {threshold:.3f})")
        print()
    
    # Calculate metrics
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    abstention_rate = abstained / (total_predictions + abstained)
    
    print("=== Final Results ===")
    print(f"Total questions: {len(test_questions)}")
    print(f"Predictions made: {total_predictions}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Abstained: {abstained}")
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Abstention rate: {abstention_rate:.1%}")
    
    print("\n=== Expected Paper Results Comparison ===")
    print("According to the FactTest paper (arXiv:2411.02603):")
    print("- The method should provide statistical guarantees for Type I error control")
    print("- Vanilla entropy method shows good performance on ParaRel dataset")
    print("- Expected accuracy improvement of >40% when allowing abstention")
    print("- Trade-off between accuracy and coverage (1 - abstention rate)")

if __name__ == "__main__":
    main()