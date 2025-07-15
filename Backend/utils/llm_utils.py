"""
LLM utility functions using LiteLLM for the AI Context Builder.

This module provides a unified interface for interacting with various LLM providers
through LiteLLM, including functions for chat completions, embeddings, and voice transcription.
"""
import logging
from typing import Dict, List, Optional, Union, Any

from litellm import acompletion, completion, embedding, aembedding
from litellm.exceptions import APIError, RateLimitError, ServiceUnavailableError

from Backend.config.settings import settings

logger = logging.getLogger(__name__)

async def generate_chat_response(
    prompt: str,
    provider: str = None,
    model: str = None,
    system_message: str = None,
    messages: List[Dict[str, str]] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    **kwargs
) -> str:
    """
    Generate a chat response using LiteLLM.
    
    Args:
        prompt: The user prompt to send to the LLM
        provider: The LLM provider to use (defaults to settings.DEFAULT_CHAT_PROVIDER)
        model: The specific model to use (defaults to provider's chat_model in settings)
        system_message: Optional system message to include
        messages: Optional list of previous messages for context
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        **kwargs: Additional parameters to pass to LiteLLM
        
    Returns:
        The generated text response
        
    Raises:
        ValueError: If the provider is not configured
        APIError: If there's an error with the LLM API call
    """
    provider = provider or settings.DEFAULT_CHAT_PROVIDER
    provider_config = settings.LITELLM_PROVIDERS.get(provider)
    
    if not provider_config:
        raise ValueError(f"Provider {provider} not configured")
    
    if not provider_config.get("api_key"):
        raise ValueError(f"API key for provider {provider} not set")
    
    model = model or provider_config.get("chat_model")
    
    # Prepare messages
    if messages is None:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
    
    try:
        response = await acompletion(
            model=model,
            messages=messages,
            api_key=provider_config["api_key"],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    except (RateLimitError, ServiceUnavailableError) as e:
        logger.warning(f"Error with provider {provider}: {str(e)}. Attempting fallback...")
        # Try fallback if available and different from current provider
        if settings.DEFAULT_CHAT_PROVIDER != provider:
            return await generate_chat_response(
                prompt=prompt,
                provider=settings.DEFAULT_CHAT_PROVIDER,
                system_message=system_message,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        raise
    except APIError as e:
        logger.error(f"LiteLLM API error: {str(e)}")
        raise

async def generate_embedding(
    text: Union[str, List[str]],
    provider: str = None,
    model: str = None,
    **kwargs
) -> Union[List[float], List[List[float]]]:
    """
    Generate embeddings for text using LiteLLM.
    
    Args:
        text: Text or list of texts to embed
        provider: The LLM provider to use (defaults to settings.DEFAULT_EMBEDDING_PROVIDER)
        model: The specific model to use (defaults to provider's embedding_model in settings)
        **kwargs: Additional parameters to pass to LiteLLM
        
    Returns:
        List of embeddings (or list of lists for batch embedding)
        
    Raises:
        ValueError: If the provider is not configured
        APIError: If there's an error with the LLM API call
    """
    provider = provider or settings.DEFAULT_EMBEDDING_PROVIDER
    provider_config = settings.LITELLM_PROVIDERS.get(provider)
    
    if not provider_config:
        raise ValueError(f"Provider {provider} not configured")
    
    if not provider_config.get("api_key"):
        raise ValueError(f"API key for provider {provider} not set")
    
    model = model or provider_config.get("embedding_model")
    
    try:
        response = await aembedding(
            model=model,
            input=text if isinstance(text, list) else [text],
            api_key=provider_config["api_key"],
            **kwargs
        )
        
        embeddings = [data.embedding for data in response.data]
        return embeddings if isinstance(text, list) else embeddings[0]
    except (RateLimitError, ServiceUnavailableError) as e:
        logger.warning(f"Error with provider {provider}: {str(e)}. Attempting fallback...")
        # Try fallback if available and different from current provider
        if settings.DEFAULT_EMBEDDING_PROVIDER != provider:
            return await generate_embedding(
                text=text,
                provider=settings.DEFAULT_EMBEDDING_PROVIDER,
                **kwargs
            )
        raise
    except APIError as e:
        logger.error(f"LiteLLM API error: {str(e)}")
        raise

async def transcribe_audio(
    audio_path: str,
    provider: str = None,
    model: str = "whisper-1",
    **kwargs
) -> str:
    """
    Transcribe audio using LiteLLM (primarily via OpenAI's Whisper API).
    
    Args:
        audio_path: Path to the audio file
        provider: The provider to use (defaults to settings.DEFAULT_VOICE_PROVIDER)
        model: The model to use (defaults to "whisper-1" for OpenAI)
        **kwargs: Additional parameters to pass to the API
        
    Returns:
        Transcribed text
        
    Raises:
        ValueError: If the provider is not configured
        APIError: If there's an error with the LLM API call
    """
    provider = provider or settings.DEFAULT_VOICE_PROVIDER
    provider_config = settings.LITELLM_PROVIDERS.get(provider)
    
    if not provider_config:
        raise ValueError(f"Provider {provider} not configured")
    
    if not provider_config.get("api_key"):
        raise ValueError(f"API key for provider {provider} not set")
    
    try:
        # For OpenAI, we use their specific audio transcription API
        if provider == "openai":
            # Import here to avoid dependency if not used
            import openai
            
            client = openai.OpenAI(api_key=provider_config["api_key"])
            with open(audio_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    **kwargs
                )
            return response.text
        else:
            # For other providers that might support audio transcription via LiteLLM
            # This is a placeholder and might need adjustment based on LiteLLM's capabilities
            logger.warning(f"Audio transcription with provider {provider} not fully implemented")
            return f"Audio transcription with {provider} not implemented"
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise 