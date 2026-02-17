"""
Fast MCQ Generator - Optimized for speed while maintaining quality
Uses smaller, faster models with intelligent caching and optimization
"""

import os
import re
import json
import random
import time
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import (
        AutoTokenizer, AutoModelForSeq2SeqLM, 
        T5ForConditionalGeneration, T5Tokenizer,
        pipeline
    )
    from sentence_transformers import SentenceTransformer
    import spacy
    import nltk
    from nltk.tokenize import sent_tokenize
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    FAST_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Fast dependencies not available: {e}")
    FAST_DEPENDENCIES_AVAILABLE = False

class FastMCQGenerator:
    """Fast MCQ Generator optimized for speed and efficiency"""
    
    def __init__(self):
        self.models_loaded = False
        self.model_cache_dir = "./fast_models"
        
        # Fast models (smaller, optimized)
        self.question_generator = None
        self.question_tokenizer = None
        self.sentence_model = None
        self.nlp = None
        
        # Cache for repeated operations
        self._sentence_cache = {}
        self._embedding_cache = {}
        
        os.makedirs(self.model_cache_dir, exist_ok=True)
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        """Download NLTK data quickly"""
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.download('punkt_tab', quiet=True)
            except:
                nltk.download('punkt', quiet=True)
    
    def load_fast_models(self):
        """Load fast, optimized models"""
        if not FAST_DEPENDENCIES_AVAILABLE:
            raise ImportError("Fast dependencies not available")
        
        print("⚡ Loading fast MCQ generation models...")
        start_time = time.time()
        
        try:
            # 1. Load T5-Base (much faster than Large)
            print("📚 Loading T5-Base for question generation...")
            model_name = "t5-base"  # 850MB vs 3GB for large
            self.question_tokenizer = T5Tokenizer.from_pretrained(
                model_name, 
                cache_dir=os.path.join(self.model_cache_dir, "question_generation")
            )
            self.question_generator = T5ForConditionalGeneration.from_pretrained(
                model_name,
                cache_dir=os.path.join(self.model_cache_dir, "question_generation"),
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            # Optimize for inference
            self.question_generator.eval()
            if torch.cuda.is_available():
                self.question_generator = self.question_generator.cuda()
            
            # 2. Load fast sentence transformer
            print("🔍 Loading fast sentence transformer...")
            self.sentence_model = SentenceTransformer(
                'all-MiniLM-L6-v2',  # 90MB vs 420MB for mpnet
                cache_folder=os.path.join(self.model_cache_dir, "sentence_transformer")
            )
            
            # 3. Load spaCy small model (fastest)
            print("🧠 Loading spaCy small model...")
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("⚠️ spaCy model not found, downloading...")
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            self.models_loaded = True
            load_time = time.time() - start_time
            print(f"✅ Fast models loaded in {load_time:.1f} seconds!")
            
        except Exception as e:
            print(f"❌ Error loading fast models: {e}")
            self.models_loaded = False
            raise
    
    def generate_fast_questions(self, text: str, num_questions: int = 10, 
                               difficulty: str = "medium") -> List[Dict]:
        """Generate questions quickly with good quality"""
        if not self.models_loaded:
            self.load_fast_models()
        
        if not text.strip():
            return []
        
        print(f"⚡ Fast generating {num_questions} MCQ questions...")
        start_time = time.time()
        
        # Step 1: Quick text analysis
        analysis = self._fast_text_analysis(text)
        
        # Step 2: Generate questions using optimized strategies
        all_questions = []
        
        # Strategy 1: Pattern-based generation (60% - fastest)
        pattern_count = max(1, int(num_questions * 0.6))
        pattern_questions = self._generate_pattern_questions(text, analysis, pattern_count)
        all_questions.extend(pattern_questions)
        
        # Strategy 2: T5-based generation (40% - higher quality)
        remaining = num_questions - len(all_questions)
        if remaining > 0:
            t5_questions = self._generate_fast_t5_questions(text, analysis, remaining)
            all_questions.extend(t5_questions)
        
        # Step 3: Quick quality filter and selection
        final_questions = self._fast_quality_filter(all_questions, num_questions)
        
        # Step 4: Apply difficulty and polish
        for question in final_questions:
            question["difficulty"] = difficulty
            self._quick_polish(question)
        
        generation_time = time.time() - start_time
        print(f"✅ Generated {len(final_questions)} questions in {generation_time:.1f} seconds")
        
        return final_questions
    
    def _fast_text_analysis(self, text: str) -> Dict:
        """Fast text analysis with caching"""
        # Check cache first
        text_hash = hash(text)
        if text_hash in self._sentence_cache:
            return self._sentence_cache[text_hash]
        
        # Quick analysis
        sentences = sent_tokenize(text)
        
        # Fast NLP processing
        doc = self.nlp(text[:1000])  # Limit to first 1000 chars for speed
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Quick factual statement extraction
        factual_statements = []
        for sentence in sentences:
            if self._is_factual_sentence(sentence):
                factual_statements.append(sentence)
        
        # Quick key phrase extraction
        key_phrases = self._extract_key_phrases_fast(text)
        
        analysis = {
            "sentences": sentences,
            "entities": entities,
            "factual_statements": factual_statements,
            "key_phrases": key_phrases
        }
        
        # Cache result
        self._sentence_cache[text_hash] = analysis
        return analysis
    
    def _is_factual_sentence(self, sentence: str) -> bool:
        """Quick check if sentence contains factual information"""
        factual_indicators = [
            r'\b(?:is|are|was|were)\s+(?:a|an|the)?\s*\w+',
            r'\b(?:created|developed|invented|founded)\b',
            r'\b\d{4}\b',  # Years
            r'\b(?:first|second|primary|main)\b',
            r'\b(?:features?|includes?|supports?)\b'
        ]
        
        return any(re.search(pattern, sentence, re.IGNORECASE) for pattern in factual_indicators)
    
    def _extract_key_phrases_fast(self, text: str) -> List[str]:
        """Fast key phrase extraction using simple patterns"""
        # Extract capitalized phrases (likely important terms)
        phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Extract quoted terms
        quoted = re.findall(r'"([^"]+)"', text)
        phrases.extend(quoted)
        
        # Remove duplicates and filter
        unique_phrases = list(set(phrases))
        return [p for p in unique_phrases if len(p) > 2 and len(p) < 50][:10]
    
    def _generate_pattern_questions(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate questions using fast pattern matching"""
        questions = []
        
        # Enhanced patterns for fast generation
        patterns = [
            # Definition patterns
            {
                'pattern': r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a\s+|an\s+|the\s+)?([^.]{10,80})',
                'question_template': 'What is {term}?',
                'answer_group': 2,
                'term_group': 1
            },
            # Creation patterns
            {
                'pattern': r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:was\s+)?(?:created|developed|invented|founded)\s+by\s+([^.]{5,50})',
                'question_template': 'What was created by {creator}?',
                'answer_group': 1,
                'creator_group': 2
            },
            # Year patterns
            {
                'pattern': r'(?:in\s+|during\s+)?(\d{4})',
                'question_template': 'In which year did this occur?',
                'answer_group': 1
            },
            # Feature patterns
            {
                'pattern': r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:features?|supports?|includes?)\s+([^.]{10,60})',
                'question_template': 'What does {subject} feature?',
                'answer_group': 2,
                'subject_group': 1
            }
        ]
        
        for sentence in analysis["factual_statements"][:num_questions * 2]:
            if len(questions) >= num_questions:
                break
            
            for pattern_info in patterns:
                match = re.search(pattern_info['pattern'], sentence, re.IGNORECASE)
                if match:
                    answer = match.group(pattern_info['answer_group']).strip()
                    answer = re.sub(r'^(?:a\s+|an\s+|the\s+)', '', answer, flags=re.IGNORECASE)
                    answer = answer.strip(' .,;:')
                    
                    if len(answer) > 3 and len(answer) < 80:
                        # Build question
                        question_text = pattern_info['question_template']
                        
                        # Replace placeholders
                        if '{term}' in question_text and 'term_group' in pattern_info:
                            term = match.group(pattern_info['term_group'])
                            question_text = question_text.replace('{term}', term)
                        
                        if '{creator}' in question_text and 'creator_group' in pattern_info:
                            creator = match.group(pattern_info['creator_group'])
                            question_text = question_text.replace('{creator}', creator)
                        
                        if '{subject}' in question_text and 'subject_group' in pattern_info:
                            subject = match.group(pattern_info['subject_group'])
                            question_text = question_text.replace('{subject}', subject)
                        
                        # Generate fast distractors
                        options = self._generate_fast_distractors(answer, sentence, text)
                        
                        if len(options) >= 4:
                            questions.append({
                                "question": question_text,
                                "options": {
                                    "A": options[0],
                                    "B": options[1],
                                    "C": options[2],
                                    "D": options[3]
                                },
                                "correct": "A",
                                "explanation": f"Based on: {sentence[:100]}...",
                                "source": "fast_pattern",
                                "confidence": 0.8
                            })
                            break
        
        return questions
    
    def _generate_fast_t5_questions(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate questions using T5 with speed optimizations"""
        questions = []
        
        # Select best sentences for T5 generation
        best_sentences = analysis["factual_statements"][:num_questions]
        
        for sentence in best_sentences:
            if len(questions) >= num_questions:
                break
            
            try:
                # Simple, fast prompt
                prompt = f"question: {sentence}"
                
                # Fast tokenization
                inputs = self.question_tokenizer.encode(
                    prompt, 
                    return_tensors="pt", 
                    max_length=256,  # Reduced from 512
                    truncation=True
                )
                
                if torch.cuda.is_available():
                    inputs = inputs.cuda()
                
                # Fast generation with reduced parameters
                with torch.no_grad():
                    outputs = self.question_generator.generate(
                        inputs,
                        max_length=32,  # Reduced from 128
                        num_beams=2,    # Reduced from 5
                        early_stopping=True,
                        do_sample=False  # Faster than sampling
                    )
                
                question_text = self.question_tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                if self._is_valid_question_fast(question_text):
                    # Fast answer extraction
                    answer = self._extract_answer_fast(sentence, question_text)
                    
                    if answer:
                        # Fast distractor generation
                        options = self._generate_fast_distractors(answer, sentence, text)
                        
                        if len(options) >= 4:
                            questions.append({
                                "question": question_text,
                                "options": {
                                    "A": options[0],
                                    "B": options[1],
                                    "C": options[2],
                                    "D": options[3]
                                },
                                "correct": "A",
                                "explanation": f"From: {sentence[:80]}...",
                                "source": "fast_t5",
                                "confidence": 0.7
                            })
                
            except Exception as e:
                print(f"T5 generation error: {e}")
                continue
        
        return questions
    
    def _is_valid_question_fast(self, question_text: str) -> bool:
        """Fast question validation"""
        if not question_text or len(question_text.strip()) < 8:
            return False
        
        question_text = question_text.strip()
        
        # Must end with question mark
        if not question_text.endswith('?'):
            return False
        
        # Reasonable length
        words = question_text.split()
        if not (3 <= len(words) <= 20):
            return False
        
        return True
    
    def _extract_answer_fast(self, sentence: str, question: str) -> Optional[str]:
        """Fast answer extraction"""
        # Simple entity extraction from sentence
        doc = self.nlp(sentence)
        entities = [ent.text for ent in doc.ents if len(ent.text) > 2]
        
        # Return first reasonable entity
        for entity in entities:
            if len(entity) > 2 and len(entity) < 50:
                return entity
        
        # Fallback: extract key terms
        key_terms = re.findall(r'\b[A-Z][a-z]+\b', sentence)
        if key_terms:
            return key_terms[0]
        
        return None
    
    def _generate_fast_distractors(self, correct_answer: str, context: str, full_text: str) -> List[str]:
        """Generate distractors quickly"""
        distractors = [correct_answer]
        
        # Strategy 1: Extract similar entities from text
        doc = self.nlp(full_text[:500])  # Limit for speed
        entities = [ent.text for ent in doc.ents if ent.text != correct_answer and len(ent.text) > 2]
        
        # Add similar entities
        for entity in entities[:3]:
            if entity.lower() != correct_answer.lower():
                distractors.append(entity)
        
        # Strategy 2: Generate variations
        if len(distractors) < 4:
            variations = self._generate_answer_variations(correct_answer)
            distractors.extend(variations)
        
        # Strategy 3: Use fallbacks
        if len(distractors) < 4:
            fallbacks = self._get_fast_fallbacks(correct_answer)
            distractors.extend(fallbacks)
        
        # Ensure exactly 4 unique options
        unique_distractors = []
        seen = set()
        for d in distractors:
            if d.lower() not in seen and len(d.strip()) > 1:
                unique_distractors.append(d.strip())
                seen.add(d.lower())
        
        return unique_distractors[:4]
    
    def _generate_answer_variations(self, answer: str) -> List[str]:
        """Generate quick answer variations"""
        variations = []
        
        # For years
        if re.match(r'\d{4}', answer):
            year = int(answer)
            variations.extend([str(year-1), str(year+1), str(year-5)])
        
        # For names/terms
        elif len(answer.split()) == 1:
            variations.extend([
                answer + "s",
                "Non-" + answer,
                answer.upper() if answer.islower() else answer.lower()
            ])
        
        return variations[:3]
    
    def _get_fast_fallbacks(self, answer: str) -> List[str]:
        """Get fast fallback distractors"""
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ['programming', 'language', 'code']):
            return ['Java', 'C++', 'JavaScript']
        elif any(word in answer_lower for word in ['company', 'corporation']):
            return ['Microsoft', 'Google', 'Apple']
        elif re.match(r'\d{4}', answer):
            year = int(re.findall(r'\d{4}', answer)[0])
            return [str(year-1), str(year+1), str(year+10)]
        else:
            return ['System', 'Framework', 'Method']
    
    def _fast_quality_filter(self, questions: List[Dict], target_count: int) -> List[Dict]:
        """Fast quality filtering"""
        # Simple quality scoring
        scored_questions = []
        
        for q in questions:
            score = 0
            
            # Question format (0.4)
            if q.get("question", "").endswith('?'):
                score += 0.4
            
            # Options quality (0.3)
            options = q.get("options", {})
            if len(options) == 4 and len(set(options.values())) == 4:
                score += 0.3
            
            # Answer quality (0.3)
            correct_option = options.get(q.get("correct", "A"), "")
            if len(correct_option) > 2:
                score += 0.3
            
            if score >= 0.6:  # Minimum threshold
                scored_questions.append((q, score))
        
        # Sort by score and return top questions
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        return [q for q, score in scored_questions[:target_count]]
    
    def _quick_polish(self, question: Dict):
        """Quick question polishing"""
        # Shuffle options
        options = question.get("options", {})
        if options:
            option_values = list(options.values())
            correct_answer = option_values[0]
            
            random.shuffle(option_values)
            new_correct_index = option_values.index(correct_answer)
            new_correct_letter = ["A", "B", "C", "D"][new_correct_index]
            
            question["options"] = {
                "A": option_values[0],
                "B": option_values[1],
                "C": option_values[2],
                "D": option_values[3]
            }
            question["correct"] = new_correct_letter


# Main interface function
def generate_fast_mcq_questions(text: str, num_questions: int = 10, 
                               difficulty: str = "medium") -> List[Dict]:
    """
    Generate MCQ questions quickly with good quality
    
    Args:
        text (str): Input text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)
        
    Returns:
        List[Dict]: List of MCQ questions generated quickly
    """
    try:
        generator = FastMCQGenerator()
        return generator.generate_fast_questions(text, num_questions, difficulty)
    except Exception as e:
        print(f"Error in fast MCQ generation: {e}")
        return []


def is_fast_mode_available() -> bool:
    """Check if fast mode dependencies are available"""
    return FAST_DEPENDENCIES_AVAILABLE
