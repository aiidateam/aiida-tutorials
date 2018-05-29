# AiiDA tutorials

Visit http://ltalirz.github.io/aiida-tutorials

## Building locally

Prerequisites:
- ruby >= 2.1.0
  - Homebrew on Mac: 'brew install ruby'
  - Macports on Mac: 'sudo port install ruby25'
- `gem install bundler --user`  
- `cd docs; bundle install`  

Note: If the installation of `nokogiri` is failing, try
```
bundle config build.nokogiri --with-xml2-include=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk/usr/include/libxml2  --use-system-libraries
``` 

Build website locally:
- `bundle exec jekyll serve`
- connect with your browser to `http://localhost:4000`
