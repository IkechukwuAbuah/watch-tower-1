"""
OpenAI Responses API service for Watch Tower natural language interface
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from openai import AsyncOpenAI
from core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for handling natural language queries using OpenAI Responses API"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens
        
        # Function registry for available AI tools
        self.function_registry: Dict[str, Callable] = {}
        self._register_default_functions()
    
    def _register_default_functions(self):
        """Register default AI functions"""
        from .ai_functions import (
            get_truck_location,
            create_new_trip,
            get_fleet_status,
            get_trip_details,
            get_daily_summary
        )
        
        self.function_registry.update({
            "get_truck_location": get_truck_location,
            "create_new_trip": create_new_trip,
            "get_fleet_status": get_fleet_status,
            "get_trip_details": get_trip_details,
            "get_daily_summary": get_daily_summary
        })
    
    def register_function(self, name: str, func: Callable):
        """Register a new AI function"""
        self.function_registry[name] = func
        logger.info(f"Registered AI function: {name}")
    
    async def process_natural_language_query(
        self, 
        query: str, 
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language query and return structured response
        
        Args:
            query: User's natural language query
            user_context: Additional context (user_id, permissions, etc.)
            
        Returns:
            Structured response with data and/or actions
        """
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Define available functions for the AI
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_truck_location",
                        "description": "Get current location and status of a specific truck",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "truck_number": {
                                    "type": "string",
                                    "description": "The truck number (e.g., T11985LA)"
                                }
                            },
                            "required": ["truck_number"]
                        }
                    }
                },
                {
                    "type": "function", 
                    "function": {
                        "name": "create_new_trip",
                        "description": "Create a new trip for a truck",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "truck_number": {
                                    "type": "string",
                                    "description": "The truck number"
                                },
                                "origin": {
                                    "type": "string",
                                    "description": "Origin location or terminal"
                                },
                                "destination": {
                                    "type": "string", 
                                    "description": "Destination location"
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Scheduled departure date/time"
                                }
                            },
                            "required": ["truck_number", "origin", "destination"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_fleet_status",
                        "description": "Get overall fleet status and summary",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filter": {
                                    "type": "string",
                                    "description": "Optional filter (active, idle, maintenance, etc.)"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_trip_details",
                        "description": "Get details of a specific trip",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "trip_id": {
                                    "type": "string",
                                    "description": "Trip ID or VPC ID"
                                }
                            },
                            "required": ["trip_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_daily_summary",
                        "description": "Get daily fleet performance summary",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "Date for summary (YYYY-MM-DD) or 'today'"
                                }
                            }
                        }
                    }
                }
            ]
            
            # System prompt for Lagos fleet management context
            system_prompt = """You are a helpful assistant for VPC (Virgo Point Capital) fleet management in Lagos, Nigeria. 
            
You help fleet managers track trucks, create trips, and analyze fleet performance. The fleet consists of container trucks operating between terminals (like ESSLIBRA, ECLAT, PTML) and client locations.

Key context:
- Trucks have numbers like T11985LA, T28737LA
- All times are in Lagos timezone (Africa/Lagos)
- Common terminals: ESSLIBRA, ECLAT, PTML, APM
- Trip creation requires truck number, origin, destination, and optionally scheduled time
- Always provide clear, actionable responses for fleet operations

Use the available functions to help users with their fleet management queries."""

            # Make API call to OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                tools=tools,
                tool_choice="auto",
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            message = response.choices[0].message
            
            # Check if AI wants to call functions
            if message.tool_calls:
                function_results = []
                
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)
                    
                    logger.info(f"Calling function: {function_name} with args: {function_args}")
                    
                    if function_name in self.function_registry:
                        try:
                            result = await self.function_registry[function_name](**function_args)
                            function_results.append({
                                "tool_call_id": tool_call.id,
                                "function": function_name,
                                "result": result
                            })
                        except Exception as e:
                            logger.error(f"Function {function_name} failed: {e}")
                            function_results.append({
                                "tool_call_id": tool_call.id,
                                "function": function_name,
                                "error": str(e)
                            })
                    else:
                        logger.error(f"Unknown function: {function_name}")
                        function_results.append({
                            "tool_call_id": tool_call.id,
                            "function": function_name,
                            "error": f"Function {function_name} not available"
                        })
                
                # Get final response from AI with function results
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": message.content, "tool_calls": message.tool_calls}
                ]
                
                for result in function_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": result["tool_call_id"],
                        "content": str(result.get("result", result.get("error")))
                    })
                
                final_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                return {
                    "response": final_response.choices[0].message.content,
                    "function_calls": function_results,
                    "status": "success"
                }
            else:
                # Direct response without function calls
                return {
                    "response": message.content,
                    "function_calls": [],
                    "status": "success"
                }
                
        except Exception as e:
            logger.error(f"AI query processing failed: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again or contact support.",
                "error": str(e),
                "status": "error"
            }
    
    async def create_trip_from_natural_language(
        self, 
        description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create trip from natural language description
        
        Example: "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
        """
        enhanced_query = f"""Parse this trip creation request and create the trip: {description}
        
        Extract the truck number, origin, destination, and scheduled time if mentioned.
        If no time is specified, assume 9:00 AM Lagos time.
        If "tomorrow" is mentioned, use tomorrow's date.
        """
        
        return await self.process_natural_language_query(enhanced_query, context)
    
    async def query_fleet_status(
        self, 
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle fleet status queries"""
        enhanced_query = f"Fleet status query: {query}"
        return await self.process_natural_language_query(enhanced_query, context)


# Global instance
ai_service = AIService()