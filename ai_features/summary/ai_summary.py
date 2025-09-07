# import PyPDF2
# import google.generativeai as genai
# import os
# import sys

# def extract_text_from_pdf(pdf_path):
#     """Extract text from PDF file"""
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text() + "\n"
#             return text
#     except Exception as e:
#         print(f"Error reading PDF: {e}")
#         return None

# def summarize_text_with_gemini(text, chunk_size=30000):
#     """
#     Summarize text using Google's Gemini AI with chunking for long texts
#     """
#     # Configure Gemini API
#     api_key = os.getenv('GEMINI_API_KEY')
#     if not api_key:
#         print("Error: GEMINI_API_KEY environment variable not set!")
#         print("Please set your Gemini API key using:")
#         print("set GEMINI_API_KEY=your_api_key_here (Windows)")
#         print("or export GEMINI_API_KEY=your_api_key_here (Linux/Mac)")
#         return None
    
#     genai.configure(api_key=api_key)
    
#     # Initialize the model
#     model = genai.GenerativeModel('gemini-pro')
    
#     print(f"Text length: {len(text)} characters")
    
#     # If text is too long, split into chunks
#     if len(text) > chunk_size:
#         print("Text is long, splitting into chunks...")
#         chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
#         summaries = []
        
#         for i, chunk in enumerate(chunks):
#             print(f"Processing chunk {i+1}/{len(chunks)}...")
            
#             prompt = f"""
#             Please provide a comprehensive summary of the following text. 
#             Focus on the main points, key findings, and important details.
            
#             Text to summarize:
#             {chunk}
#             """
            
#             try:
#                 response = model.generate_content(prompt)
#                 summaries.append(response.text)
#                 print(f"Chunk {i+1} summarized successfully!")
#             except Exception as e:
#                 print(f"Error processing chunk {i+1}: {e}")
#                 summaries.append(f"Chunk {i+1} could not be processed due to error.")
        
#         # Summarize the summaries
#         print("Combining chunk summaries...")
#         final_summary_prompt = f"""
#         Combine and synthesize these partial summaries into one cohesive, comprehensive summary:
        
#         {''.join(summaries)}
#         """
        
#         try:
#             final_response = model.generate_content(final_summary_prompt)
#             return final_response.text
#         except Exception as e:
#             print(f"Error creating final summary: {e}")
#             return " ".join(summaries)
    
#     else:
#         # For shorter texts
#         print("Generating summary...")
#         prompt = f"""
#         Please provide a comprehensive summary of the following text. 
#         Focus on the main points, key findings, and important details.
        
#         Text to summarize:
#         {text}
#         """
        
#         try:
#             response = model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             print(f"Error generating summary: {e}")
#             return f"Summary generation failed: {str(e)}"

# def main():
#     """Main function to run the PDF summarization"""
#     print("=== PDF Text Summarization using Gemini AI ===")
    
#     # Ask for PDF file path
#     pdf_path = input("Please enter the path to your PDF file: ").strip().strip('"')
    
#     # Check if file exists
#     if not os.path.exists(pdf_path):
#         print(f"Error: File '{pdf_path}' not found!")
#         return
    
#     print("Extracting text from PDF...")
#     pdf_text = extract_text_from_pdf(pdf_path)
    
#     if not pdf_text:
#         print("Failed to extract text from PDF.")
#         return
    
#     print(f"Extracted {len(pdf_text)} characters of text.")
    
#     # Check if text is too short
#     if len(pdf_text.strip()) < 100:
#         print("Warning: Very little text extracted from PDF. The PDF might be scanned or image-based.")
#         proceed = input("Continue anyway? (y/n): ").lower()
#         if proceed != 'y':
#             return
    
#     print("Generating summary using Gemini AI...")
#     summary = summarize_text_with_gemini(pdf_text)
    
#     if summary:
#         print("\n" + "="*50)
#         print("SUMMARY:")
#         print("="*50)
#         print(summary)
#         print("="*50)
        
#         # Option to save summary to file
#         save_file = input("\nWould you like to save the summary to a file? (y/n): ").lower()
#         if save_file == 'y':
#             output_path = os.path.splitext(pdf_path)[0] + "_summary.txt"
#             with open(output_path, 'w', encoding='utf-8') as f:
#                 f.write(summary)
#             print(f"Summary saved to: {output_path}")
#     else:
#         print("Failed to generate summary.")

# if __name__ == "__main__":
#     main()


# summarizer.py
from transformers import pipeline

# Initialize Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=200, min_length=50):
    """
    Summarizes the given text using a pre-trained transformer model.
    
    Args:
        text (str): The input text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.
    
    Returns:
        str: The summarized text.
    """
    # Hugging Face models have input token limits (~1024 tokens for BART)
    # So we truncate the text if it's too long
    if len(text) > 2000:
        text = text[:2000]

    summary = summarizer(
        text, 
        max_length=max_length, 
        min_length=min_length, 
        do_sample=False
    )

    return summary[0]['summary_text']
