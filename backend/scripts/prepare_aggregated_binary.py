import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_and_prepare_binary():
    """Analyze aggregated data and create binary datasets"""
    
    # Create output directory for plots
    os.makedirs('../data/training/analysis_plots', exist_ok=True)
    
    print("="*70)
    print("AGGREGATED DATA ANALYSIS & BINARY DATASET PREPARATION")
    print("="*70)
    
    # Load aggregated datasets
    train_df = pd.read_csv('../data/training/mbti_aggregated_train.csv')
    val_df = pd.read_csv('../data/training/mbti_aggregated_val.csv')
    test_df = pd.read_csv('../data/training/mbti_aggregated_test.csv')
    
    print(f"\n1. DATASET SIZES:")
    print(f"   Train: {len(train_df)} people")
    print(f"   Val:   {len(val_df)} people")
    print(f"   Test:  {len(test_df)} people")
    print(f"   Total: {len(train_df) + len(val_df) + len(test_df)} people")
    
    # Text length analysis
    print(f"\n2. TEXT LENGTH ANALYSIS:")
    train_df['text_length'] = train_df['text'].str.len()
    val_df['text_length'] = val_df['text'].str.len()
    test_df['text_length'] = test_df['text'].str.len()
    
    all_lengths = pd.concat([train_df['text_length'], val_df['text_length'], test_df['text_length']])
    
    print(f"   Min length:    {all_lengths.min()} characters")
    print(f"   Max length:    {all_lengths.max()} characters")
    print(f"   Mean length:   {all_lengths.mean():.0f} characters")
    print(f"   Median length: {all_lengths.median():.0f} characters")
    
    # Plot text length distribution
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(all_lengths, bins=50, edgecolor='black', color='skyblue')
    plt.xlabel('Text Length (characters)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Aggregated Text Lengths', fontsize=14, fontweight='bold')
    plt.axvline(all_lengths.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {all_lengths.mean():.0f}')
    plt.axvline(all_lengths.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {all_lengths.median():.0f}')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.boxplot([train_df['text_length'], val_df['text_length'], test_df['text_length']], 
                labels=['Train', 'Val', 'Test'])
    plt.ylabel('Text Length (characters)', fontsize=12)
    plt.title('Text Length by Split', fontsize=14, fontweight='bold')
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../data/training/analysis_plots/text_length_distribution.png', dpi=300, bbox_inches='tight')
    print(f"\n   📊 Saved: text_length_distribution.png")
    
    # MBTI type distribution
    print(f"\n3. MBTI TYPE DISTRIBUTION:")
    
    combined_df = pd.concat([train_df, val_df, test_df])
    type_counts = combined_df['type'].value_counts().sort_index()
    
    print(f"   Types represented: {len(type_counts)}/16")
    print("\n   Distribution:")
    for mbti_type, count in type_counts.items():
        print(f"   {mbti_type}: {count:3d} ({count/len(combined_df)*100:.1f}%)")
    
    # Plot MBTI distribution
    plt.figure(figsize=(14, 6))
    colors = ['#3498db' if count >= 150 else '#e74c3c' for count in type_counts]
    bars = plt.bar(type_counts.index, type_counts.values, color=colors, edgecolor='black')
    plt.xlabel('MBTI Type', fontsize=12, fontweight='bold')
    plt.ylabel('Number of People', fontsize=12, fontweight='bold')
    plt.title('MBTI Type Distribution (Aggregated Dataset)', fontsize=14, fontweight='bold')
    plt.axhline(y=150, color='orange', linestyle='--', linewidth=2, label='Target: 150+')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../data/training/analysis_plots/mbti_distribution.png', dpi=300, bbox_inches='tight')
    print(f"\n   📊 Saved: mbti_distribution.png")
    
    # Dimension distribution
    print(f"\n4. DIMENSION ANALYSIS:")
    
    dimensions = {
        'I/E': lambda t: t[0],
        'N/S': lambda t: t[1],
        'T/F': lambda t: t[2],
        'J/P': lambda t: t[3]
    }
    
    dim_counts = {}
    for dim_name, extractor in dimensions.items():
        counts = combined_df['type'].apply(extractor).value_counts()
        dim_counts[dim_name] = counts
        letter1, letter2 = dim_name.split('/')
        print(f"\n   {dim_name} Distribution:")
        print(f"   {letter1}: {counts.get(letter1, 0):4d} ({counts.get(letter1, 0)/len(combined_df)*100:.1f}%)")
        print(f"   {letter2}: {counts.get(letter2, 0):4d} ({counts.get(letter2, 0)/len(combined_df)*100:.1f}%)")
    
    # Plot dimension distributions
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('MBTI Dimension Distributions', fontsize=16, fontweight='bold')
    
    for idx, (dim_name, counts) in enumerate(dim_counts.items()):
        ax = axes[idx // 2, idx % 2]
        letters = dim_name.split('/')
        values = [counts.get(letters[0], 0), counts.get(letters[1], 0)]
        
        bars = ax.bar(letters, values, color=['#3498db', '#e74c3c'], edgecolor='black', linewidth=2)
        ax.set_ylabel('Number of People', fontsize=11, fontweight='bold')
        ax.set_title(f'{dim_name} Dimension', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add percentage labels
        for bar, val in zip(bars, values):
            percentage = val / sum(values) * 100
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                   f'{val}\n({percentage:.1f}%)', 
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../data/training/analysis_plots/dimension_distributions.png', dpi=300, bbox_inches='tight')
    print(f"\n   📊 Saved: dimension_distributions.png")
    
    # Sample text examples
    print(f"\n5. SAMPLE TEXT EXAMPLES:")
    
    sample_types = ['INTJ', 'ENFP', 'ISTP', 'INFJ']
    for mbti_type in sample_types:
        sample = combined_df[combined_df['type'] == mbti_type].iloc[0] if len(combined_df[combined_df['type'] == mbti_type]) > 0 else None
        if sample is not None:
            text_preview = sample['text'][:200] + "..." if len(sample['text']) > 200 else sample['text']
            print(f"\n   {mbti_type} Sample ({len(sample['text'])} chars):")
            print(f"   \"{text_preview}\"")
    
    # Create binary datasets
    print(f"\n6. CREATING BINARY DATASETS:")
    
    def extract_dimension(df, dimension_index, letters):
        """Extract binary labels for a specific MBTI dimension"""
        df_copy = df.copy()
        df_copy['label'] = df_copy['type'].str[dimension_index]
        df_copy['binary_label'] = df_copy['label'].apply(lambda x: 0 if x == letters[0] else 1)
        return df_copy[['text', 'binary_label', 'label']]
    
    dimensions_to_create = [
        ('IE', 0, ('I', 'E')),
        ('NS', 1, ('N', 'S')),
        ('TF', 2, ('T', 'F')),
        ('JP', 3, ('J', 'P'))
    ]
    
    os.makedirs('../data/training/aggregated_binary', exist_ok=True)
    
    for dim_name, dim_index, letters in dimensions_to_create:
        print(f"\n   Creating {dim_name} ({letters[0]} vs {letters[1]})...")
        
        train_binary = extract_dimension(train_df, dim_index, letters)
        val_binary = extract_dimension(val_df, dim_index, letters)
        test_binary = extract_dimension(test_df, dim_index, letters)
        
        # Distribution
        train_dist = train_binary['label'].value_counts()
        test_dist = test_binary['label'].value_counts()
        
        print(f"   Train: {letters[0]}={train_dist.get(letters[0], 0)}, {letters[1]}={train_dist.get(letters[1], 0)}")
        print(f"   Test:  {letters[0]}={test_dist.get(letters[0], 0)}, {letters[1]}={test_dist.get(letters[1], 0)}")
        
        # Save
        train_binary.to_csv(f'../data/training/aggregated_binary/{dim_name}_train.csv', index=False)
        val_binary.to_csv(f'../data/training/aggregated_binary/{dim_name}_val.csv', index=False)
        test_binary.to_csv(f'../data/training/aggregated_binary/{dim_name}_test.csv', index=False)
    
    # Create analysis summary
    summary = {
        'dataset_info': {
            'total_people': len(combined_df),
            'train_size': len(train_df),
            'val_size': len(val_df),
            'test_size': len(test_df)
        },
        'text_statistics': {
            'min_length': int(all_lengths.min()),
            'max_length': int(all_lengths.max()),
            'mean_length': float(all_lengths.mean()),
            'median_length': float(all_lengths.median())
        },
        'mbti_distribution': type_counts.to_dict(),
        'dimension_distributions': {
            dim: {letter: int(counts.get(letter, 0)) for letter in dim.split('/')}
            for dim, counts in dim_counts.items()
        }
    }
    
    import json
    with open('../data/training/analysis_plots/dataset_analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nFiles created:")
    print(f"  📊 3 analysis plots in: data/training/analysis_plots/")
    print(f"  📄 Analysis summary JSON")
    print(f"  📁 12 binary CSV files in: data/training/aggregated_binary/")
    print(f"\nReady for training!")

if __name__ == '__main__':
    analyze_and_prepare_binary()