"""
Tests for the LiteLLM utility functions.
"""
import sys
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from Backend.utils.llm_utils import generate_chat_response, generate_embedding, transcribe_audio
from Backend.config.settings import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = MagicMock()
    settings.DEFAULT_CHAT_PROVIDER = "openai"
    settings.DEFAULT_EMBEDDING_PROVIDER = "openai"
    settings.DEFAULT_VOICE_PROVIDER = "openai"
    settings.LITELLM_PROVIDERS = {
        "openai": {
            "api_key": "test-api-key",
            "chat_model": "gpt-4o",
            "embedding_model": "text-embedding-3-large",
        },
        "anthropic": {
            "api_key": "test-anthropic-key",
            "chat_model": "claude-3-5-sonnet-20241022",
        },
    }
    return settings


@pytest.mark.asyncio
async def test_generate_chat_response(mock_settings):
    """Test generate_chat_response function."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test response"
    
    with patch("Backend.utils.llm_utils.settings", mock_settings), \
         patch("Backend.utils.llm_utils.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = mock_response
        
        # Test with default parameters
        result = await generate_chat_response("Test prompt")
        assert result == "This is a test response"
        
        # Verify acompletion was called with correct parameters
        mock_acompletion.assert_called_with(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Test prompt"}],
            api_key="test-api-key",
            temperature=0.7,
            max_tokens=1000
        )
        
        # Test with system message
        result = await generate_chat_response("Test prompt", system_message="You are a helpful assistant")
        assert result == "This is a test response"
        
        # Verify acompletion was called with correct parameters including system message
        mock_acompletion.assert_called_with(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Test prompt"}
            ],
            api_key="test-api-key",
            temperature=0.7,
            max_tokens=1000
        )


@pytest.mark.asyncio
async def test_generate_embedding(mock_settings):
    """Test generate_embedding function."""
    mock_embedding = [0.1, 0.2, 0.3]
    mock_response = MagicMock()
    mock_response.data = [MagicMock()]
    mock_response.data[0].embedding = mock_embedding
    
    with patch("Backend.utils.llm_utils.settings", mock_settings), \
         patch("Backend.utils.llm_utils.aembedding", new_callable=AsyncMock) as mock_aembedding:
        mock_aembedding.return_value = mock_response
        
        # Test with single text
        result = await generate_embedding("Test text")
        assert result == mock_embedding
        
        # Verify aembedding was called with correct parameters
        mock_aembedding.assert_called_with(
            model="text-embedding-3-large",
            input=["Test text"],
            api_key="test-api-key"
        )
        
        # Test with list of texts
        mock_response.data = [MagicMock(), MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_response.data[1].embedding = [0.4, 0.5, 0.6]
        mock_aembedding.return_value = mock_response
        
        result = await generate_embedding(["Text 1", "Text 2"])
        assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        # Verify aembedding was called with correct parameters
        mock_aembedding.assert_called_with(
            model="text-embedding-3-large",
            input=["Text 1", "Text 2"],
            api_key="test-api-key"
        )


@pytest.mark.asyncio
async def test_transcribe_audio(mock_settings):
    """Test transcribe_audio function."""
    # Mock the OpenAI client for audio transcription
    mock_transcription = MagicMock()
    mock_transcription.text = "This is a test transcription"
    
    mock_client = MagicMock()
    mock_client.audio.transcriptions.create.return_value = mock_transcription
    
    # Mock the openai import
    mock_openai = MagicMock()
    mock_openai.OpenAI.return_value = mock_client
    
    with patch("Backend.utils.llm_utils.settings", mock_settings), \
         patch.dict("sys.modules", {"openai": mock_openai}), \
         patch("builtins.open", MagicMock()):
        
        # Test with default parameters
        result = await transcribe_audio("test_audio.mp3")
        assert result == "This is a test transcription"
        
        # Verify OpenAI client was called correctly
        mock_client.audio.transcriptions.create.assert_called_once() 