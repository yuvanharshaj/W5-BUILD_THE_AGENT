import json

def calculate_scores(case_id):
    with open('workspace/data/synthetic_cases.json', 'r') as f:
        data = json.load(f)
        
    case = next(c for c in data['cases'] if c['id'] == case_id)
    
    symptoms = case['symptoms']
    candidates = case['candidate_conditions']
    
    raw_scores = []
    
    for candidate in candidates:
        prior = candidate['prior_probability']
        weights = candidate['evidence_weights']
        
        matching_weights = []
        for symptom in symptoms:
            matching_weights.append(weights.get(symptom, 0.0))
            
        avg_matching = sum(matching_weights) / len(symptoms)
        raw_score = prior * avg_matching
        raw_scores.append({
            'name': candidate['name'],
            'raw': raw_score,
            'prior': prior,
            'avg_matching': avg_matching
        })
        
    total_raw = sum(c['raw'] for c in raw_scores)
    
    for c in raw_scores:
        c['normalized'] = c['raw'] / total_raw if total_raw > 0 else 0
        
    # Sort
    raw_scores.sort(key=lambda x: x['normalized'], reverse=True)
    
    print(f"Results for {case_id}:")
    for c in raw_scores:
        print(f"{c['name']}: {c['normalized']*100:.2f}% (Raw: {c['raw']:.4f})")

calculate_scores('CASE-001')
