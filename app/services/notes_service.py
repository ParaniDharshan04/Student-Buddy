from typing import List, Dict, Any
import re
import math
from app.services.ai_service import AIService
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class NotesService:
    def __init__(self):
        self.ai_service = None
        self.max_chunk_size = settings.MAX_CONTENT_LENGTH
    
    def _get_ai_service(self):
        """Return an AIService instance, creating it if necessary."""
        if self.ai_service is None:
            self.ai_service = AIService()
        return self.ai_service
    
    async def summarize_content(
        self,
        content: str,
        format_type: str = "bullet_points",
        max_length: int = None,
        topic: str = None
    ) -> Dict[str, Any]:
        """
        Summarize text content into structured notes
        
        Args:
            content: Text content to summarize
            format_type: Format for the summary
            max_length: Maximum length of summary
            topic: Optional topic for context
            
        Returns:
            Dictionary containing summary and metadata
        """
        try:
            # Get AI service
            ai_service = self._get_ai_service()
            
            # Handle long content by chunking if necessary
            chunks = self._chunk_content(content)
            
            if len(chunks) == 1:
                # Single chunk - direct summarization
                summary = await self._summarize_chunk(chunks[0], format_type, topic)
            else:
                # Multiple chunks - summarize each then combine
                chunk_summaries = []
                for i, chunk in enumerate(chunks):
                    logger.info(f"Summarizing chunk {i+1}/{len(chunks)}")
                    chunk_summary = await self._summarize_chunk(chunk, format_type, topic)
                    chunk_summaries.append(chunk_summary)
                
                # Combine chunk summaries
                combined_content = "\n\n".join(chunk_summaries)
                summary = await self._create_final_summary(combined_content, format_type, topic)
            
            # Apply length limit if specified
            if max_length and len(summary) > max_length:
                summary = self._truncate_summary(summary, max_length)
            
            # Extract metadata
            key_terms = self._extract_key_terms(summary)
            main_topics = self._extract_main_topics(summary, topic)
            reading_time = self._calculate_reading_time(summary)
            compression_ratio = len(summary) / len(content) if len(content) > 0 else 0
            
            return {
                "summary": summary,
                "format": format_type,
                "original_length": len(content),
                "summary_length": len(summary),
                "compression_ratio": round(compression_ratio, 3),
                "key_terms": key_terms,
                "main_topics": main_topics,
                "reading_time": reading_time
            }
            
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            raise Exception(f"Failed to summarize content: {str(e)}")
    
    def _chunk_content(self, content: str) -> List[str]:
        """Split content into manageable chunks"""
        if len(content) <= self.max_chunk_size:
            return [content]
        
        chunks = []
        words = content.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > self.max_chunk_size and current_chunk:
                # Finish current chunk
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        # Add the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    async def _summarize_chunk(self, chunk: str, format_type: str, topic: str = None) -> str:
        """Summarize a single chunk of content"""
        prompt = self._create_summary_prompt(chunk, format_type, topic)
        
        # Use AI service to summarize
        ai_service = self._get_ai_service()
        ai_response = await ai_service.summarize_notes(chunk)
        
        # Format the response according to the requested format
        formatted_summary = self._format_summary(ai_response["summary"], format_type)
        
        return formatted_summary
    
    async def _create_final_summary(self, combined_summaries: str, format_type: str, topic: str = None) -> str:
        """Create final summary from multiple chunk summaries"""
        prompt = f"""Please create a cohesive final summary from these section summaries:

{combined_summaries}

Requirements:
- Combine related points and remove redundancy
- Maintain the {format_type} format
- Focus on the most important information
- Ensure logical flow and organization
"""
        
        if topic:
            prompt += f"\n- Keep focus on the topic: {topic}"
        
        try:
            ai_service = self._get_ai_service()
            response = await ai_service._make_request_with_retry(prompt)
            return self._format_summary(response, format_type)
        except Exception as e:
            logger.warning(f"Failed to create final summary, using combined summaries: {str(e)}")
            return combined_summaries
    
    def _create_summary_prompt(self, content: str, format_type: str, topic: str = None) -> str:
        """Create prompt for summarization based on format type"""
        base_prompt = f"Please summarize the following content:\n\n{content}\n\n"
        
        format_instructions = {
            "bullet_points": """Format as bullet points:
- Use clear, concise bullet points
- Group related information together
- Highlight key concepts and important details
- Use sub-bullets for supporting information""",
            
            "paragraph": """Format as coherent paragraphs:
- Write 2-3 well-structured paragraphs
- Each paragraph should focus on a main theme
- Use clear topic sentences and supporting details
- Maintain logical flow between paragraphs""",
            
            "outline": """Format as a structured outline:
- Use hierarchical numbering (1., 1.1, 1.1.1)
- Organize information from general to specific
- Include main topics and subtopics
- Keep each point concise but informative""",
            
            "key_concepts": """Format as key concepts with explanations:
- Identify 5-8 most important concepts
- Provide brief explanation for each concept
- Use bold or emphasis for concept names
- Focus on understanding rather than details"""
        }
        
        instruction = format_instructions.get(format_type, format_instructions["bullet_points"])
        prompt = base_prompt + instruction
        
        if topic:
            prompt += f"\n\nFocus particularly on information related to: {topic}"
        
        return prompt
    
    def _format_summary(self, summary: str, format_type: str) -> str:
        """Apply additional formatting to the summary"""
        if format_type == "bullet_points":
            return self._ensure_bullet_format(summary)
        elif format_type == "outline":
            return self._ensure_outline_format(summary)
        elif format_type == "key_concepts":
            return self._ensure_key_concepts_format(summary)
        else:
            return summary
    
    def _ensure_bullet_format(self, text: str) -> str:
        """Ensure text is properly formatted with bullet points"""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('•', '-', '*')):
                # Add bullet point if missing
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                    line = '• ' + line[2:].strip()
                elif not line.startswith('  '):  # Not a sub-bullet
                    line = '• ' + line
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _ensure_outline_format(self, text: str) -> str:
        """Ensure text is properly formatted as an outline"""
        lines = text.split('\n')
        formatted_lines = []
        main_counter = 1
        
        for line in lines:
            line = line.strip()
            if line:
                # Check if line already has numbering
                if not re.match(r'^\d+\.', line):
                    # Add numbering if it's a main point
                    if not line.startswith('  '):
                        line = f"{main_counter}. {line}"
                        main_counter += 1
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _ensure_key_concepts_format(self, text: str) -> str:
        """Ensure text is formatted as key concepts"""
        # This is a simple implementation - could be enhanced
        return text
    
    def _truncate_summary(self, summary: str, max_length: int) -> str:
        """Truncate summary to maximum length while preserving structure"""
        if len(summary) <= max_length:
            return summary
        
        # Try to truncate at sentence boundaries
        sentences = summary.split('. ')
        truncated = ""
        
        for sentence in sentences:
            if len(truncated + sentence + '. ') <= max_length - 3:  # -3 for "..."
                truncated += sentence + '. '
            else:
                break
        
        if truncated:
            return truncated.rstrip() + "..."
        else:
            # Fallback: hard truncate
            return summary[:max_length-3] + "..."
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from the summary"""
        # Enhanced key term extraction
        key_terms = []
        
        # Look for capitalized terms (proper nouns, concepts)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Look for terms in quotes or emphasis
        quoted_terms = re.findall(r'"([^"]+)"', text)
        emphasized_terms = re.findall(r'\*([^*]+)\*', text)
        
        # Combine and filter
        all_terms = capitalized_terms + quoted_terms + emphasized_terms
        
        # Remove common words and duplicates
        common_words = {
            'The', 'This', 'That', 'These', 'Those', 'When', 'Where', 'What', 
            'How', 'Why', 'Which', 'Who', 'First', 'Second', 'Third', 'Next',
            'Finally', 'However', 'Therefore', 'Moreover', 'Furthermore'
        }
        
        for term in all_terms:
            if term not in common_words and len(term) > 2:
                key_terms.append(term)
        
        # Remove duplicates and limit to top 8
        return list(dict.fromkeys(key_terms))[:8]
    
    def _extract_main_topics(self, text: str, provided_topic: str = None) -> List[str]:
        """Extract main topics from the summary"""
        topics = []
        
        # Add provided topic if available
        if provided_topic:
            topics.append(provided_topic.title())
        
        # Look for topic indicators in text
        topic_patterns = [
            r'(?:about|regarding|concerning)\s+([A-Za-z\s]+?)(?:\.|,|:)',
            r'(?:topic|subject|theme)(?:\s+of)?\s+([A-Za-z\s]+?)(?:\.|,|:)',
            r'(?:study|analysis|discussion)\s+of\s+([A-Za-z\s]+?)(?:\.|,|:)'
        ]
        
        for pattern in topic_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                topic = match.strip().title()
                if len(topic) > 3 and topic not in topics:
                    topics.append(topic)
        
        # Limit to 5 topics
        return topics[:5]
    
    def _calculate_reading_time(self, text: str) -> int:
        """Calculate estimated reading time in minutes"""
        # Average reading speed: 200-250 words per minute
        # Using 225 words per minute as average
        word_count = len(text.split())
        reading_time = math.ceil(word_count / 225)
        
        # Minimum 1 minute
        return max(1, reading_time)