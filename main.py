import pyphen


pyphen.language_fallback('nl_NL_variant1')
dic = pyphen.Pyphen(lang='nl_NL')
print(dic.inserted('absolutely.'))

# Get Data into usable format

# Get simplified DF transcript