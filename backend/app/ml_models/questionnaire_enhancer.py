import json
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

class QuestionnaireMLEnhancer:
    """Simple ML model to enhance questionnaire confidence scores"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = os.path.join(os.path.dirname(__file__), 'questionnaire_model.pkl')
        
        # Try to load existing model
        self.load_model()
    
    def load_training_data(self):
        """Load training data"""
        data_path = os.path.join(os.path.dirname(__file__), '../../data/training/questionnaire_training_data.json')
        
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    def train(self):
        """Train the ML model"""
        print("Training questionnaire ML model...")
        
        # Load data
        training_data = self.load_training_data()
        
        # Prepare features and labels
        X = []  # Answer patterns
        y = []  # MBTI types
        
        for sample in training_data:
            X.append(sample['answers'])
            y.append(sample['mbti'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X, y_encoded)
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        print(f"✅ Model trained successfully! Accuracy: {self.model.score(X, y_encoded):.2%}")
        
        return True
    
    def save_model(self):
        """Save trained model"""
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.model = model_data['model']
                self.label_encoder = model_data['label_encoder']
                self.is_trained = True
                
                print("✅ Loaded existing ML model")
                return True
            except Exception as e:
                print(f"Failed to load model: {e}")
                return False
        return False
    
    def enhance_confidence(self, answers, base_mbti, base_confidence):
        """
        Enhance confidence scores using ML
        
        Args:
            answers: List of answer choices (A, B, C)
            base_mbti: MBTI type from rule-based scoring
            base_confidence: Confidence scores from rule-based scoring
        
        Returns:
            Enhanced confidence scores
        """
        if not self.is_trained:
            # If model not trained, return base confidence
            return base_confidence
        
        try:
            # Convert answers to numeric (A=1, B=2, C=3)
            numeric_answers = []
            for ans in answers:
                choice = ans['choice']
                if choice == 'A':
                    numeric_answers.append(1)
                elif choice == 'B':
                    numeric_answers.append(2)
                else:  # C
                    numeric_answers.append(3)
            
            # Predict with model
            X = np.array([numeric_answers])
            probabilities = self.model.predict_proba(X)[0]
            
            # Get predicted MBTI
            predicted_idx = np.argmax(probabilities)
            predicted_mbti = self.label_encoder.inverse_transform([predicted_idx])[0]
            
            # Calculate enhancement factor
            if predicted_mbti == base_mbti:
                # Model agrees - boost confidence
                ml_confidence = probabilities[predicted_idx]
                enhancement_factor = 0.7 * ml_confidence + 0.3  # Scale to 0.3-1.0
            else:
                # Model disagrees - slightly reduce confidence
                enhancement_factor = 0.85
            
            # Apply enhancement to each dimension
            enhanced_confidence = {}
            for dim, conf in base_confidence.items():
                enhanced = conf * enhancement_factor
                # Keep within reasonable bounds
                enhanced = max(0.50, min(0.99, enhanced))
                enhanced_confidence[dim] = round(enhanced, 2)
            
            return enhanced_confidence
            
        except Exception as e:
            print(f"ML enhancement failed: {e}")
            return base_confidence

# Global instance
ml_enhancer = QuestionnaireMLEnhancer()

# Train on first import if not already trained
if not ml_enhancer.is_trained:
    ml_enhancer.train()