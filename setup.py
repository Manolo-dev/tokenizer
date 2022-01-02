from setuptools import setup, find_packages

# crée le package et définit ses métadonnées
setup(
    name             = 'tokenizer',
    version          = '1.2',
    plateformes      = 'Windows',
    packages         = find_packages(),
    packages_dir     =  {'' : 'tokenizer'},
    author           = 'sergeLabo',
    description      = 'Python tokenizer',
    #download_url     = 'https://github.com/sergeLabo/pymultilame',
    keywords         =  ['token', 'tokenization', 'language', 'comprehension'],
    long_description = open('README.md').read(),
    classifiers      =  [
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: Windows',
        'Topic :: Tokenization',
        'Topic :: Making language',
        'Topic :: Language comprehension'
    ]
)