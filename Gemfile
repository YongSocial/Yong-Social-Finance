source "https://rubygems.org"

# GitHub Pages builds your repo with this gem, which pins Jekyll + the exact
# plugin versions GitHub's servers support. Using it locally guarantees your
# local preview matches what GitHub Pages will actually publish.
gem "github-pages", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

# Windows/JRuby compatibility (harmless on Mac/Linux)
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw]
