"""
Simple keyword-based category predictor.
Matches expense descriptions to categories using keyword dictionaries.
No machine learning — easy to understand and extend.
"""

# Dictionary mapping category names to their keywords
CATEGORY_KEYWORDS = {
    'Food': [
        'pizza', 'burger', 'restaurant', 'food', 'biryani', 'coffee', 'tea',
        'snacks', 'lunch', 'dinner', 'breakfast', 'cafe', 'hotel', 'eat',
        'meal', 'rice', 'roti', 'dosa', 'idli', 'juice', 'milk', 'bread',
        'grocery', 'groceries', 'sweets', 'chocolate', 'biscuit', 'chips',
        'sandwich', 'noodles', 'pasta', 'soup', 'ice cream', 'bakery'
    ],
    'Travel': [
        'uber', 'ola', 'bus', 'train', 'taxi', 'petrol', 'fuel', 'metro',
        'auto', 'rickshaw', 'flight', 'air', 'travel', 'trip', 'cab',
        'parking', 'toll', 'railway', 'airport', 'ride', 'ticket', 'fare',
        'diesel', 'rapido', 'swift', 'carpool'
    ],
    'Shopping': [
        'amazon', 'flipkart', 'clothes', 'shopping', 'shoes', 'shirt',
        'pant', 'dress', 'jeans', 'jacket', 'bag', 'watch', 'accessories',
        'myntra', 'meesho', 'ajio', 'zara', 'h&m', 'mall', 'store',
        'fashion', 'cosmetics', 'perfume', 'wallet'
    ],
    'Education': [
        'book', 'course', 'college', 'school', 'udemy', 'education',
        'tutorial', 'class', 'fees', 'exam', 'study', 'notes', 'pen',
        'pencil', 'notebook', 'stationery', 'library', 'university',
        'coaching', 'tuition', 'learning', 'coursera', 'khan', 'nptel'
    ],
    'Entertainment': [
        'movie', 'netflix', 'game', 'gaming', 'cinema', 'theatre',
        'hotstar', 'prime', 'youtube', 'spotify', 'music', 'concert',
        'show', 'event', 'party', 'club', 'subscription', 'amazon prime',
        'disney', 'zee5', 'sonyliv', 'fun', 'amusement', 'play', 'ps5',
        'xbox', 'steam'
    ],
    'Bills': [
        'electricity', 'water', 'internet', 'mobile', 'recharge', 'bill',
        'gas', 'maintenance', 'rent', 'wifi', 'broadband', 'phone',
        'emi', 'insurance', 'loan', 'tax', 'charges', 'utility', 'airtel',
        'jio', 'bsnl', 'vi', 'vodafone', 'idea', 'postpaid'
    ],
    'Health': [
        'medicine', 'hospital', 'doctor', 'pharmacy', 'medical', 'clinic',
        'health', 'gym', 'fitness', 'yoga', 'tablet', 'injection',
        'blood test', 'scan', 'xray', 'dental', 'eye', 'optician',
        'apollo', 'fortis', 'medplus', 'wellness', 'protein', 'supplement'
    ],
}


def predict_category(description: str) -> str:
    """
    Predict the expense category based on keywords in the description.

    Args:
        description: The expense description text entered by the user.

    Returns:
        A category string. Returns 'Other' if no keyword matches.
    """
    if not description:
        return 'Other'

    # Convert description to lowercase for case-insensitive matching
    description_lower = description.lower()

    # Check each category's keywords against the description
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category

    # No match found — return default category
    return 'Other'
