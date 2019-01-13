# AiiDA tutorials

This repository contains a collection of texts used for
various AiiDA tutorials.

Visit http://ltalirz.github.io/aiida-tutorials

## Building locally

Prerequisites:
- Follow the [jekyll installation instructions](https://jekyllrb.com/docs/installation/) for your operating system
- `cd docs; sudo bundle install`  

Note: If the installation of `nokogiri` is failing, try
```
bundle config build.nokogiri --with-xml2-include=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk/usr/include/libxml2  --use-system-libraries
``` 

Build website locally:
- `bundle exec jekyll serve`
- connect with your browser to `http://127.0.0.1:4000/aiida-tutorials/`

## Acknowledgements

This work is supported by the [MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>)
funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>), as well as by the [MaX
European Centre of Excellence](<http://www.max-centre.eu/>) funded by the Horizon 2020 EINFRA-5 program,
Grant No. 676598.

![MARVEL](docs/assets/images/MARVEL.png)
![MaX](docs/assets/images/MaX.png)
