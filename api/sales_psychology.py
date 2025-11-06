"""
Sales Psychology Module
Adds urgency, scarcity, and social proof elements to increase conversion
"""
import random


def add_urgency_trigger(price):
    """
    Add urgency messaging based on product price
    
    Args:
        price: Product price
    
    Returns:
        Urgency message or empty string
    """
    if price > 400:
        # High-value items get stronger urgency
        urgency_messages = [
            "🔥 **Limited stock!** Only a few units left at this price!",
            "⚡ **Hot item!** High demand - don't wait too long!",
            "🎯 **Premium pick** - These don't last long in stock!"
        ]
        return "\n\n" + random.choice(urgency_messages)
    elif price > 150:
        # Mid-range items
        urgency_messages = [
            "🔥 **Popular choice!** Stock is moving fast!",
            "⏰ **Trending now** - grab it while available!",
            "💫 **In demand** - order soon to secure yours!"
        ]
        return "\n\n" + random.choice(urgency_messages)
    else:
        # Budget items - subtle urgency
        if random.random() < 0.5:  # 50% chance
            return "\n\n🔥 **Popular choice!** Stock is moving fast!"
        else:
            return ""


def add_scarcity_message(price):
    """
    Add scarcity messaging based on price tier
    
    Args:
        price: Product price
    
    Returns:
        Scarcity message or empty string
    """
    if price > 300:
        return "🔥 **Limited availability** at this price! These premium items sell out quickly."
    elif price > 100:
        return "💰 **Best value** in its category! Popular choice among smart shoppers."
    else:
        return "⭐ **Unbeatable price** - thousands of happy customers!"


def add_social_proof(price):
    """
    Add social proof elements based on product price tier
    
    Args:
        price: Product price
    
    Returns:
        Social proof message
    """
    if price < 50:
        # Budget items - emphasize volume and ratings
        social_proof_options = [
            "⭐ **4.8/5 stars** from 2,000+ happy customers!",
            "🔥 **Bestseller!** Over 5,000 sold this month!",
            "💯 **95% recommend** this to friends and family!",
            "🎯 **Top seller** - Customer favorite for a reason!"
        ]
    elif price < 200:
        # Mid-range items - emphasize quality ratings
        social_proof_options = [
            "⭐ **Customer favorite!** Rated 4.7/5 by hundreds of users!",
            "🏆 **Top rated** in its category!",
            "💬 **Customers love it:** 'Best purchase I've made!'",
            "🌟 **Highly recommended** by tech enthusiasts!"
        ]
    else:
        # Premium items - emphasize exclusivity and expert endorsements
        social_proof_options = [
            "💎 **Premium choice** - Loved by professionals!",
            "🏅 **Award-winning** design and performance!",
            "👑 **Elite tier** - Top 1% in customer satisfaction!",
            "⭐ **Expert-approved** - Featured in tech reviews!"
        ]
    
    return "\n\n" + random.choice(social_proof_options)


def add_value_proposition(price):
    """
    Add value messaging to justify the price
    
    Args:
        price: Product price
    
    Returns:
        Value proposition message
    """
    if price > 400:
        return "\n\n✨ **Premium Investment:** Quality that lasts + warranty protection = Long-term value!"
    elif price > 150:
        return "\n\n💰 **Smart Purchase:** Great quality at a fair price - you won't regret it!"
    else:
        return "\n\n🎁 **Affordable Excellence:** Amazing quality without breaking the bank!"


def enhance_product_response(base_response, price, add_social=True, include_urgency=True):
    """
    Enhance a product response with sales psychology elements
    
    Args:
        base_response: Base product description
        price: Product price
        add_social: Whether to add social proof
        include_urgency: Whether to add urgency messaging
    
    Returns:
        Enhanced response with psychology triggers
    """
    enhanced = base_response
    
    # Add social proof (random 70% of the time to avoid repetition)
    if add_social and random.random() < 0.7:
        enhanced += add_social_proof(price)
    
    # Add urgency trigger based on price
    if include_urgency:
        enhanced += add_urgency_trigger(price)
    
    return enhanced


def get_buying_intent_message(product_name, price):
    """
    Generate persuasive message when user shows buying intent
    
    Args:
        product_name: Name of the product
        price: Product price
    
    Returns:
        Persuasive buying message
    """
    base_message = f"""That's awesome! The {product_name} is a fantastic choice! 🎉

**Ready to purchase?** Here's what happens next:

✅ **30-day money-back guarantee** (love it or return it!)
✅ **1-year warranty included** (full protection)
✅ **Fast shipping** (arrives in 3-5 business days)
✅ **Secure checkout** (your data is safe)
"""
    
    # Add urgency for higher-priced items
    if price > 200:
        base_message += "\n🔥 **Great timing!** Limited stock available."
    
    # Always add contact info
    base_message += "\n\n📞 **To complete your order:** Contact @Store_help_bot and mention this product!"
    
    return base_message
