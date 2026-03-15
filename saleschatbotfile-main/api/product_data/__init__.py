"""
Product Data Module - Modular Architecture
Centralized imports for all product data components
"""

from .prices import PRODUCT_PRICES
from .specs import PRODUCT_SPECS
from .keywords import PRODUCT_KEYWORDS
from .responses import PRODUCT_RESPONSES
from .images import PRODUCT_IMAGES
from .utils import (
    detect_product,
    get_all_products,
    get_product_price,
    get_product_spec,
    get_product_responses,
    get_product_images
)

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
