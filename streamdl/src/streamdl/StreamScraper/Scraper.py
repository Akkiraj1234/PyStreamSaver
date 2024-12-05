from ..utility import requests, json
from ..error import InvalidURLError


class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.data = None
    
    def __enter__(self):
        self.check_interent_conection()
        data = requests.get(self.url)
        
        if data.status_code == 200:
            self.data = data.content.decode("utf-8")
            self.data = self._remove_whitespace(self.data)
        
        else:
            raise ConnectionError("coudent scrape the html conetent")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup any temporary resources or data here
        self.data = None
        return False  # Propagate exceptions if any

    def check_interent_conection(self):
        pass
    
    def _remove_whitespace(self, string: str) -> str:
        """
        Remove all whitespace characters from a string, except those within double quotes.

        This method removes all whitespace characters from the input string, except those
        within double quotes. It preserves whitespace characters that are enclosed within
        double quotes. This can be useful, for example, when extracting text from HTML
        documents where whitespace within certain elements like titles should be preserved.

        Parameters:
            string (str): The input string from which whitespace characters are to be removed.

        Returns:
            str: The modified string with whitespace characters removed, except those within
                double quotes.

        Example:
            >>> instance = ClassName()
            >>> modified_string = instance._remove_whitespace('This is "a string" with whitespace.')
            >>> print(modified_string)
            Thisis"a string"withwhitespace.

        Note:
            This method only removes whitespace characters outside of double quotes. Whitespace
            within double quotes is preserved in the output.
        """
        output = ''
        remove = True
        for char in string:
            if char == '"':
                remove = not remove #if true then became false if false then beacme true
            if remove:
                if char in ' \t\n\r\f':
                    continue #continue to the main loop and so it's don't write whitespace in output
            output += char
        return output

    
    def _varify_json_format(self,html_data:str,starting_index:int)->dict|None:
        """
        Verify JSON format within a string.

        Steps:
        1. Check the opening curly bracket to start searching for JSON data. If:
            - The character at the starting index is '{', it proceeds.
            - The character at the starting index is '(' or '=' and the next character is '{', it adjusts the string.
        2. Extract JSON data from the string by iterating through each character, counting opening (+) and closing (-)
        curly brackets. When the count becomes 0, it marks the end of JSON data.
        3. Attempt to load the extracted JSON data. If successful, return the JSON object.
        If it encounters a JSON decoding error, return None.

        Args:
        - html_data (str): The string containing HTML data.
        - starting_index (int): The index to start searching for JSON data.

        Returns:
        - dict | None: The JSON object if successful, otherwise None.

        Time complexity: O(n + k), where n is the length of the string and k is the length of the extracted JSON data.
        Space complexity: O(1) for the function, O(k) for the JSON data."""
        counting_curly_bracket=0
        #step 1
        if html_data[starting_index]=='{':pass
        elif html_data[starting_index]=='('and html_data[starting_index+1]=='{':html_data=html_data[1:]
        elif html_data[starting_index]=='='and html_data[starting_index+1]=='{':html_data=html_data[1:]
        else:return None
        # step 2
        for num,i in enumerate(html_data[starting_index:]):
            if i=='{':
                counting_curly_bracket+=1
            elif i=='}':
                counting_curly_bracket-=1
            if counting_curly_bracket==0:
                ending_index=num
                break
        # step 3
        json_data=html_data[starting_index:starting_index+ending_index+1]
        try:return json.loads(json_data)
        except json.JSONDecodeError:return None
    
    def _finding_data(self,html_data:str,search:str)->int|None:
        """
        Find the word in a document and return its index.

        Args:
        - html_data (str): The string to search in.
        - search (str): The word to search for.

        Returns:
        - int | None: The index of the word if found, otherwise None.

        It iterates through the characters of the string, comparing them with the characters of the word.
        If a match is found, it increments the index counter. If the length of the word and the index counter is equal,
        return the index; otherwise, return None.

        Time complexity: O(n)
        Space complexity: O(1)
        """
        index=0
        length=len(search)
        for num,item in enumerate(html_data,start=0):
            if item==search[index]:
                index+=1
            else:
                index=0
                
            if index==length:
                return num+1
        return None
    
    def _getting_data(self,html_data:str,search)->dict|None:
        """
        Return searched data if found, otherwise return None.

        Args:
        - html_data (str): The entire string containing the data.
        - search (str): The search word.

        Returns:
        - dict | None: The searched data if found, otherwise None.

        It tries to find the index of the first matched object in an HTML document, starting from index 0.
        If no match is found, it returns None. If a match is found, it checks if the matched object belongs to a JSON file.
        If it is JSON, it returns the JSON object; otherwise, it increases the index to the index found and searches again.
        If JSON data is found during this process, it returns it.

        """
        index=0
        while True:
            index_fond=self._finding_data(html_data[index:],search)
            if index_fond is None:
                return None
            
            data=self._varify_json_format(html_data[index:],index_fond)
            if not data:
                index+=index_fond
            else:
                return data