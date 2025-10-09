import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

class TextMBTIClassifier:
    """Text-based MBTI classifier using aggregated ensemble models"""
    
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.bert_model = None
        self.is_loaded = False
        
        # Try to load models
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        try:
            model_dir = os.path.join(os.path.dirname(__file__), 'text')
            
            print("Loading text classification models...")
            
            # Load BERT model
            print("  - Loading BERT model...")
            self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load 4 binary classifiers and vectorizers
            dimensions = ['IE', 'NS', 'TF', 'JP']
            
            for dim in dimensions:
                ensemble_path = os.path.join(model_dir, f'{dim}_aggregated_ensemble.pkl')
                vectorizer_path = os.path.join(model_dir, f'{dim}_aggregated_vectorizer.pkl')
                
                with open(ensemble_path, 'rb') as f:
                    self.models[dim] = pickle.load(f)
                
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizers[dim] = pickle.load(f)
                
                print(f"  - Loaded {dim} classifier")
            
            self.is_loaded = True
            print("✅ Text classification models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Failed to load text models: {str(e)}")
            self.is_loaded = False
    
    def extract_linguistic_features(self, text):
        """Extract linguistic features from text"""
        words = text.split()
        sentences = text.split('.')
        
        features = {
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'avg_sentence_length': np.mean([len(s.split()) for s in sentences]) if sentences else 0,
            'num_words': len(words),
            'num_sentences': len(sentences),
            'num_chars': len(text),
            
            # Punctuation
            'exclamation_ratio': text.count('!') / max(len(words), 1),
            'question_ratio': text.count('?') / max(len(words), 1),
            'comma_ratio': text.count(',') / max(len(words), 1),
            'ellipsis_ratio': text.count('...') / max(len(words), 1),
            
            # Capitalization
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'title_case_words': sum(1 for w in words if w.istitle()) / max(len(words), 1),
            
            # Personal pronouns
            'i_count': text.lower().count(' i ') / max(len(words), 1),
            'we_count': text.lower().count(' we ') / max(len(words), 1),
            'you_count': text.lower().count(' you ') / max(len(words), 1),
            
            # Emotional words
            'positive_words': sum(1 for w in ['good', 'great', 'happy', 'love', 'like', 'best', 'amazing', 'wonderful'] if w in text.lower()) / max(len(words), 1),
            'negative_words': sum(1 for w in ['bad', 'hate', 'worst', 'never', 'no', 'not', 'terrible', 'awful'] if w in text.lower()) / max(len(words), 1),
            
            # Thinking words
            'think_words': sum(1 for w in ['think', 'believe', 'feel', 'know', 'understand', 'realize', 'consider'] if w in text.lower()) / max(len(words), 1),
            
            # Social words
            'social_words': sum(1 for w in ['friend', 'people', 'together', 'meet', 'party', 'group', 'social'] if w in text.lower()) / max(len(words), 1),
            
            # Planning words
            'plan_words': sum(1 for w in ['plan', 'schedule', 'organize', 'prepare', 'ready', 'structured'] if w in text.lower()) / max(len(words), 1),
            
            # Abstract words
            'abstract_words': sum(1 for w in ['idea', 'theory', 'concept', 'possibility', 'future', 'potential', 'vision'] if w in text.lower()) / max(len(words), 1),
        }
        
        return np.array(list(features.values())).reshape(1, -1)
    
    def predict(self, text):
        """
        Predict MBTI type from text
        
        Args:
            text: Input text (minimum 500 characters recommended)
        
        Returns:
            tuple: (mbti_type, confidence_dict, keywords)
        """
        if not self.is_loaded:
            raise Exception("Models not loaded")
        
        if len(text) < 100:
            raise ValueError("Text too short. Minimum 100 characters required.")
        
        # Extract features
        bert_features = self.bert_model.encode([text])
        linguistic_features = self.extract_linguistic_features(text)
        
        # Predict each dimension
        mbti_letters = []
        confidence_scores = {}
        dimension_map = {
            'IE': ('I', 'E'),
            'NS': ('N', 'S'),
            'TF': ('T', 'F'),
            'JP': ('J', 'P')
        }
        
        for dim, letters in dimension_map.items():
            # Get CountVectorizer features
            count_features = self.vectorizers[dim].transform([text]).toarray()
            
            # Combine all features
            combined_features = np.hstack([bert_features, count_features, linguistic_features])
            
            # Predict
            prediction = self.models[dim].predict(combined_features)[0]
            
            # Get probability
            if hasattr(self.models[dim], 'predict_proba'):
                proba = self.models[dim].predict_proba(combined_features)[0]
                confidence = float(proba[prediction])
            else:
                confidence = 0.75  # Default if no probability available
            
            # Determine letter
            predicted_letter = letters[1] if prediction == 1 else letters[0]
            mbti_letters.append(predicted_letter)
            
            confidence_scores[dim] = round(confidence, 2)
        
        mbti_type = ''.join(mbti_letters)
        
        # Extract keywords (top features from CountVectorizer)
        keywords = self._extract_keywords(text)
        
        return mbti_type, confidence_scores, keywords
    
    def _extract_keywords(self, text):
        """Extract top keywords that influenced prediction"""
        keywords = []
        
        # Get words from each dimension's vectorizer
        for dim in ['IE', 'NS', 'TF', 'JP']:
            vectorizer = self.vectorizers[dim]
            features = vectorizer.transform([text]).toarray()[0]
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top 5 features for this dimension
            top_indices = features.argsort()[-5:][::-1]
            dim_keywords = [feature_names[i] for i in top_indices if features[i] > 0]
            keywords.extend(dim_keywords)
        
        # Remove duplicates and return top 10
        keywords = list(dict.fromkeys(keywords))[:10]
        
        return keywords

# Global instance
text_classifier = TextMBTIClassifier()