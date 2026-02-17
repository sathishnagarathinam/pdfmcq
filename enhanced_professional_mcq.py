"""
Enhanced Professional MCQ Generator
Generates truly professional-quality questions suitable for academic and certification use
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
        AutoTokenizer, AutoModelForSeq2SeqLM, 
        T5ForConditionalGeneration, T5Tokenizer,
        pipeline
    )
    from sentence_transformers import SentenceTransformer
    import spacy
    import nltk
    from nltk.tokenize import sent_tokenize
    import numpy as np
    ENHANCED_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Enhanced dependencies not available: {e}")
    ENHANCED_DEPENDENCIES_AVAILABLE = False

class EnhancedProfessionalMCQGenerator:
    """Enhanced Professional MCQ Generator for truly professional questions"""
    
    def __init__(self):
        self.models_loaded = False
        self.model_cache_dir = "./enhanced_models"
        
        # Professional models
        self.question_generator = None
        self.question_tokenizer = None
        self.sentence_model = None
        self.nlp = None
        
        os.makedirs(self.model_cache_dir, exist_ok=True)
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        """Download NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.download('punkt_tab', quiet=True)
            except:
                nltk.download('punkt', quiet=True)
    
    def load_enhanced_models(self):
        """Load enhanced models for professional quality"""
        if not ENHANCED_DEPENDENCIES_AVAILABLE:
            raise ImportError("Enhanced dependencies not available")
        
        print("🎯 Loading enhanced professional models...")
        
        try:
            # Use T5-Large for better quality (compromise between speed and quality)
            print("📚 Loading T5-Large for professional question generation...")
            model_name = "t5-large"  # Better than base, faster than FLAN-T5-Large
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
            
            # Load good sentence transformer
            print("🔍 Loading sentence transformer...")
            self.sentence_model = SentenceTransformer(
                'all-mpnet-base-v2',  # Better quality than MiniLM
                cache_folder=os.path.join(self.model_cache_dir, "sentence_transformer")
            )
            
            # Load spaCy medium model (good balance)
            print("🧠 Loading spaCy medium model...")
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                except OSError:
                    print("⚠️ Downloading spaCy model...")
                    os.system("python -m spacy download en_core_web_sm")
                    self.nlp = spacy.load("en_core_web_sm")
            
            self.models_loaded = True
            print("✅ Enhanced models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading enhanced models: {e}")
            self.models_loaded = False
            raise
    
    def generate_professional_questions(self, text: str, num_questions: int = 10, 
                                      difficulty: str = "medium") -> List[Dict]:
        """Generate truly professional-quality MCQ questions"""
        if not self.models_loaded:
            self.load_enhanced_models()
        
        if not text.strip():
            return []
        
        print(f"🎯 Generating {num_questions} professional MCQ questions...")
        
        # Step 1: Advanced text analysis
        analysis = self._professional_text_analysis(text)
        
        # Step 2: Generate questions using professional strategies
        all_questions = []
        
        # Strategy 1: Definition-based questions (30%)
        definition_count = max(1, int(num_questions * 0.3))
        definition_questions = self._generate_definition_questions(analysis, definition_count)
        all_questions.extend(definition_questions)
        
        # Strategy 2: Concept-based questions (40%)
        concept_count = max(1, int(num_questions * 0.4))
        concept_questions = self._generate_concept_questions(text, analysis, concept_count)
        all_questions.extend(concept_questions)
        
        # Strategy 3: Application-based questions (30%)
        application_count = max(1, int(num_questions * 0.3))
        application_questions = self._generate_application_questions(text, analysis, application_count)
        all_questions.extend(application_questions)
        
        # Step 3: Professional quality enhancement
        enhanced_questions = self._enhance_question_quality(all_questions, text)
        
        # Step 4: Select best questions
        final_questions = self._select_professional_questions(enhanced_questions, num_questions)
        
        # Step 5: Apply difficulty and final professional polish
        for question in final_questions:
            question["difficulty"] = difficulty
            self._apply_professional_polish(question, difficulty)
        
        print(f"✅ Generated {len(final_questions)} professional questions")
        return final_questions
    
    def _professional_text_analysis(self, text: str) -> Dict:
        """Professional-grade text analysis"""
        print("🔍 Performing professional text analysis...")
        
        # Basic analysis
        sentences = sent_tokenize(text)
        
        # Advanced NLP analysis
        doc = self.nlp(text)
        
        # Extract high-quality entities
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "PRODUCT", "EVENT", "LAW", "LANGUAGE", "WORK_OF_ART"]:
                entities.append((ent.text, ent.label_))
        
        # Extract professional definitions
        definitions = self._extract_professional_definitions(sentences)
        
        # Extract key concepts
        key_concepts = self._extract_key_concepts(text, doc)
        
        # Extract relationships
        relationships = self._extract_relationships(sentences)
        
        # Extract processes and procedures
        processes = self._extract_processes(sentences)
        
        return {
            "sentences": sentences,
            "entities": entities,
            "definitions": definitions,
            "key_concepts": key_concepts,
            "relationships": relationships,
            "processes": processes
        }
    
    def _extract_professional_definitions(self, sentences: List[str]) -> List[Dict]:
        """Extract professional-quality definitions"""
        definitions = []
        
        # Enhanced definition patterns
        definition_patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s+is\s+(?:a|an|the)?\s*([^.]{20,150})',
            r'([A-Z][a-zA-Z\s]+?)\s+refers to\s+([^.]{20,150})',
            r'([A-Z][a-zA-Z\s]+?)\s+can be defined as\s+([^.]{20,150})',
            r'([A-Z][a-zA-Z\s]+?)\s+means\s+([^.]{20,150})',
            r'The term\s+([A-Z][a-zA-Z\s]+?)\s+describes\s+([^.]{20,150})',
            r'([A-Z][a-zA-Z\s]+?)\s+represents\s+([^.]{20,150})'
        ]
        
        for sentence in sentences:
            if len(sentence.split()) >= 10:  # Ensure substantial content
                for pattern in definition_patterns:
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    if match:
                        term = match.group(1).strip()
                        definition = match.group(2).strip()
                        
                        # Quality filters
                        if (len(term.split()) <= 5 and 
                            len(definition.split()) >= 5 and
                            not any(word in definition.lower() for word in ['this', 'that', 'it', 'they'])):
                            
                            definitions.append({
                                "term": term,
                                "definition": definition,
                                "sentence": sentence,
                                "quality_score": self._calculate_definition_quality(term, definition)
                            })
        
        # Sort by quality and return best
        definitions.sort(key=lambda x: x["quality_score"], reverse=True)
        return definitions[:10]
    
    def _extract_key_concepts(self, text: str, doc) -> List[str]:
        """Extract key concepts from text"""
        concepts = []
        
        # Extract noun phrases that are likely concepts
        for chunk in doc.noun_chunks:
            if (len(chunk.text.split()) <= 4 and 
                len(chunk.text) > 3 and
                chunk.root.pos_ == "NOUN"):
                concepts.append(chunk.text)
        
        # Extract capitalized terms (likely important concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend(capitalized)
        
        # Remove duplicates and filter
        unique_concepts = list(set(concepts))
        return [c for c in unique_concepts if len(c) > 3 and len(c) < 50][:15]
    
    def _extract_relationships(self, sentences: List[str]) -> List[Dict]:
        """Extract relationships between concepts"""
        relationships = []
        
        relationship_patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s+(?:is a type of|is a kind of|is a subset of)\s+([^.]{5,50})',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:includes|contains|comprises)\s+([^.]{5,50})',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:leads to|results in|causes)\s+([^.]{5,50})',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:is used for|is designed for)\s+([^.]{5,50})'
        ]
        
        for sentence in sentences:
            for pattern in relationship_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    subject = match.group(1).strip()
                    object_rel = match.group(2).strip()
                    relationships.append({
                        "subject": subject,
                        "object": object_rel,
                        "sentence": sentence
                    })
        
        return relationships[:8]
    
    def _extract_processes(self, sentences: List[str]) -> List[Dict]:
        """Extract processes and procedures"""
        processes = []
        
        process_patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s+(?:involves|requires|consists of)\s+([^.]{10,100})',
            r'(?:The process of|The method of)\s+([A-Z][a-zA-Z\s]+?)\s+([^.]{10,100})',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:works by|operates by)\s+([^.]{10,100})'
        ]
        
        for sentence in sentences:
            for pattern in process_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    process_name = match.group(1).strip()
                    process_description = match.group(2).strip()
                    processes.append({
                        "name": process_name,
                        "description": process_description,
                        "sentence": sentence
                    })
        
        return processes[:5]
    
    def _calculate_definition_quality(self, term: str, definition: str) -> float:
        """Calculate quality score for a definition"""
        score = 0.0
        
        # Length appropriateness
        if 20 <= len(definition) <= 150:
            score += 0.3
        
        # Term specificity
        if len(term.split()) <= 3:
            score += 0.2
        
        # Definition completeness
        if any(word in definition.lower() for word in ['that', 'which', 'involving', 'including']):
            score += 0.2
        
        # Technical vocabulary
        if any(word in definition.lower() for word in ['system', 'method', 'process', 'technique', 'approach']):
            score += 0.2
        
        # Avoid vague terms
        if not any(word in definition.lower() for word in ['thing', 'stuff', 'something', 'anything']):
            score += 0.1
        
        return score
    
    def _generate_definition_questions(self, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate professional definition questions"""
        questions = []
        
        for definition in analysis["definitions"][:num_questions]:
            term = definition["term"]
            definition_text = definition["definition"]
            
            # Create professional definition question
            question_templates = [
                f"What is {term}?",
                f"How is {term} best defined?",
                f"Which of the following best describes {term}?",
                f"What does the term '{term}' refer to?"
            ]
            
            question_text = random.choice(question_templates)
            
            # Generate professional distractors
            options = self._generate_professional_distractors_for_definition(
                definition_text, term, analysis
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
                    "source": "professional_definition",
                    "confidence": definition["quality_score"],
                    "type": "definition"
                })
        
        return questions
    
    def _generate_concept_questions(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate professional concept-based questions"""
        questions = []
        
        # Use T5 for concept questions
        for concept in analysis["key_concepts"][:num_questions * 2]:
            if len(questions) >= num_questions:
                break
            
            try:
                # Professional prompts for T5
                prompts = [
                    f"Generate a professional question about {concept}: {text[:200]}",
                    f"Create an academic question regarding {concept}: {text[:200]}",
                    f"What professional question can be asked about {concept}?"
                ]
                
                for prompt in prompts:
                    if len(questions) >= num_questions:
                        break
                    
                    # Generate with T5
                    inputs = self.question_tokenizer.encode(
                        prompt, 
                        return_tensors="pt", 
                        max_length=400, 
                        truncation=True
                    )
                    
                    if torch.cuda.is_available():
                        inputs = inputs.cuda()
                    
                    with torch.no_grad():
                        outputs = self.question_generator.generate(
                            inputs,
                            max_length=64,
                            num_beams=4,
                            early_stopping=True,
                            temperature=0.8,
                            do_sample=True,
                            top_p=0.9
                        )
                    
                    question_text = self.question_tokenizer.decode(outputs[0], skip_special_tokens=True)
                    
                    if self._is_professional_question(question_text):
                        # Extract answer from text
                        answer = self._extract_professional_answer(question_text, text, concept)
                        
                        if answer:
                            # Generate professional distractors
                            options = self._generate_professional_distractors_for_concept(
                                answer, concept, text, analysis
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
                                    "explanation": f"Based on the concept of {concept} in the given text.",
                                    "source": "professional_concept",
                                    "confidence": 0.8,
                                    "type": "concept"
                                })
                                break
                
            except Exception as e:
                print(f"Error generating concept question: {e}")
                continue
        
        return questions

    def _generate_application_questions(self, text: str, analysis: Dict, num_questions: int) -> List[Dict]:
        """Generate professional application-based questions"""
        questions = []

        # Use relationships and processes for application questions
        sources = analysis["relationships"] + analysis["processes"]

        for source in sources[:num_questions]:
            try:
                if "subject" in source:  # Relationship
                    subject = source["subject"]
                    obj = source["object"]

                    question_templates = [
                        f"In what context would {subject} be most appropriately applied?",
                        f"What is the primary application of {subject}?",
                        f"How is {subject} typically utilized?",
                        f"What is the main purpose of {subject}?"
                    ]

                    question_text = random.choice(question_templates)
                    correct_answer = obj

                elif "name" in source:  # Process
                    process_name = source["name"]
                    description = source["description"]

                    question_templates = [
                        f"What is the primary function of {process_name}?",
                        f"How does {process_name} operate?",
                        f"What is achieved through {process_name}?",
                        f"What is the main characteristic of {process_name}?"
                    ]

                    question_text = random.choice(question_templates)
                    correct_answer = description

                else:
                    continue

                # Generate professional distractors
                options = self._generate_professional_distractors_for_application(
                    correct_answer, text, analysis
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
                        "explanation": f"Based on the application and context described in the text.",
                        "source": "professional_application",
                        "confidence": 0.75,
                        "type": "application"
                    })

            except Exception as e:
                print(f"Error generating application question: {e}")
                continue

        return questions

    def _is_professional_question(self, question_text: str) -> bool:
        """Check if question meets professional standards"""
        if not question_text or len(question_text.strip()) < 15:
            return False

        question_text = question_text.strip()

        # Must end with question mark
        if not question_text.endswith('?'):
            return False

        # Professional question indicators
        professional_indicators = [
            'what', 'which', 'how', 'why', 'when', 'where',
            'define', 'describe', 'explain', 'identify',
            'primary', 'main', 'best', 'most appropriate'
        ]

        question_lower = question_text.lower()
        if not any(indicator in question_lower for indicator in professional_indicators):
            return False

        # Appropriate length
        words = question_text.split()
        if not (6 <= len(words) <= 25):
            return False

        # Avoid unprofessional terms
        unprofessional_terms = ['stuff', 'thing', 'whatever', 'kinda', 'sorta']
        if any(term in question_lower for term in unprofessional_terms):
            return False

        return True

    def _extract_professional_answer(self, question: str, text: str, concept: str) -> Optional[str]:
        """Extract professional-quality answer"""
        # Use spaCy to find relevant information
        doc = self.nlp(text)

        # Look for sentences containing the concept
        relevant_sentences = []
        for sent in doc.sents:
            if concept.lower() in sent.text.lower():
                relevant_sentences.append(sent.text)

        if not relevant_sentences:
            return None

        # Extract key information from relevant sentences
        for sentence in relevant_sentences:
            # Look for definitions or descriptions
            patterns = [
                rf'{re.escape(concept)}\s+is\s+([^.]+)',
                rf'{re.escape(concept)}\s+refers to\s+([^.]+)',
                rf'{re.escape(concept)}\s+means\s+([^.]+)',
                rf'{re.escape(concept)}\s+involves\s+([^.]+)'
            ]

            for pattern in patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    answer = match.group(1).strip()
                    if len(answer) > 5 and len(answer) < 100:
                        return answer

        # Fallback: return the concept itself if no better answer found
        return concept

    def _generate_professional_distractors_for_definition(self, correct_answer: str, term: str, analysis: Dict) -> List[str]:
        """Generate professional distractors for definition questions"""
        distractors = [correct_answer]

        # Strategy 1: Use other definitions from the text
        for definition in analysis["definitions"]:
            if (definition["term"].lower() != term.lower() and
                definition["definition"] != correct_answer):
                distractors.append(definition["definition"])

        # Strategy 2: Generate semantic variations
        if len(distractors) < 4:
            variations = self._generate_semantic_variations(correct_answer)
            distractors.extend(variations)

        # Strategy 3: Use professional fallbacks
        if len(distractors) < 4:
            fallbacks = self._get_professional_definition_fallbacks(term, correct_answer)
            distractors.extend(fallbacks)

        # Ensure exactly 4 unique options
        return self._ensure_unique_options(distractors)

    def _generate_professional_distractors_for_concept(self, correct_answer: str, concept: str, text: str, analysis: Dict) -> List[str]:
        """Generate professional distractors for concept questions"""
        distractors = [correct_answer]

        # Strategy 1: Use related concepts
        for other_concept in analysis["key_concepts"]:
            if other_concept.lower() != concept.lower():
                distractors.append(other_concept)

        # Strategy 2: Use entities
        for entity, label in analysis["entities"]:
            if entity.lower() != concept.lower() and entity != correct_answer:
                distractors.append(entity)

        # Strategy 3: Generate contextual alternatives
        if len(distractors) < 4:
            alternatives = self._generate_contextual_alternatives(correct_answer, text)
            distractors.extend(alternatives)

        return self._ensure_unique_options(distractors)

    def _generate_professional_distractors_for_application(self, correct_answer: str, text: str, analysis: Dict) -> List[str]:
        """Generate professional distractors for application questions"""
        distractors = [correct_answer]

        # Strategy 1: Use other applications/processes
        for process in analysis["processes"]:
            if process["description"] != correct_answer:
                distractors.append(process["description"])

        # Strategy 2: Use relationship objects
        for relationship in analysis["relationships"]:
            if relationship["object"] != correct_answer:
                distractors.append(relationship["object"])

        # Strategy 3: Generate professional alternatives
        if len(distractors) < 4:
            alternatives = self._generate_professional_alternatives(correct_answer)
            distractors.extend(alternatives)

        return self._ensure_unique_options(distractors)

    def _generate_semantic_variations(self, text: str) -> List[str]:
        """Generate semantic variations of text"""
        variations = []

        # Simple transformations
        if "method" in text.lower():
            variations.append(text.replace("method", "technique"))
        if "system" in text.lower():
            variations.append(text.replace("system", "framework"))
        if "process" in text.lower():
            variations.append(text.replace("process", "procedure"))

        # Add negations or modifications
        if not text.startswith("not ") and not text.startswith("non-"):
            variations.append(f"not {text}")

        return variations[:2]

    def _generate_contextual_alternatives(self, answer: str, text: str) -> List[str]:
        """Generate contextual alternatives"""
        doc = self.nlp(text)
        alternatives = []

        # Extract similar noun phrases
        for chunk in doc.noun_chunks:
            if (chunk.text != answer and
                len(chunk.text) > 3 and
                len(chunk.text) < 80):
                alternatives.append(chunk.text)

        return alternatives[:3]

    def _generate_professional_alternatives(self, answer: str) -> List[str]:
        """Generate professional alternatives based on domain"""
        alternatives = []

        answer_lower = answer.lower()

        # Technology domain
        if any(word in answer_lower for word in ['software', 'program', 'system', 'algorithm']):
            alternatives.extend([
                "hardware implementation",
                "manual process",
                "theoretical framework"
            ])

        # Business domain
        elif any(word in answer_lower for word in ['management', 'strategy', 'business']):
            alternatives.extend([
                "operational procedure",
                "tactical approach",
                "strategic framework"
            ])

        # Scientific domain
        elif any(word in answer_lower for word in ['research', 'study', 'analysis']):
            alternatives.extend([
                "experimental method",
                "observational study",
                "theoretical analysis"
            ])

        # Generic professional alternatives
        else:
            alternatives.extend([
                "alternative approach",
                "different methodology",
                "contrasting technique"
            ])

        return alternatives[:3]

    def _get_professional_definition_fallbacks(self, term: str, correct_answer: str) -> List[str]:
        """Get professional fallback definitions"""
        fallbacks = []

        term_lower = term.lower()

        # Technology terms
        if any(word in term_lower for word in ['software', 'program', 'algorithm', 'system']):
            fallbacks.extend([
                "a hardware component used for processing",
                "a manual procedure for data entry",
                "a theoretical concept without practical application"
            ])

        # Scientific terms
        elif any(word in term_lower for word in ['method', 'process', 'technique']):
            fallbacks.extend([
                "a random approach without systematic basis",
                "an outdated procedure no longer in use",
                "a theoretical framework without empirical support"
            ])

        # Business terms
        elif any(word in term_lower for word in ['management', 'strategy', 'organization']):
            fallbacks.extend([
                "an informal arrangement without structure",
                "a temporary solution for immediate needs",
                "a regulatory requirement imposed externally"
            ])

        # Generic fallbacks
        else:
            fallbacks.extend([
                "an unrelated concept from a different domain",
                "a deprecated approach no longer recommended",
                "a specialized tool for specific applications"
            ])

        return [f for f in fallbacks if f != correct_answer][:3]

    def _ensure_unique_options(self, options: List[str]) -> List[str]:
        """Ensure exactly 4 unique, professional options"""
        unique_options = []
        seen = set()

        for option in options:
            option_clean = option.strip().lower()
            if option_clean not in seen and len(option.strip()) > 3:
                unique_options.append(option.strip())
                seen.add(option_clean)

        # Pad with professional fallbacks if needed
        while len(unique_options) < 4:
            fallback = f"Alternative professional option {len(unique_options)}"
            if fallback.lower() not in seen:
                unique_options.append(fallback)
                seen.add(fallback.lower())

        return unique_options[:4]

    def _enhance_question_quality(self, questions: List[Dict], text: str) -> List[Dict]:
        """Enhance the quality of generated questions"""
        enhanced_questions = []

        for question in questions:
            # Enhance question text
            question_text = question.get("question", "")
            enhanced_question_text = self._enhance_question_text(question_text)

            # Enhance options
            options = question.get("options", {})
            enhanced_options = self._enhance_options(options)

            # Calculate professional score
            professional_score = self._calculate_professional_score(
                enhanced_question_text, enhanced_options, question
            )

            if professional_score >= 0.7:  # High professional standard
                enhanced_question = question.copy()
                enhanced_question["question"] = enhanced_question_text
                enhanced_question["options"] = enhanced_options
                enhanced_question["professional_score"] = professional_score
                enhanced_questions.append(enhanced_question)

        return enhanced_questions

    def _enhance_question_text(self, question_text: str) -> str:
        """Enhance question text for professional quality"""
        if not question_text:
            return question_text

        # Ensure proper capitalization
        enhanced = question_text.strip()
        if enhanced:
            enhanced = enhanced[0].upper() + enhanced[1:]

        # Add professional language
        if enhanced.startswith("What is"):
            enhanced = enhanced.replace("What is", "Which of the following best defines")
        elif enhanced.startswith("What does"):
            enhanced = enhanced.replace("What does", "How does")

        # Ensure question mark
        if not enhanced.endswith("?"):
            enhanced += "?"

        return enhanced

    def _enhance_options(self, options: Dict) -> Dict:
        """Enhance options for professional quality"""
        enhanced_options = {}

        for key, value in options.items():
            if value:
                # Ensure proper formatting
                enhanced_value = value.strip()
                if enhanced_value:
                    # Capitalize first letter
                    enhanced_value = enhanced_value[0].upper() + enhanced_value[1:]
                    # Remove trailing punctuation except for complete sentences
                    if enhanced_value.endswith('.') and len(enhanced_value.split()) < 10:
                        enhanced_value = enhanced_value[:-1]

                enhanced_options[key] = enhanced_value
            else:
                enhanced_options[key] = value

        return enhanced_options

    def _calculate_professional_score(self, question_text: str, options: Dict, question_data: Dict) -> float:
        """Calculate professional quality score"""
        score = 0.0

        # Question quality (40%)
        if self._is_professional_question(question_text):
            score += 0.4

        # Options quality (30%)
        if len(options) == 4 and len(set(options.values())) == 4:
            score += 0.2
            # Check option balance
            lengths = [len(opt.split()) for opt in options.values() if opt]
            if lengths and max(lengths) - min(lengths) <= 4:
                score += 0.1

        # Content quality (20%)
        if question_data.get("confidence", 0) > 0.6:
            score += 0.2

        # Source quality (10%)
        source = question_data.get("source", "")
        if "professional" in source:
            score += 0.1

        return min(score, 1.0)

    def _select_professional_questions(self, questions: List[Dict], target_count: int) -> List[Dict]:
        """Select the best professional questions"""
        if len(questions) <= target_count:
            return questions

        # Sort by professional score
        questions.sort(key=lambda x: x.get("professional_score", 0), reverse=True)

        # Ensure diversity of question types
        selected = []
        type_counts = {"definition": 0, "concept": 0, "application": 0}
        max_per_type = max(1, target_count // 3)

        for question in questions:
            if len(selected) >= target_count:
                break

            question_type = question.get("type", "unknown")
            if type_counts.get(question_type, 0) < max_per_type:
                selected.append(question)
                type_counts[question_type] = type_counts.get(question_type, 0) + 1

        # Fill remaining slots with highest scoring questions
        for question in questions:
            if len(selected) >= target_count:
                break
            if question not in selected:
                selected.append(question)

        return selected[:target_count]

    def _apply_professional_polish(self, question: Dict, difficulty: str):
        """Apply final professional polish"""
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

        # Enhance explanation based on difficulty
        if difficulty == "hard":
            explanation = question.get("explanation", "")
            question["explanation"] = f"Advanced: {explanation}"
        elif difficulty == "easy":
            explanation = question.get("explanation", "")
            question["explanation"] = f"Basic: {explanation}"


# Main interface function
def generate_enhanced_professional_mcq_questions(text: str, num_questions: int = 10,
                                               difficulty: str = "medium") -> List[Dict]:
    """
    Generate enhanced professional-quality MCQ questions

    Args:
        text (str): Input text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)

    Returns:
        List[Dict]: List of enhanced professional-quality MCQ questions
    """
    try:
        generator = EnhancedProfessionalMCQGenerator()
        return generator.generate_professional_questions(text, num_questions, difficulty)
    except Exception as e:
        print(f"Error in enhanced professional MCQ generation: {e}")
        return []


def is_enhanced_professional_mode_available() -> bool:
    """Check if enhanced professional mode dependencies are available"""
    return ENHANCED_DEPENDENCIES_AVAILABLE
