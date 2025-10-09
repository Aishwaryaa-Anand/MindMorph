import pandas as pd
import numpy as np

def aggregate_posts():
    """Combine all posts for each person into one long text"""
    
    print("Loading original dataset...")
    df = pd.read_csv('../data/training/mbti_1.csv')
    
    print(f"Original: {len(df)} people")
    print(f"MBTI distribution:\n{df['type'].value_counts()}")
    
    # Each row already has multiple posts separated by |||
    # We just need to clean and keep them combined
    
    def clean_and_combine(posts_text):
        """Clean the combined posts"""
        # Split by |||
        posts = posts_text.split('|||')
        # Clean each post
        cleaned = []
        for post in posts:
            post = post.strip()
            if len(post) > 50:  # Keep substantial posts
                cleaned.append(post)
        
        # Combine back with space
        return ' '.join(cleaned)
    
    df['combined_text'] = df['posts'].apply(clean_and_combine)
    
    # Filter: keep only if combined text is substantial (at least 500 characters)
    df = df[df['combined_text'].str.len() >= 500]
    
    print(f"\nAfter filtering (min 500 chars): {len(df)} people")
    
    # Check text lengths
    df['text_length'] = df['combined_text'].str.len()
    print(f"\nText length statistics:")
    print(f"  Min: {df['text_length'].min()}")
    print(f"  Mean: {df['text_length'].mean():.0f}")
    print(f"  Median: {df['text_length'].median():.0f}")
    print(f"  Max: {df['text_length'].max()}")
    
    # Balance classes
    # Get minimum class count
    min_count = df['type'].value_counts().min()
    # Set target (use at least 200 per class, or min_count if less)
    target_per_class = min(max(min_count, 200), 400)
    
    print(f"\nBalancing to {target_per_class} samples per MBTI type...")
    
    balanced_dfs = []
    for mbti_type in df['type'].unique():
        type_df = df[df['type'] == mbti_type]
        if len(type_df) > target_per_class:
            # Sample the ones with longest text (more personality signal)
            type_df = type_df.nlargest(target_per_class, 'text_length')
        balanced_dfs.append(type_df)
    
    df_balanced = pd.concat(balanced_dfs, ignore_index=True)
    
    print(f"\nBalanced dataset: {len(df_balanced)} people")
    print(f"Distribution:\n{df_balanced['type'].value_counts().sort_index()}")
    
    # Shuffle
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split: 70% train, 15% val, 15% test
    from sklearn.model_selection import train_test_split
    
    train_df, temp_df = train_test_split(
        df_balanced[['combined_text', 'type']], 
        test_size=0.30, 
        random_state=42, 
        stratify=df_balanced['type']
    )
    
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=0.50, 
        random_state=42, 
        stratify=temp_df['type']
    )
    
    print(f"\nSplit sizes:")
    print(f"  Train: {len(train_df)}")
    print(f"  Val:   {len(val_df)}")
    print(f"  Test:  {len(test_df)}")
    
    # Rename column for consistency
    train_df = train_df.rename(columns={'combined_text': 'text'})
    val_df = val_df.rename(columns={'combined_text': 'text'})
    test_df = test_df.rename(columns={'combined_text': 'text'})
    
    # Save
    train_df.to_csv('../data/training/mbti_aggregated_train.csv', index=False)
    val_df.to_csv('../data/training/mbti_aggregated_val.csv', index=False)
    test_df.to_csv('../data/training/mbti_aggregated_test.csv', index=False)
    
    print("\n" + "="*60)
    print("Aggregated datasets saved!")
    print("="*60)
    print("Files:")
    print("  - mbti_aggregated_train.csv")
    print("  - mbti_aggregated_val.csv")
    print("  - mbti_aggregated_test.csv")
    
    return train_df, val_df, test_df

if __name__ == '__main__':
    aggregate_posts()