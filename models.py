from fuzzywuzzy import fuzz
import os
import PyPDF2
import docx

class pdf_Check():
    def __init__(self, path):
        self.list_files = []
        if not os.path.exists(path) or path is None:
            raise FileNotFoundError(f"The path '{path}' does not exist.")
        elif os.path.isfile(path):
            self.list_files.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(('.pdf', '.docx')) and not file.startswith('~') and '$' not in file:
                        self.list_files.append(os.path.join(root, file))

        else:
            raise ValueError(f"The path '{path}' is neither a file nor a directory.")
    def check_it(self,word,threshold):
        results={}
        for file_name in self.list_files:
            file, file_extension = os.path.splitext(file_name)
            if file_extension.lower() == '.pdf':
                out=pdf_Check.search_keyword_in_pdf(file_name,word,threshold)
                results[str(file_name)]=out
            elif file_extension.lower() == '.docx':
                out=pdf_Check.search_keyword_in_docx(file_name,word,threshold)
                results[str(file_name)]=out
            else:
                pass
        return results
    @staticmethod
    def search_keyword_in_docx(docx_file, keyword,threshold):
        doc = docx.Document(docx_file)
        results=[]
        for i,paragraph in enumerate(doc.paragraphs):
            if fuzz.token_set_ratio(keyword, paragraph.text) >= threshold:
                results.append(i)
        return results
    @staticmethod
    def search_keyword_in_pdf(pdf_file, keyword,threshold):
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            results = []
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                if fuzz.token_set_ratio(keyword, text) >= threshold:  
                    results.append(page_num+1)
        return results
    @staticmethod
    def search_files_for_keyword(directory, keyword,threshold):
        pass
        