"""
Vertex AI client for text summarization using Gemini models.
"""
import json
import logging
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
from google.protobuf import struct_pb2
from app.config import Config
from app.logging_config import get_logger

logger = get_logger(__name__)


class VertexAIClient:
    """Client for interacting with Vertex AI Gemini models."""
    
    def __init__(self):
        """Initialize the Vertex AI client."""
        self.project_id = Config.VERTEX_AI_PROJECT_ID
        self.location = Config.VERTEX_AI_LOCATION
        self.model = Config.VERTEX_AI_MODEL
        
        # Initialize Vertex AI
        aiplatform.init(
            project=self.project_id,
            location=self.location
        )
        
        # Create prediction client
        self.client = gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"}
        )
        
        logger.info(f"Initialized Vertex AI client for project: {self.project_id}")
    
    def summarize_text(self, text: str, max_length: int = 300) -> str:
        """
        Summarize text using Vertex AI Gemini model.
        
        Args:
            text: The text to summarize
            max_length: Maximum length of the summary
            
        Returns:
            Summarized text
        """
        try:
            # Prepare the prompt
            prompt = self._create_summary_prompt(text, max_length)
            
            # Prepare the request
            endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model}"
            
            # Create the request payload
            instance = struct_pb2.Struct()
            instance.update({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    }
                ],
                "generation_config": {
                    "max_output_tokens": max_length * 2,  # Allow some buffer
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "top_k": 40
                }
            })
            
            instances = [instance]
            
            # Make the prediction request
            response = self.client.predict(
                endpoint=endpoint,
                instances=instances
            )
            
            # Extract the summary from response
            if response.predictions:
                prediction = response.predictions[0]
                # Handle different response formats
                if hasattr(prediction, 'content'):
                    return prediction.content
                elif isinstance(prediction, dict) and 'content' in prediction:
                    return prediction['content']
                elif hasattr(prediction, 'candidates'):
                    candidates = prediction.candidates
                    if candidates and len(candidates) > 0:
                        return candidates[0].content.parts[0].text
                
            logger.warning("No valid prediction found in response")
            return "要約の生成に失敗しました。"
            
        except Exception as e:
            logger.error(f"Error during text summarization: {str(e)}")
            return f"要約エラー: {str(e)}"
    
    def _create_summary_prompt(self, text: str, max_length: int) -> str:
        """
        Create a prompt for text summarization.
        
        Args:
            text: The original text
            max_length: Maximum length of summary
            
        Returns:
            Formatted prompt string
        """
        return f"""以下のZenn記事を{max_length}文字程度で要約してください。技術的なポイントを重視し、具体的で有用な情報を含めてください。

記事内容:
{text}

要約（{max_length}文字程度）:"""
    
    def summarize_multiple_texts(self, texts: List[str], max_length: int = 300) -> List[str]:
        """
        Summarize multiple texts concurrently.
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum length per summary
            
        Returns:
            List of summaries
        """
        summaries = []
        
        for i, text in enumerate(texts):
            logger.info(f"Summarizing text {i+1}/{len(texts)}")
            summary = self.summarize_text(text, max_length)
            summaries.append(summary)
        
        return summaries
    
    def test_connection(self) -> bool:
        """
        Test the connection to Vertex AI.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Simple test with minimal text
            test_result = self.summarize_text("これはテストです。", max_length=50)
            return "テスト" in test_result or "エラー" not in test_result
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False