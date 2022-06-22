import re
import pandas as pd
import pyphen
import matplotlib.pyplot as plt
import seaborn as sns

class TranscriptPlotter:
    
    # text should take the form of 
    # <b> TITLE </b> content <b> TITLE2 </b> content2 <b> ...
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.text = f.read()
            
    def convert_to_plot(self):
        self.parse_data()
        self.filter_characters()
        self.clean_content()
        self.hyphenation()
        return self.plot()
   
    # 1. split by <b>
    # 2. strip and remove spacing (removes outer edges + strange transitions)
    # 3. For each in list, split by </b>
    # 4. strip and remove spacing, should have only two items
    # 5. add two items correspondingly to dataframe
    def parse_data(self):           
        titles = []
        contents = []

        chunks = re.split(r"<b>", self.text)
        chunks = list(filter(lambda c: c, [c.strip() for c in chunks]))
        for c in chunks:
            unparsed_line = re.split(r"<\/b>", c)
            parsed_line = [l.strip() for l in unparsed_line]
            titles.append(parsed_line[0])
            contents.append(parsed_line[1])

        self.df = pd.DataFrame({'title': titles, 'content': contents})
    
    # filters titles for just characters and CUTs
    def filter_characters(self):
        df = self.df

        # remove things with parentheses like (PAUSE), (BREAK), and other cut off phrases
        df = df[~df['title'].str.contains(r'^\(.*\)$')]
        # remove page numbers
        df = df[~df['title'].str.contains(r'\d+\.')]
        # remove indicators that end with :
        df = df[~df['title'].str.endswith(':')]
        # take first word of each title phrase (cleans things like 'Mark (V.O)', replaces with 'Mark')
        df['title'] = df['title'].apply(lambda p: p.strip().split(' ')[0])
        # remove common non-character operations, which all end with . for the fist word (like INT.)
        df = df[~df['title'].str.endswith('.')]
        # if not in top 20 list of chars, then don't include, used to exclude any outliers
        top_20 = df['title'].value_counts()[:20]
        df = df[df['title'].isin(top_20.keys())]
        
        self.df = df
    
    # cleans and readies character lines 
    def clean_content(self):
        # converting lines into single string for parsing
        self.df['content'] = self.df['content'].apply(lambda l: ' '.join([line.strip() for line in l.split('\n')]))

    # Performing hyphenation
    # hyphenation adds hyphens between words
    # 1. For each content chunk:
    #   2. Split by space to get each word
    #   3. hyphenate and count number of hyphens + 1
    #   4. Sum them up 
    def hyphenation(self):
        pyphen.language_fallback('nl_NL_variant1')
        dic = pyphen.Pyphen(lang='nl_NL')
        
        def hyphenate(word):
            return dic.inserted(word)
        
        def count_hyphens(line):
            words = line.split(' ')
            return sum([hyphenate(word).count('-') + 1 for word in words])

        self.df['syllables'] = self.df['content'].apply(count_hyphens);

    def plot(self):
        # Get color map
        color_labels = self.df['title'].unique()
        rgb_values = sns.color_palette("Set2", 20)
        color_map = dict(zip(color_labels, rgb_values))

        plt.figure(figsize=(32,10)) # Make it 14x7 inch
        plt.style.use('seaborn-whitegrid') # nice and clean grid

        plt.bar(x=range(0, len(self.df['syllables'])), height=self.df['syllables'], color=self.df['title'].map(color_map)) 

        plt.legend([plt.Rectangle((0, 0), 1, 1, color=color_map[label]) for label in color_labels], color_labels)

        plt.title('The Social Network') 
        plt.xlabel('Line Number') 
        plt.ylabel('Syllables') 
        plt.show()