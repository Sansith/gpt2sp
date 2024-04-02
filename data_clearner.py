import re


def remove_jira_syntax(text):
    # Headings
    text = re.sub(r'h[1-6]\.\s+', '', text)

    # Rich text formatting
    effects_patterns = [
        r'\*(.*?)\*',  # bold
        r'_(.*?)_',    # italic
        r'\?\?(.*?)\?\?',  # citation
        r'-(.*?)-',    # deleted
        r'\+(.*?)\+',  # inserted
        r'\^(.*?)\^',  # superscript
        r'~(.*?)~',    # subscript
        r'\{\{(.*?)\}\}',  # monospaced
        r'\{quote\}(.*?)\{quote\}',  # block quote
        r'\{color:[^}]+\}(.*?)\{color\}',  # colored text
    ]
    for pattern in effects_patterns:
        text = re.sub(pattern, r'\1', text)

    # Attached link item syntaxes
    links_patterns = [
        (r'\[.*?\|(.*?)\]', r'\1'),  # remove attached file names 
        (r'\[https?:[^\]]+\]', ''),  # external links
        (r'\[mailto:[^\]]+\]', ''),  # email links
        (r'\[file:[^\]]+\]', ''),    # file links
        (r'\[~[^\]]+\]', '')         # user profile links
    ]

    for pattern, replacement in links_patterns:
        text = re.sub(pattern, replacement, text)


    # attachments
    text = re.sub(r'(![^\s]+?\!)', '', text)  # images
    text = re.sub(r'\{anchor:[^}]+\}', '', text)  # anchors
    text = re.sub(r'\|\|.*?\|\|', '', text)  # table headers
    text = re.sub(r'\|.*?\|', '', text)  # table rows
    text = re.sub(r'\{[^}]+\}', '', text)  # advanced blocks like {panel} or {code}

    # Remove miscellaneous characters and cleanup
    text = re.sub(r'\\[\\@]', '', text)  # Escaped characters
    text = text.replace('----', '')  # Horizontal ruler
    text = re.sub(r'\n{2,}', '\n', text)  # Multiple newlines

    return text


def remove_html_tags(html_text):
    
    pattern = re.compile('<.*?>')
    cleaned_text = re.sub(pattern, '/', html_text)
    cleaned_text = re.sub('\/+', '/', cleaned_text).strip('|')
    return cleaned_text


def clean_text(_text):
    text = str(_text if _text else " ")
    text = remove_jira_syntax(text)
    text = remove_html_tags(text)

    # Remove special characters,
    text = re.sub(r"[\*\-]+", " ", text)
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)


    return text
