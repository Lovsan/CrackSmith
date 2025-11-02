"""
Utility functions for the CrackSmith backend
"""
import logging

logger = logging.getLogger(__name__)

def safe_error_response(error, default_message="An error occurred"):
    """
    Return a safe error message that doesn't expose internal details
    
    Args:
        error: The exception object
        default_message: Default message to return to user
        
    Returns:
        str: Safe error message for external users
    """
    # Log the actual error for debugging
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    
    # Return generic message to user
    return default_message
