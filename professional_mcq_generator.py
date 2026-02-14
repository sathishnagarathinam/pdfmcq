"""
Professional MCQ Generator using state-of-the-art models
Generates high-quality, professional-grade multiple choice questions
"""

import os
import re
import json
import random
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import (
        AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM,
        T5ForConditionalGeneration, T5Tokenizer,
        pipeline, AutoModelForQuestionAnswering
    )
    from sentence_transformers import SentenceTransformer
    import spacy
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    PROFESSIONAL_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Professional dependencies not available: {e}")
    PROFESSIONAL_DEPENDENCIES_AVAILABLE = False

class ProfessionalMCQGenerator:
    """Professional-grade MCQ Generator using best available models"""
    
    def __init__(self, config_manager=None):
        try:
            from offline_config import get_model_manager
            self.config_manager = config_manager or get_model_manager()
        except ImportError:
            self.config_manager = None
            print("Warning: Using default configuration")
        
        self.model_cache_dir = self.config_manager.cache_dir if self.config_manager else "./models"
        self.models_loaded = False
        
        # Professional models
        self.question_generator = None
        self.question_tokenizer = None
        self.answer_generator = None
        self.answer_tokenizer = None
        self.sentence_model = None
        self.qa_pipeline = None
        self.nlp = None
        
        # Ensure cache directory exists
        os.makedirs(self.model_cache_dir, exist_ok=True)
        
        # Download NLTK data if needed
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.download('punkt_tab', quiet=True)
            except:
                nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    
    def load_professional_models(self):
        """Load professional-grade models for high-quality MCQ generation"""
        if not PROFESSIONAL_DEPENDENCIES_AVAILABLE:
            raise ImportError("Professional dependencies not available")
        
        print("🚀 Loading professional-grade models for MCQ generation...")
        
        try:
            # 1. Load FLAN-T5 Large for question generation
            print("📚 Loading Google FLAN-T5 Large for question generation...")
            qg_model_name = "google/flan-t5-large"
            self.question_tokenizer = T5Tokenizer.from_pretrained(
                qg_model_name, 
                cache_dir=os.path.join(self.model_cache_dir, "question_generation")
            )
            self.question_generator = T5ForConditionalGeneration.from_pretrained(
                qg_model_name,
                cache_dir=os.path.join(self.model_cache_dir, "question_generation"),
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # 2. Load best sentence transformer
            print("🔍 Loading sentence transformer for semantic analysis...")
            self.sentence_model = SentenceTransformer(
                'sentence-transformers/all-mpnet-base-v2',
                cache_folder=os.path.join(self.model_cache_dir, "sentence_transformer")
            )
            
            # 3. Load QA model for answer validation
            print("🎯 Loading RoBERTa QA model for answer validation...")
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                tokenizer="deepset/roberta-base-squad2",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # 4. Load spaCy large model
            print("🧠 Loading spaCy large model...")
            try:
                self.nlp = spacy.load("en_core_web_lg")
            except OSError:
                print("⚠️ spaCy large model not found, trying medium...")
                try:
                    self.nlp = spacy.load("en_core_web_md")
                except OSError:
                    print("⚠️ spaCy medium model not found, using small...")
                    self.nlp = spacy.load("en_core_web_sm")
            
            # 5. Load text generation model for distractors
            print("💭 Loading text generation model for distractors...")
            try:
                self.answer_tokenizer = AutoTokenizer.from_pretrained(
                    "microsoft/DialoGPT-medium",
                    cache_dir=os.path.join(self.model_cache_dir, "answer_generation")
                )
                self.answer_generator = AutoModelForCausalLM.from_pretrained(
                    "microsoft/DialoGPT-medium",
                    cache_dir=os.path.join(self.model_cache_dir, "answer_generation"),
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
            except Exception as e:
                print(f"⚠️ Could not load answer generation model: {e}")
                self.answer_generator = None
                self.answer_tokenizer = None
            
            self.models_loaded = True
            print("✅ All professional models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading professional models: {e}")
            self.models_loaded = False
            raise
    
    def generate_professional_questions(self, text: str, num_questions: int = 10, 
                                      difficulty: str = "medium") -> List[Dict]:
        """Generate professional-quality MCQ questions"""
        if not self.models_loaded:
            self.load_professional_models()
        
        if not text.strip():
            return []
        
        print(f"🎯 Generating {num_questions} professional MCQ questions...")
        
        # Step 1: Advanced text analysis
        analysis = self._advanced_text_analysis(text)
        
        # Step 2: Generate questions using multiple professional strategies
        all_questions = []
        
        # Strategy 1: FLAN-T5 based generation (50%)
        flan_count = max(1, int(num_questions * 0.5))
        flan_questions = self._generate_with_flan_t5(text, analysis, flan_count * 2)
        all_questions.extend(flan_questions)
        
        # Strategy 2: Educational QA based generation (30%)
        qa_count = max(1, int(num_questions * 0.3))
        qa_questions = self._generate_with_qa_model(text, analysis, qa_count * 2)
        all_questions.extend(qa_questions)
        
        # Strategy 3: Semantic similarity based generation (20%)
        semantic_count = max(1, int(num_questions * 0.2))
        semantic_questions = self._generate_semantic_questions(text, analysis, semantic_count * 2)
        all_questions.extend(semantic_questions)
        
        # Step 3: Professional quality filtering and ranking
        professional_questions = self._apply_professional_quality_filter(all_questions, text)
        
        # Step 4: Select best questions
        final_questions = self._select_best_questions(professional_questions, num_questions)
        
        # Step 5: Apply difficulty and final polish
        for question in final_questions:
            question["difficulty"] = difficulty
            question = self._polish_question(question)
        
        print(f"✅ Generated {len(final_questions)} professional questions")
        return final_questions
    
    def _advanced_text_analysis(self, text: str) -> Dict:
        """Advanced text analysis using professional models"""
        print("🔍 Performing advanced text analysis...")
        
        # Basic analysis
        sentences = sent_tokenize(text)
        
        # NLP analysis with spaCy
        doc = self.nlp(text)
        
        # Extract entities
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Extract key phrases using noun chunks
        key_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 4]
        
        # Semantic analysis with sentence transformer
        sentence_embeddings = self.sentence_model.encode(sentences)
        
        # Find most important sentences using centrality
        similarity_matrix = cosine_similarity(sentence_embeddings)
        centrality_scores = np.mean(similarity_matrix, axis=1)
        important_sentences = [sentences[i] for i in np.argsort(centrality_scores)[-10:]]
        
        # Extract factual statements
        factual_statements = self._extract_factual_statements(sentences)
        
        # Extract definitions
        definitions = self._extract_definitions(sentences)
        
        return {
            "sentences": sentences,
            "entities": entities,
            "key_phrases": key_phrases,
            "important_sentences": important_sentences,
            "factual_statements": factual_statements,
            "definitions": definitions,
            "sentence_embeddings": sentence_embeddings
        }
    
    def _extract_factual_statements(self, sentences: List[str]) -> List[str]:
        """Extract factual statements suitable for questions"""
        factual_patterns = [
            r'\b(?:is|are|was|were)\s+(?:a|an|the)?\s*[^.]{10,}',
            r'\b(?:created|developed|invented|founded|established)\s+(?:by|in)\s+[^.]{5,}',
            r'\b(?:features?|includes?|contains?|supports?)\s+[^.]{10,}',
            r'\b(?:used for|designed to|helps to|enables)\s+[^.]{10,}',
            r'\b\d{4}\b.*(?:created|developed|invented|founded)',
            r'\b(?:first|second|third|primary|main|key)\s+[^.]{10,}'
        ]
        
        factual_statements = []
        for sentence in sentences:
            if len(sentence.split()) >= 8:  # Minimum length
                for pattern in factual_patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        factual_statements.append(sentence)
                        break
        
        return factual_statements
    
    def _extract_definitions(self, sentences: List[str]) -> List[Dict]:
        """Extract definitions from text"""
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an|the)?\s*([^.]{15,})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+refers to\s+([^.]{15,})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+means\s+([^.]{15,})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+can be defined as\s+([^.]{15,})'
        ]
        
        definitions = []
        for sentence in sentences:
            for pattern in definition_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    term = match.group(1).strip()
                    definition = match.group(2).strip()
                    definitions.append({
                        "term": term,
                        "definition": definition,
                        "sentence": sentence
                    })
        
        return definitions

    def _generate_with_flan_t5(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate questions using Google FLAN-T5 Large model"""
        print("📚 Generating questions with FLAN-T5 Large...")

        questions = []

        # Use important sentences and factual statements
        source_sentences = analysis["important_sentences"] + analysis["factual_statements"]
        source_sentences = list(set(source_sentences))  # Remove duplicates

        for sentence in source_sentences[:num_questions]:
            try:
                # Multiple prompting strategies for FLAN-T5
                prompts = [
                    f"Generate a multiple choice question based on this text: {sentence}",
                    f"Create an educational question about: {sentence}",
                    f"What question can be asked about: {sentence}",
                    f"Generate a quiz question from: {sentence}"
                ]

                for prompt in prompts:
                    if len(questions) >= num_questions:
                        break

                    # Generate question with FLAN-T5
                    inputs = self.question_tokenizer.encode(
                        prompt,
                        return_tensors="pt",
                        max_length=512,
                        truncation=True
                    )

                    with torch.no_grad():
                        outputs = self.question_generator.generate(
                            inputs,
                            max_length=128,
                            num_beams=5,
                            early_stopping=True,
                            temperature=0.7,
                            do_sample=True,
                            top_p=0.9
                        )

                    question_text = self.question_tokenizer.decode(outputs[0], skip_special_tokens=True)

                    if self._is_valid_question(question_text):
                        # Generate answer using QA model
                        answer = self._extract_answer_with_qa_model(question_text, sentence)

                        if answer:
                            # Generate professional distractors
                            options = self._generate_professional_distractors(answer, sentence, text)

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
                                    "explanation": f"Based on the text: {sentence}",
                                    "source": "flan_t5_large",
                                    "confidence": 0.9
                                })

            except Exception as e:
                print(f"Error with FLAN-T5 generation: {e}")
                continue

        return questions

    def _generate_with_qa_model(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate questions using educational QA model"""
        print("🎯 Generating questions with educational QA model...")

        questions = []

        # Generate questions from definitions
        for definition in analysis["definitions"][:num_questions]:
            try:
                term = definition["term"]
                definition_text = definition["definition"]

                # Create definition question
                question_text = f"What is {term}?"

                # Validate answer with QA model
                qa_result = self.qa_pipeline(
                    question=question_text,
                    context=definition["sentence"]
                )

                if qa_result["score"] > 0.5:  # High confidence
                    # Generate professional distractors
                    options = self._generate_professional_distractors(
                        definition_text,
                        definition["sentence"],
                        text
                    )

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
                            "explanation": f"{term} is defined as {definition_text}",
                            "source": "educational_qa",
                            "confidence": qa_result["score"]
                        })

            except Exception as e:
                print(f"Error with QA model generation: {e}")
                continue

        return questions

    def _generate_semantic_questions(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate questions using semantic similarity"""
        print("🔍 Generating semantic similarity questions...")

        questions = []

        # Use entities for relationship questions
        entities = [ent[0] for ent in analysis["entities"] if ent[1] in ["PERSON", "ORG", "PRODUCT", "EVENT"]]

        for entity in entities[:num_questions]:
            try:
                # Find sentences containing this entity
                entity_sentences = [s for s in analysis["sentences"] if entity.lower() in s.lower()]

                if entity_sentences:
                    context = entity_sentences[0]

                    # Generate relationship question
                    question_text = f"What is {entity} associated with in the given context?"

                    # Find related entities using semantic similarity
                    related_entities = self._find_related_entities(entity, analysis, text)

                    if len(related_entities) >= 3:
                        # Create options with the most related entity as correct answer
                        correct_answer = related_entities[0]
                        distractors = related_entities[1:4]

                        options = [correct_answer] + distractors
                        random.shuffle(options)

                        correct_index = options.index(correct_answer)
                        correct_letter = ["A", "B", "C", "D"][correct_index]

                        questions.append({
                            "question": question_text,
                            "options": {
                                "A": options[0],
                                "B": options[1],
                                "C": options[2],
                                "D": options[3]
                            },
                            "correct": correct_letter,
                            "explanation": f"In the context, {entity} is most closely associated with {correct_answer}",
                            "source": "semantic_similarity",
                            "confidence": 0.8
                        })

            except Exception as e:
                print(f"Error with semantic generation: {e}")
                continue

        return questions

    def _is_valid_question(self, question_text: str) -> bool:
        """Validate if generated text is a proper question"""
        if not question_text or len(question_text.strip()) < 10:
            return False

        question_text = question_text.strip()

        # Must end with question mark
        if not question_text.endswith('?'):
            return False

        # Must start with question word or be reasonable length
        question_words = ['what', 'who', 'when', 'where', 'why', 'how', 'which', 'is', 'are', 'was', 'were', 'do', 'does', 'did', 'can', 'could', 'will', 'would']
        first_word = question_text.split()[0].lower()

        if first_word not in question_words and len(question_text.split()) < 6:
            return False

        # Reasonable length
        if not (5 <= len(question_text.split()) <= 30):
            return False

        return True

    def _extract_answer_with_qa_model(self, question: str, context: str) -> Optional[str]:
        """Extract answer using professional QA model"""
        try:
            result = self.qa_pipeline(question=question, context=context)

            if result["score"] > 0.3:  # Minimum confidence
                answer = result["answer"].strip()
                if len(answer) > 2 and len(answer) < 100:
                    return answer
        except Exception as e:
            print(f"Error extracting answer: {e}")

        return None

    def _generate_professional_distractors(self, correct_answer: str, context: str, full_text: str) -> List[str]:
        """Generate professional-quality distractors"""
        distractors = [correct_answer]

        # Strategy 1: Use named entities from text
        doc = self.nlp(full_text)
        entities = [ent.text for ent in doc.ents if ent.text != correct_answer]

        # Strategy 2: Use semantic similarity
        if len(entities) > 0:
            # Get embeddings for correct answer and entities
            answer_embedding = self.sentence_model.encode([correct_answer])
            entity_embeddings = self.sentence_model.encode(entities)

            # Find semantically similar but different entities
            similarities = cosine_similarity(answer_embedding, entity_embeddings)[0]
            similar_indices = np.argsort(similarities)[::-1]

            for idx in similar_indices:
                if len(distractors) >= 4:
                    break
                entity = entities[idx]
                if (entity.lower() != correct_answer.lower() and
                    len(entity) > 2 and len(entity) < 50):
                    distractors.append(entity)

        # Strategy 3: Generate contextual alternatives
        if len(distractors) < 4:
            contextual_alternatives = self._generate_contextual_alternatives(correct_answer, context)
            distractors.extend(contextual_alternatives)

        # Strategy 4: Use professional fallbacks
        if len(distractors) < 4:
            professional_fallbacks = self._get_professional_fallbacks(correct_answer)
            distractors.extend(professional_fallbacks)

        # Ensure exactly 4 unique options
        unique_distractors = []
        seen = set()
        for d in distractors:
            if d.lower() not in seen and len(d.strip()) > 1:
                unique_distractors.append(d.strip())
                seen.add(d.lower())

        return unique_distractors[:4]

    def _generate_contextual_alternatives(self, correct_answer: str, context: str) -> List[str]:
        """Generate contextual alternatives using text analysis"""
        alternatives = []

        # Extract similar terms from context
        doc = self.nlp(context)

        # Get words with similar POS tags
        correct_doc = self.nlp(correct_answer)
        if correct_doc:
            correct_pos = correct_doc[0].pos_
            similar_words = [token.text for token in doc if token.pos_ == correct_pos and token.text != correct_answer]
            alternatives.extend(similar_words[:3])

        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks if chunk.text != correct_answer]
        alternatives.extend(noun_phrases[:2])

        return alternatives

    def _get_professional_fallbacks(self, correct_answer: str) -> List[str]:
        """Get professional fallback distractors based on answer type"""
        fallbacks = []

        answer_lower = correct_answer.lower()

        # Technology/Programming
        if any(word in answer_lower for word in ['programming', 'language', 'software', 'code']):
            fallbacks.extend(['Java', 'C++', 'JavaScript', 'Ruby', 'Go', 'Swift'])

        # Companies/Organizations
        elif any(word in answer_lower for word in ['company', 'corporation', 'organization']):
            fallbacks.extend(['Microsoft', 'Google', 'Apple', 'Amazon', 'IBM', 'Oracle'])

        # Years/Dates
        elif re.match(r'\d{4}', correct_answer):
            year = int(re.findall(r'\d{4}', correct_answer)[0])
            fallbacks.extend([str(year-1), str(year+1), str(year-5), str(year+5)])

        # People/Names
        elif any(word in answer_lower for word in ['person', 'founder', 'creator', 'inventor']):
            fallbacks.extend(['John Smith', 'Jane Doe', 'Robert Johnson', 'Mary Williams'])

        # Concepts/Methods
        elif any(word in answer_lower for word in ['method', 'approach', 'technique', 'process']):
            fallbacks.extend(['supervised learning', 'unsupervised learning', 'reinforcement learning', 'deep learning'])

        # Generic professional terms
        else:
            fallbacks.extend(['system', 'framework', 'methodology', 'protocol', 'standard', 'specification'])

        return [f for f in fallbacks if f.lower() != correct_answer.lower()][:3]

    def _find_related_entities(self, entity: str, analysis: Dict, text: str) -> List[str]:
        """Find entities related to the given entity using semantic similarity"""
        related = []

        # Get all entities except the target
        other_entities = [ent[0] for ent in analysis["entities"] if ent[0].lower() != entity.lower()]

        if other_entities and len(other_entities) > 0:
            # Use sentence transformer to find semantic similarity
            entity_embedding = self.sentence_model.encode([entity])
            other_embeddings = self.sentence_model.encode(other_entities)

            similarities = cosine_similarity(entity_embedding, other_embeddings)[0]
            sorted_indices = np.argsort(similarities)[::-1]

            related = [other_entities[i] for i in sorted_indices[:5]]

        return related

    def _apply_professional_quality_filter(self, questions: List[Dict], text: str) -> List[Dict]:
        """Apply professional quality filtering"""
        print("🔍 Applying professional quality filters...")

        professional_questions = []

        for question in questions:
            score = self._calculate_professional_score(question, text)

            if score >= 0.7:  # High professional standard
                question["professional_score"] = score
                professional_questions.append(question)

        return professional_questions

    def _calculate_professional_score(self, question: Dict, text: str) -> float:
        """Calculate professional quality score"""
        score = 0.0

        # Question quality (30%)
        question_text = question.get("question", "")
        if self._is_valid_question(question_text):
            score += 0.3

        # Options quality (25%)
        options = question.get("options", {})
        if len(options) == 4 and len(set(options.values())) == 4:
            score += 0.15

            # Check option balance
            lengths = [len(opt.split()) for opt in options.values()]
            if max(lengths) - min(lengths) <= 3:
                score += 0.1

        # Answer accuracy (25%)
        if question.get("confidence", 0) > 0.5:
            score += 0.25

        # Explanation quality (10%)
        explanation = question.get("explanation", "")
        if len(explanation) > 20 and "based on" in explanation.lower():
            score += 0.1

        # Source reliability (10%)
        source = question.get("source", "")
        if source in ["flan_t5_large", "educational_qa"]:
            score += 0.1
        elif source == "semantic_similarity":
            score += 0.05

        return min(score, 1.0)

    def _select_best_questions(self, questions: List[Dict], num_questions: int) -> List[Dict]:
        """Select the best questions based on professional scores"""
        if len(questions) <= num_questions:
            return questions

        # Sort by professional score
        questions.sort(key=lambda x: x.get("professional_score", 0), reverse=True)

        # Select top questions ensuring diversity
        selected = []
        used_sources = set()

        for question in questions:
            if len(selected) >= num_questions:
                break

            source = question.get("source", "")

            # Ensure diversity of sources
            if len(selected) < num_questions // 2 or source not in used_sources:
                selected.append(question)
                used_sources.add(source)

        # Fill remaining slots with highest scoring questions
        for question in questions:
            if len(selected) >= num_questions:
                break
            if question not in selected:
                selected.append(question)

        return selected[:num_questions]

    def _polish_question(self, question: Dict) -> Dict:
        """Apply final polish to question"""
        # Ensure proper capitalization
        question_text = question.get("question", "")
        if question_text:
            question["question"] = question_text[0].upper() + question_text[1:]

        # Shuffle options
        options = question.get("options", {})
        if options:
            option_values = list(options.values())
            correct_answer = option_values[0]  # Assuming A is correct initially

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

        return question


# Main interface function
def generate_professional_mcq_questions(text: str, num_questions: int = 10,
                                       difficulty: str = "medium") -> List[Dict]:
    """
    Generate professional-quality MCQ questions using state-of-the-art models

    Args:
        text (str): Input text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)

    Returns:
        List[Dict]: List of professional-quality MCQ questions
    """
    try:
        generator = ProfessionalMCQGenerator()
        return generator.generate_professional_questions(text, num_questions, difficulty)
    except Exception as e:
        print(f"Error in professional MCQ generation: {e}")
        return []


def is_professional_mode_available() -> bool:
    """Check if professional mode dependencies are available"""
    return PROFESSIONAL_DEPENDENCIES_AVAILABLE
