"""Utility functions for text processing."""

# Telegram message length limit
TELEGRAM_MAX_MESSAGE_LENGTH = 4096

def split_text(text, max_length=TELEGRAM_MAX_MESSAGE_LENGTH):
    """Split text into chunks of max_length characters.
    
    This function tries to split text intelligently at paragraph, sentence,
    or word boundaries to avoid cutting in the middle of words or sentences.
    
    Args:
        text (str): The text to split
        max_length (int): Maximum length of each chunk
        
    Returns:
        list: List of text chunks, each under max_length
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by paragraphs first
    paragraphs = text.split("\n\n")
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit
        if len(current_chunk) + len(paragraph) + 2 > max_length:
            # If the current chunk is not empty, add it to chunks
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            # If the paragraph itself is too long, split it further
            if len(paragraph) > max_length:
                # Split by sentences
                sentences = paragraph.replace(". ", ".\n").split("\n")
                
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 2 > max_length:
                        if current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = ""
                        
                        # If the sentence is still too long, split it by words
                        if len(sentence) > max_length:
                            words = sentence.split(" ")
                            for word in words:
                                if len(current_chunk) + len(word) + 1 > max_length:
                                    chunks.append(current_chunk)
                                    current_chunk = word + " "
                                else:
                                    current_chunk += word + " "
                        else:
                            current_chunk = sentence + " "
                    else:
                        if current_chunk and not current_chunk.endswith(" "):
                            current_chunk += " "
                        current_chunk += sentence + " "
            else:
                current_chunk = paragraph
        else:
            # Add paragraph separator if needed
            if current_chunk and not current_chunk.endswith("\n\n"):
                current_chunk += "\n\n"
            current_chunk += paragraph
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks 