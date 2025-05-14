
import re
from unidecode import unidecode

# Mapping of abbreviated forms to their full forms
STREET_ABBR_MAPPING = {
    'g.': 'gatve',
    'd.': 'dambis',
    'bulv.': 'bulvāris',
    'pr.': 'prospekts',
    'šķ. l.': 'šķērslīnija',
    'šķ l.': 'šķērslīnija',
    'l.': 'līnija',
    'šķ.': 'šķērslīnija',
    'šķ': 'šķērslīnija',
    #'kor.': 'korpuss',
    #'kor': 'korpuss',
    #'k-': 'korpuss',
    #'k': 'korpuss',
}

# Mapping of street name initials to their full forms
STREET_INITIALS_MAPPING = {
    'M.': 'Mazā',
    #'V.': 'Vecā',
    #'J.': 'Jaunā'
}

# List of initials to remove if they're not expanded
INITIALS = ['V.','J.']

# Mapping for building corpus notations to standardize to "k" format
KORPUSS_PATTERNS = [
    (r'(\d+)\s+kor(\d+)', r'\1 k\2'),  # "7 kor2" -> "7 k2"
    (r'(\d+)\s+kor\.(\d+)', r'\1 k\2'),  # "7 kor.2" -> "7 k2"
    (r'(\d+)\s+korpuss(\d+)', r'\1 k\2'),  # "7 korpuss2" -> "7 k2"
    (r'(\d+)\s+k-(\d+)', r'\1 k\2'),  # "7 k-2" -> "7 k2"
    (r'(\d+)k(\d+)', r'\1 k\2'),  # "7k2" -> "7 k2"
    (r'(\d+)kor(\d+)', r'\1 k\2'),  # "7kor2" -> "7 k2"
    (r'(\d+)kor\.(\d+)', r'\1 k\2'),  # "7kor.2" -> "7 k2"
    (r'(\d+)korpuss(\d+)', r'\1 k\2'),  # "7korpuss2" -> "7 k2"
    (r'(\d+)k-(\d+)', r'\1 k\2'),  # "7k-2" -> "7 k2"
]

# Additional address simplification patterns
ADDRESS_SIMPLIFICATION_PATTERNS = [
    (r'(\d+)/\d+', r'\1'),  # "74/1" -> "74"
    (r'(\d+)-\d+', r'\1'),  # "258-6" -> "258"
    (r'(\d+)([a-zA-Z]+)', r'\1'),  # "410a" -> "410" (but not affecting "k" cases which are handled separately)
]

def expand_street_abbreviations(address):
    """
    Expands abbreviated street types and street name initials to their full form.

    Args:
        address (str): The address string with possible abbreviations

    Returns:
        str: The address with abbreviations expanded to full form
    """
    # Create a copy of the address to work with
    expanded_address = address

    # Replace each street type abbreviation with its full form
    for abbr, full_form in STREET_ABBR_MAPPING.items():
        # Use word boundaries to ensure we only match complete words
        # We need to handle the case where the abbreviation is at the end of a word
        # or followed by a space and a number
        pattern = r'(\s)' + re.escape(abbr) + r'(\s|$|\d)'
        replacement = r'\1' + full_form + r'\2'
        expanded_address = re.sub(pattern, replacement, ' ' + expanded_address)

        # Remove the extra space we added at the beginning
        expanded_address = expanded_address.lstrip()

    # Replace each street name initial with its full form
    for initial, full_form in STREET_INITIALS_MAPPING.items():
        # Match initials at the beginning of the address or after a space
        # followed by a space (to ensure we're matching initials, not parts of words)
        pattern = r'(^|\s)' + re.escape(initial) + r'\s'
        replacement = r'\1' + full_form + ' '
        expanded_address = re.sub(pattern, replacement, expanded_address)

    return expanded_address

def simplify_address(address):
    # First expand abbreviations to their full forms
    address = expand_street_abbreviations(address)

    # Remove dots after numbers (e.g., "6." -> "6")
    # This will handle all occurrences of dots after numbers in the address
    address = re.sub(r'(\d+)\.(\s)', r'\1\2', address)

    # Standardize building corpus notations (e.g., "kor2" -> "k2", "k-2" -> "k2")
    for pattern, replacement in KORPUSS_PATTERNS:
        address = re.sub(pattern, replacement, address)

    # Apply additional address simplifications
    # We need to handle "k" numbers specially to avoid removing the numbers after "k"

    # First, temporarily replace "k" numbers with a placeholder
    k_pattern = r'(\d+)\s+k(\d+)'
    k_matches = re.finditer(k_pattern, address)
    placeholders = {}

    for i, match in enumerate(k_matches):
        placeholder = f"__K_PLACEHOLDER_{i}__"
        placeholders[placeholder] = match.group(0)
        address = address.replace(match.group(0), placeholder)

    # Now apply the simplification patterns
    for pattern, replacement in ADDRESS_SIMPLIFICATION_PATTERNS:
        address = re.sub(pattern, replacement, address)

    # Restore the "k" number placeholders
    for placeholder, original in placeholders.items():
        address = address.replace(placeholder, original)

    # Improved pattern for initials - match at beginning of words with a dot
    for initial in INITIALS:
        # Match initials at the beginning of the address or after a space
        # This pattern specifically targets initials like "J." at the start of words
        pattern = r'(^|\s)' + re.escape(initial) + r'\s'
        address = re.sub(pattern, r'\1', address)

    # Remove any remaining stopwords with word boundaries
    stopwords = INITIALS
    pattern = r'\b(?:' + '|'.join(re.escape(sw) for sw in stopwords) + r')\b'
    address_clean = re.sub(pattern, '', address)

    address_clean = unidecode(address_clean) #remove regional characters

    # Clean up extra spaces and normalize
    address_clean = re.sub(r'\s+', ' ', address_clean).strip()

    return address_clean


if __name__ == "__main__":
    addresses = [
        "Varavīksnes g. 10",
        "Raņķa d. 5",
        "Latgales 250/3",
        "Latgales+250/3",
        "Vienības g. 87d",
        "Čiekurkalna 4. šķ l. 8",
        "Ganību d. 40a",
        "Kundziņsalas 16. l. 24a",
        "Edžiņa g. 5",
        "Katrīnas d. 24k3",
        "V. Buļļu 10",
        "Vecmīlgrāvja 17/3",
        "Kandavas 8-13",
        "Rigondas g. 1",
        "Vecmīlgrāvja 1. l. 28",
        "Raiņa bulv. 9",
        "V. Buļļu 10",
        "Balasta d. 72",
        "Latgales 256/7",
        "Raņķa d. 5",
        "J. Rancāna 8",
        "Raņķa d. 5",
        "Aspazijas bulv. 30",
        "Vecmīlgrāvja 1. l. 26",
        "Čiekurkalna 4. šķ l. 12 k-2",
        "Čiekurkalna 4. šķ l. 8",
        "M. Nometņu 24",
        "M. Nometņu 24",
        "M. Nometņu 24",
        "Stendes 7 kor2",
        "Jūrmalas g. 108",
        "Vienības g. 186",
        "Brīvības gatve 410a",
        "Latgales 260/7",
        "Salaspils 12/5",
        "Silciema 15/2",
        "J. Vācieša 6",
        "M. Nometņu 24",
        "Ganību d. 15",
        "Silciema 15/2",
        "J. Vācieša 6",
        "Latgales 268/2",
        "Kurzemes pr. 110",
        "Katrīnas d. 20/2",
        "Latgales 258-6",
        "Pavasara g. 6",
        "Kaivas 50/4",
        "Ostas pr. 4-23",
        "Latgales 268/2",
        "Katrīnas d. 27",
        "Katrīnas d. 27",
        "Kaivas 31/3",
        "Vienības g. 126",
        "Krustpils 75k5",
        "Katrīnas d. 27",
        "Pavasara g. 5",
        "Kalpaka bulv. 7",
        "M. Muzeja 1",
        "Dudajeva g. 4",
        "Dudajeva g. 4",
        "Pavasara g. 2",
        "Katrīnas d. 6",
        "M. Stērstu 8",
        "Latgales 258/4",
        "Dzelzavas 74/1",
        "Kalpaka bulv. 9",
        "Raņķa d. 31",
        "Raņķa d. 31",
        "Raņķa d. 31",
        "Valdemāra 72/2",
        "Dudajeva g. 7",
        "Čiekurkalna 7. šķ l. 7",
        "Vienības g. 87",
        "M. Piena 8",
        "Vienības g. 186a",
        "Jaunciema 2. šķ. l. 2",
        "Vecmīlgrāvja 6. l. 2",
        "Deglava 106/2",
        "Vecmīlgrāvja 6. l. 2",
        "Kurzemes pr. 112",
        "Kaivas 50/1",
        "Čiekurkalna 7. šķ l. 7",
        "M. Stērstu 6",
        "M. Stērstu 6",
        "Kurzemes pr. 164",
        "Raiņa bulv. 3",
        "Čiekurkalna 4. šķ l. 12 k-2",
        "Čiekurkalna 7. šķ l. 3",
        "Raiņa bulv. 3",
        "Kalpaka bulv. 7",
        "Kaivas 50/1",
        "Rigondas g. 1",
        "Katrīnas d. 6",
        "Ilūkstes 107/2",
        "Raņķa d. 5",
        "J. Rancāna 8",
        "Raņķa d. 5",
        "Aspazijas bulv. 30",
        "Ganību d. 13 k1",
        "Jūrmalas g. 100/1",
        "Čiekurkalna 4. šķ l. 8",
        "M. Nometņu 24",
        "M. Nometņu 24",
        "M. Nometņu 24",
        "J. Daliņa 4",
        "M. Nometņu 11a",
        "Raņķa d. 34",
        "Rigondas g. 10",
        "Pavasara g. 3",
        "M. Stacijas 4",
        "Latgales 256/7",
        "Raiņa bulv. 2",
        "Meierovica bulv. 4",
        "Jūrmalas g. 100",
        "Raņķa d. 34",
        "Raņķa d. 34",
        "Raņķa d. 34",
        "Čiekurkalna 7. šķ l. 7a",
        "Rigondas g. 7",
        "Salaspils 12/5",
        "Jūrmalas g. 108",
        "Vienības g. 186",
        "Brīvības gatve 410a",
        "Latgales 260/7",
        "M. Nometņu 24",
        "Ganību d. 15",
        "Kurzemes pr. 110",
        "Katrīnas d. 20/2",
        "Latgales 258-6",
        "Pavasara g. 6",
        "Kaivas 50/4",
        "Ostas pr. 4-23",
        "Altonavas 9-6",
        "Čiekurkalna 1. l. 12",
        "Jaunciema g. 182",
        "Kvēles 15/15",
        "Tālavas g. 9"
    ]

    print("Testing Utils class...")

    # Test address expansion
    print("\nTesting address expansion:")
    test_addresses = [
        "Varavīksnes g. 10",
        "Raņķa d. 5",
        "Vienības g. 87d",
        "Čiekurkalna 4. šķ l. 8",
        "Ganību d. 40a",
        "Kundziņsalas 16. l. 24a",
        "Raiņa bulv. 9",
        "Kurzemes pr. 110",
        "M. Nometņu 24",
        "V. Buļļu 10",
        "J. Rancāna 8",
        "J. Vācieša 6",
        "Vecmīlgrāvja 6. linija 2",
        "Stendes 7 kor2",
        "Čiekurkalna 12 k-2",
        "Ganību d. 13 k1",
        "Katrīnas d. 24k3",
        "Krustpils 75k5",
        # Additional test cases for new simplifications
        "Dzelzavas 74/1",
        "Latgales 258-6",
        "Brīvības gatve 410a",
        "Vecmīlgrāvja 17/3",
        "Katrīnas d. 24k3 un Krustpils 75k5"  # Test multiple patterns in one address
    ]

    for address in test_addresses:
        expanded = expand_street_abbreviations(address)
        print(f"Original: {address}")
        print(f"Expanded: {expanded}")
        print(f"Simplified: {simplify_address(address)}")
        print("---")

    # Process all addresses
    print("\nProcessing all addresses:")
    for address in addresses:
        print(simplify_address(address))

