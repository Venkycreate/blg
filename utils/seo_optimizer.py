from typing import Dict, List
import re

class SEOOptimizer:
    def __init__(self):
        self.min_word_count = 300
        self.max_word_count = 2500
        self.min_keyword_density = 0.01
        self.max_keyword_density = 0.03

    def analyze_content(self, content: Dict, keywords: List[str]) -> Dict:
        """Analyze content for SEO metrics"""
        text = content['content']
        word_count = len(text.split())
        
        metrics = {
            'word_count': word_count,
            'keyword_density': {},
            'readability_score': self._calculate_readability(text),
            'suggestions': []
        }

        # Calculate keyword density
        for keyword in keywords:
            count = len(re.findall(rf'\b{re.escape(keyword)}\b', text.lower()))
            density = count / word_count if word_count > 0 else 0
            metrics['keyword_density'][keyword] = density

        # Generate suggestions
        if word_count < self.min_word_count:
            metrics['suggestions'].append(f"Content length ({word_count} words) is below recommended minimum of {self.min_word_count} words")
        elif word_count > self.max_word_count:
            metrics['suggestions'].append(f"Content length ({word_count} words) exceeds recommended maximum of {self.max_word_count} words")

        for keyword, density in metrics['keyword_density'].items():
            if density < self.min_keyword_density:
                metrics['suggestions'].append(f"Keyword '{keyword}' density is too low ({density:.2%})")
            elif density > self.max_keyword_density:
                metrics['suggestions'].append(f"Keyword '{keyword}' density is too high ({density:.2%})")

        return metrics

    def _calculate_readability(self, text: str) -> float:
        """Calculate basic readability score"""
        sentences = len(re.split(r'[.!?]+', text))
        words = len(text.split())
        syllables = self._count_syllables(text)
        
        if sentences == 0 or words == 0:
            return 0
        
        # Flesch Reading Ease score
        score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        return max(0, min(100, score))

    def _count_syllables(self, text: str) -> int:
        """Rough syllable count"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
            
        return count
