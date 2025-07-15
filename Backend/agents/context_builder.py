"""
Context Builder Agent for generating system prompts and configurations.
"""
import logging
from typing import Any, Dict, List, Optional

from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from Backend.utils.llm_utils import generate_chat_response

logger = logging.getLogger(__name__)


class ContextBuilderInput(BaseModel):
    """Input for the Context Builder Agent."""
    job_id: str
    format: str = "cursor"  # cursor, windsurf, etc.
    context_data: Dict[str, Any] = Field(default_factory=dict)


class ContextBuilderOutput(BaseModel):
    """Output from the Context Builder Agent."""
    config: str
    format: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextBuilderState(BaseModel):
    """State for the Context Builder workflow."""
    job_id: str
    format: str
    context_data: Dict[str, Any] = Field(default_factory=dict)
    extracted_entities: List[Dict[str, Any]] = Field(default_factory=list)
    knowledge_graph: Dict[str, Any] = Field(default_factory=dict)
    generated_config: Optional[str] = None
    errors: List[str] = Field(default_factory=list)


class ContextBuilderAgent:
    """Agent for building context and generating configurations."""
    
    def __init__(self):
        """Initialize the Context Builder Agent."""
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow for context building.
        
        Returns:
            StateGraph: The workflow graph.
        """
        # This is a placeholder for the actual workflow implementation
        # It will be implemented with LangGraph once we have the full structure
        workflow = StateGraph(ContextBuilderState)
        
        # Define workflow nodes and edges here
        # For now, we'll just return the empty workflow
        return workflow
    
    async def _analyze_context_data(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze context data using LiteLLM to extract key insights.
        
        Args:
            context_data: The context data to analyze
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Convert context data to a string representation for the LLM
            context_str = "\n\n".join([
                f"{key}:\n{value}" for key, value in context_data.items()
            ])
            
            # Create a prompt for context analysis
            prompt = f"""
            Analyze the following context data and extract key insights:
            
            {context_str}
            
            Extract the following:
            1. Main topics and themes
            2. Key entities (e.g., technologies, concepts, frameworks)
            3. Important relationships between entities
            4. Domain classification
            
            Format your response as a structured JSON.
            """
            
            # Use LiteLLM to analyze the context
            system_message = "You are an expert context analyzer that extracts structured information from text."
            response = await generate_chat_response(
                prompt=prompt,
                system_message=system_message,
                temperature=0.3,  # Lower temperature for more deterministic results
                max_tokens=2000
            )
            
            # In a real implementation, we would parse the JSON response
            # For now, we'll just return a placeholder
            return {
                "analysis": response,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error analyzing context data: {str(e)}")
            return {
                "analysis": "Error analyzing context data",
                "status": "error",
                "error": str(e)
            }
    
    async def _generate_configuration(self, format: str, analysis: Dict[str, Any]) -> str:
        """
        Generate configuration based on the format and analysis.
        
        Args:
            format: The format of the configuration (e.g., cursor, windsurf)
            analysis: The analysis of the context data
            
        Returns:
            The generated configuration as a string
        """
        try:
            # Create a prompt for configuration generation
            prompt = f"""
            Based on the following analysis, generate a {format.upper()} configuration:
            
            {analysis.get('analysis', 'No analysis available')}
            
            The configuration should follow these guidelines:
            - For Cursor format, create a markdown file with rules and context
            - For Windsurf format, create a JSON configuration
            - Include relevant rules based on the domain and entities
            - Structure the configuration according to best practices
            
            Generate the complete configuration content.
            """
            
            system_message = f"You are an expert {format} configuration generator that creates optimal AI assistant configurations."
            
            # Use LiteLLM to generate the configuration
            config = await generate_chat_response(
                prompt=prompt,
                system_message=system_message,
                temperature=0.5,
                max_tokens=4000
            )
            
            return config
        except Exception as e:
            logger.error(f"Error generating configuration: {str(e)}")
            return f"# Error Generating Configuration\n\nAn error occurred: {str(e)}"
    
    async def build_context(self, input_data: ContextBuilderInput) -> ContextBuilderOutput:
        """
        Build context and generate configuration.
        
        Args:
            input_data: The input data for context building.
            
        Returns:
            ContextBuilderOutput: The generated configuration.
        """
        try:
            # Step 1: Analyze the context data
            analysis_result = await self._analyze_context_data(input_data.context_data)
            
            # Step 2: Generate the configuration based on the analysis
            generated_config = await self._generate_configuration(
                format=input_data.format,
                analysis=analysis_result
            )
            
            # Step 3: Return the output
            return ContextBuilderOutput(
                config=generated_config,
                format=input_data.format,
                metadata={
                    "source": "litellm",
                    "analysis": analysis_result
                },
            )
        except Exception as e:
            logger.error(f"Error in build_context: {str(e)}")
            # Return a fallback configuration in case of error
            return ContextBuilderOutput(
                config=f"# Error in Configuration Generation\n\nAn error occurred: {str(e)}",
                format=input_data.format,
                metadata={"error": str(e)},
            ) 