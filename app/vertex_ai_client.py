"""
Vertex AI client for text summarization using Gemini models.
"""
import json
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
from google.protobuf import struct_pb2
from app.config import Config
from app.logging_config import get_logger

logger = get_logger()


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
        
        logger.info(
            operation="vertex_ai_init",
            message="Vertex AI client initialized",
            context={
                "project_id": self.project_id,
                "location": self.location,
                "model": self.model
            }
        )
    
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
                
            logger.warning(
                operation="text_summarization",
                message="No valid prediction found in response",
                context={
                    "response_type": type(response).__name__,
                    "predictions_count": len(predictions) if predictions else 0
                }
            )
            return "要約の生成に失敗しました。"
            
        except Exception as e:
            logger.error(
                operation="text_summarization",
                message="Text summarization failed",
                context={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "text_length": len(text) if text else 0
                },
                human_note="AI-TODO: テキスト要約エラーの詳細な調査が必要です"
            )
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
            logger.info(
                operation="batch_summarization",
                message="Processing text batch",
                context={
                    "current_index": i+1,
                    "total_count": len(texts),
                    "text_length": len(text)
                }
            )
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
            logger.error(
                operation="connection_test",
                message="Vertex AI connection test failed",
                context={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "project_id": self.project_id,
                    "location": self.location
                },
                human_note="AI-TODO: Vertex AI接続設定の確認が必要です"
            )
            return False