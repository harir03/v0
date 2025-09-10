#!/usr/bin/env python3
"""
Enhanced Duplicate Detection Module for LinkedIn Bot

Enhanced duplicate comment detection using multiple methods:
1. TF-IDF and cosine similarity for semantic matching
2. N-gram fingerprinting for partial matches
3. Key phrase extraction for content similarity
"""

import re
import string
import hashlib

# Check for optional dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


class EnhancedDuplicateDetector:
    """
    Enhanced duplicate comment detection using multiple methods:
    1. TF-IDF and cosine similarity for semantic matching
    2. N-gram fingerprinting for partial matches
    3. Key phrase extraction for content similarity
    """
    
    def __init__(self, similarity_threshold=0.75):
        """
        Initialize the duplicate detector.
        
        Args:
            similarity_threshold (float): Threshold for considering comments as duplicates
        """
        self.similarity_threshold = similarity_threshold
        
        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        
        if NLTK_AVAILABLE:
            self.stop_words = set(stopwords.words('english'))
        else:
            # Basic stopwords list if NLTK is not available
            self.stop_words = set([
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
                'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
                'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
                'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
                'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
                'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
                'about', 'against', 'between', 'into', 'through', 'during', 'before', 
                'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
                'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once'
            ])
            
    def preprocess_text(self, text):
        """
        Preprocess text for comparison.
        
        Args:
            text (str): Text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        if not text:
            return ""
            
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Simple tokenization and stopword removal
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        return ' '.join(words)
        
    def calculate_similarity(self, text1, text2):
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1, text2 (str): Texts to compare
            
        Returns:
            float: Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
            
        # For very short texts, use a different approach
        if len(text1) < 20 or len(text2) < 20:
            return self._calculate_short_text_similarity(text1, text2)
            
        # Preprocess texts
        processed1 = self.preprocess_text(text1)
        processed2 = self.preprocess_text(text2)
        
        # Skip if either text is empty after preprocessing
        if not processed1 or not processed2:
            return 0.0
            
        if SKLEARN_AVAILABLE:
            try:
                # Create document-term matrix
                documents = [processed1, processed2]
                tfidf_matrix = self.vectorizer.fit_transform(documents)
                
                # Calculate cosine similarity
                similarity_matrix = cosine_similarity(tfidf_matrix)
                return similarity_matrix[0][1]
            except:
                # Fallback to simple similarity
                return self._calculate_simple_similarity(processed1, processed2)
        else:
            return self._calculate_simple_similarity(processed1, processed2)
            
    def _calculate_short_text_similarity(self, text1, text2):
        """Calculate similarity for very short texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
        
    def _calculate_simple_similarity(self, text1, text2):
        """Calculate simple word-based similarity."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
        
    def generate_fingerprint(self, text, n=3):
        """Generate n-gram fingerprint of the text."""
        if not text:
            return set()
            
        # Convert to lowercase and remove punctuation
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        
        # Generate n-grams
        ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
        
        # Generate hashes
        fingerprint = set()
        for ngram in ngrams:
            fingerprint.add(hashlib.md5(ngram.encode()).hexdigest()[:8])
            
        return fingerprint
        
    def calculate_fingerprint_similarity(self, text1, text2, n=3):
        """Calculate similarity using n-gram fingerprinting."""
        if not text1 or not text2:
            return 0.0
            
        fingerprint1 = self.generate_fingerprint(text1, n)
        fingerprint2 = self.generate_fingerprint(text2, n)
        
        if not fingerprint1 or not fingerprint2:
            return 0.0
            
        intersection = len(fingerprint1.intersection(fingerprint2))
        union = len(fingerprint1.union(fingerprint2))
        
        return intersection / union if union > 0 else 0.0
        
    def is_duplicate(self, text1, text2):
        """
        Determine if two texts are duplicates.
        
        Args:
            text1, text2 (str): Texts to compare
            
        Returns:
            tuple: (is_duplicate, confidence_score, method_used)
        """
        # Skip comparison if either text is empty
        if not text1 or not text2:
            return False, 0.0, "empty_text"
            
        # Skip comparison if texts are identical
        if text1.strip() == text2.strip():
            return True, 1.0, "exact_match"
            
        # Calculate semantic similarity
        semantic_similarity = self.calculate_similarity(text1, text2)
        
        # Calculate fingerprint similarity
        fingerprint_similarity = self.calculate_fingerprint_similarity(text1, text2)
        
        # Combine scores with weights
        combined_score = semantic_similarity * 0.7 + fingerprint_similarity * 0.3
        
        # Determine which method contributed most to the result
        if semantic_similarity > fingerprint_similarity:
            primary_method = "semantic"
        else:
            primary_method = "fingerprint"
        
        # Determine if duplicate
        is_duplicate = combined_score >= self.similarity_threshold
        
        return is_duplicate, combined_score, primary_method
        
    def find_similar_comments(self, new_comment, existing_comments, return_details=False):
        """Find similar comments in a list of existing comments."""
        if not new_comment or not existing_comments:
            return []
            
        similar_comments = []
        
        for i, existing in enumerate(existing_comments):
            is_duplicate, similarity, method = self.is_duplicate(new_comment, existing)
            
            if is_duplicate or similarity > 0.5:  # Include high similarity even if not duplicate
                result = {
                    "index": i,
                    "text": existing,
                    "similarity": similarity,
                    "is_duplicate": is_duplicate,
                    "method": method
                }
                similar_comments.append(result)
                
        # Sort by similarity (highest first)
        similar_comments.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similar_comments
