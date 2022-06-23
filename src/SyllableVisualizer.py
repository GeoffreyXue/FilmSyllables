import pandas as pd
import pyphen
import matplotlib.pyplot as plt
import seaborn as sns
import random
import math
import re

class SyllableVisualizer:
    
    # text should take the form of 
    # <b> TITLE </b> content <b> TITLE2 </b> content2 <b> ...
    def __init__(self, path, log=True):
        with open(path, "r", encoding="utf-8") as f:
            self.text = f.read()
        self.log = log
    
    def convert_and_save(self, outputFolder, name):
        if self.log: print(f"parsing {name}...")
        self.parse()
        if self.log: print("finished parsing. generating image...")
        self.save_plot(outputFolder, name)
        if self.log: print(f"finished {name}, saved to {outputFolder}/{name}.png")
            
    def parse(self):
        self.parse_data()
        self.filter_characters()
        self.clean_content()
        self.hyphenation()
   
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
    
    # filters titles for just characters, leave numbers
    def filter_characters(self):
        df = self.df
        
        # remove page numbers
        # df = df[~df['title'].str.contains(r'\d+\.')]
        # remove things ending with .
        # df = df[~df['title'].str.endswith('.')]

        # remove things with parentheses like (PAUSE), (BREAK), and other cut off phrases
        df = df[~df['title'].str.contains(r'^\(.*\)$')]
        # remove indicators that end with :
        df = df[~df['title'].str.endswith(':')]
        # take first word of each title phrase (cleans things like 'Mark (V.O)', replaces with 'Mark')
        df['title'] = df['title'].apply(lambda p: p.strip().split(' ')[0])
        # remove CUT, Internal shots, and External shots
        df = df[~df['title'].str.contains(r'CUT|INT|EXT')]
    
        extra = df[df['title'].str.contains(r'\d+\.$')]

        # if not in top 20 list of chars, then don't include, used to exclude any outliers
        top_20 = df['title'].value_counts()[:20].append(extra['title'].value_counts())
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

    def save_plot(self, outputFolder, name):
        df = self.df
        # Get color map
        color_labels = df[~df['title'].str.contains(r'\d+\.')]['title'].unique()
        random.shuffle(color_labels)
        rgb_values = sns.color_palette("Spectral", len(color_labels))
        color_map = dict(zip(color_labels, rgb_values))

        indexes = df[df['title'].str.contains(r'\d+\.')].index

        scenes = len(indexes) + 1
        size = math.ceil(math.sqrt(scenes))

        _, ax = plt.subplots(ncols=size, nrows=size, figsize=(size * 4, size * 4))

        def add_bar_plot(ax, data):
            x = data['syllables'].index
            color = data['title'].map(color_map)
            ax.bar(x=x, height=data['syllables'], color=color)
            
            # hide gridded look
            ax.grid(False)
            
            # Hide the right and top spines
            ax.spines.right.set_visible(False)
            ax.spines.top.set_visible(False)

            # Only show ticks on the left and bottom spines
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            
            # assign colors to legend
            chars_in_plot = data['title'].unique()
            ax.legend([plt.Rectangle((0, 0), 1, 1, color=color_map[c]) for c in chars_in_plot], chars_in_plot, loc='upper left')

            ax.set_xlabel('Line Number') 
            ax.set_ylabel('Syllables') 
            
        for i, ax in enumerate(ax.flatten()):
            if i == 0:
                add_bar_plot(ax, df.loc[:indexes[0] - 1])
                continue
            
            if i == len(indexes):
                add_bar_plot(ax, df.loc[indexes[-1] + 1:])
                break

            add_bar_plot(ax, df.loc[indexes[i - 1] + 1:indexes[i] - 1])
        
        plt.title(name)

        plt.tight_layout()
        plt.savefig(f"{outputFolder}/{name}.png", bbox_inches='tight')