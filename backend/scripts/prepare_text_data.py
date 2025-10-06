import pandas as pd
import re
from sklearn.model_selection import train_test_split

def clean_text(text):
    """Clean text data"""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user mentions
    text = re.sub(r'@\w+', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def prepare_dataset():
    """Prepare MBTI text dataset"""
    print("Loading dataset...")
    
    # Load CSV
    df = pd.read_csv('../data/training/mbti_1.csv')
    
    print(f"Original dataset: {len(df)} samples")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nMBTI type distribution:")
    print(df['type'].value_counts())
    
    # Clean posts
    df['posts'] = df['posts'].apply(clean_text)
    
    # Filter out very short posts (less than 50 characters)
    df = df[df['posts'].str.len() >= 50]
    
    # Split posts into individual texts (currently multiple posts per row)
    # Each row has multiple posts separated by |||
    rows = []
    for _, row in df.iterrows():
        posts = row['posts'].split('|||')
        for post in posts:
            post = post.strip()
            if len(post) >= 100:  # Only keep substantial posts
                rows.append({
                    'text': post,
                    'type': row['type']
                })
    
    df_expanded = pd.DataFrame(rows)
    
    print(f"\nExpanded dataset: {len(df_expanded)} samples")
    print(f"\nType distribution after expansion:")
    print(df_expanded['type'].value_counts())
    
    # Balance dataset by undersampling majority classes
    # Get minimum class count
    min_count = df_expanded['type'].value_counts().min()
    target_per_class = min(min_count * 2, 600)  # Max 600 per class
    
    balanced_dfs = []
    for mbti_type in df_expanded['type'].unique():
        type_df = df_expanded[df_expanded['type'] == mbti_type]
        if len(type_df) > target_per_class:
            type_df = type_df.sample(n=target_per_class, random_state=42)
        balanced_dfs.append(type_df)
    
    df_balanced = pd.concat(balanced_dfs, ignore_index=True)
    
    print(f"\nBalanced dataset: {len(df_balanced)} samples")
    print(f"Samples per type: ~{target_per_class}")
    
    # Shuffle
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split: 80% train, 10% val, 10% test
    train_df, temp_df = train_test_split(df_balanced, test_size=0.2, random_state=42, stratify=df_balanced['type'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['type'])
    
    print(f"\nTrain: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # Save processed datasets
    train_df.to_csv('../data/training/mbti_train.csv', index=False)
    val_df.to_csv('../data/training/mbti_val.csv', index=False)
    test_df.to_csv('../data/training/mbti_test.csv', index=False)
    
    print("\nDatasets saved:")
    print("- mbti_train.csv")
    print("- mbti_val.csv")
    print("- mbti_test.csv")
    
    return train_df, val_df, test_df

if __name__ == '__main__':
    prepare_dataset()