def detect_intent(question):
    """
    Simple keyword-based intent detection.
    Returns one of: 'medical', 'school', 'transportation', 'shopping', 'family', 'unknown'
    """
    q = question.lower()
    
    if any(w in q for w in ['hospital', 'medical', 'doctor', 'clinic', 'emergency']):
        return 'medical'
    elif any(w in q for w in ['school', 'university', 'college', 'education', 'kindergarten']):
        return 'school'
    elif any(w in q for w in ['transport', 'bus', 'train', 'metro', 'subway', 'station']):
        return 'transportation'
    elif any(w in q for w in ['shop', 'mall', 'grocery', 'market', 'store']):
        return 'shopping'
    elif any(w in q for w in ['family', 'kid', 'child']):
        return 'family'
    
    return 'unknown'

def validate_data(context, intent):
    """
    Checks if relevant data exists for the detected intent.
    Returns:
        is_valid (bool): True if data exists and we should proceed to AI
        relevant_data (list): List of dicts containing only relevant info
        message (str): Manual response if invalid, None otherwise
    """
    if not context or not context.get('exists'):
        return False, [], "House not found."

    if intent == 'unknown':
        return False, [], "I can help with nearby hospitals, schools, transportation, and shopping."

    places = context['nearby_places']
    
    if intent == 'family':
        # For family, we check for schools primarily, but maybe parks if we had them.
        # Based on specs, we derive family-friendly from existing data (likely schools).
        relevant = [p for p in places if p['category'] == 'school']
        if not relevant:
             return False, [], "Sorry, that information isn’t available for this property yet."
        return True, relevant, None

    # Direct category matching
    relevant = [p for p in places if p['category'] == intent]
    
    if not relevant:
        return False, [], "Sorry, that information isn’t available for this property yet."
        
    return True, relevant, None
