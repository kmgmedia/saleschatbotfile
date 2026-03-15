"""
Product Data Module - Legacy Compatibility Layer
This file now imports from the modular product_data package
All functionality remains the same - just better organized!

New structure:
- product_data/prices.py - Product pricing
- product_data/specs.py - Product specifications
- product_data/keywords.py - Search keywords
- product_data/responses.py - Response variations
- product_data/images.py - Product images (Cloudinary URLs)
- product_data/utils.py - Helper functions
"""

# Import everything from the modular structure
from .product_data import (
    PRODUCT_PRICES,
    PRODUCT_SPECS,
    PRODUCT_KEYWORDS,
    PRODUCT_RESPONSES,
    PRODUCT_IMAGES,
    detect_product,
    get_all_products,
    get_product_price,
    get_product_spec,
    get_product_responses,
    get_product_images
)

# Export everything for backward compatibility
__all__ = [
    'PRODUCT_PRICES',
    'PRODUCT_SPECS',
    'PRODUCT_KEYWORDS',
    'PRODUCT_RESPONSES',
    'PRODUCT_IMAGES',
    'detect_product',
    'get_all_products',
    'get_product_price',
    'get_product_spec',
    'get_product_responses',
    'get_product_images'
]
