"""
Product Data Utility Functions
Helper functions for product detection and data retrieval
"""

from .keywords import PRODUCT_KEYWORDS
from .prices import PRODUCT_PRICES
from .specs import PRODUCT_SPECS
from .responses import PRODUCT_RESPONSES
from .images import PRODUCT_IMAGES


def detect_product(user_input):
    """
    Detect which product the user is asking about
    
    Args:
        user_input: User's message text
        
    Returns:
        Product name if detected, None otherwise
    """
    user_input_lower = user_input.lower().strip()
    
    # Exclude bundle/category requests from product detection
    if any(word in user_input_lower for word in ['bundle', 'category', 'categories', 'all products', 'catalog', 'list']):
        return None
    
    # Exclude "cheapest" requests - let responses.py handle those
    if any(word in user_input_lower for word in ['cheapest', 'cheap', 'affordable', 'budget', 'least expensive', 'lowest price']):
        return None
    
    # Check for exact matches first (longer phrases)
    for keyword in sorted(PRODUCT_KEYWORDS.keys(), key=len, reverse=True):
        if keyword in user_input_lower:
            return PRODUCT_KEYWORDS[keyword]
    
    return None


def get_all_products():
    """
    Get list of all product names
    
    Returns:
        List of product names
    """
    return list(PRODUCT_PRICES.keys())


def get_product_price(product_name):
    """
    Get price for a specific product
    
    Args:
        product_name: Name of the product
        
    Returns:
        Price as integer, or None if product not found
    """
    return PRODUCT_PRICES.get(product_name)


def get_product_spec(product_name):
    """
    Get specifications for a specific product
    
    Args:
        product_name: Name of the product
        
    Returns:
        Specification string, or None if product not found
    """
    return PRODUCT_SPECS.get(product_name)


def get_product_responses(product_name):
    """
    Get all response variations for a specific product
    
    Args:
        product_name: Name of the product
        
    Returns:
        List of response variations, or empty list if product not found
    """
    return PRODUCT_RESPONSES.get(product_name, [])


def get_product_images(product_name):
    """
    Get images for a specific product
    
    Args:
        product_name: Name of the product
        
    Returns:
        List of image URLs, or empty list if no images available
    """
    return PRODUCT_IMAGES.get(product_name, [])
