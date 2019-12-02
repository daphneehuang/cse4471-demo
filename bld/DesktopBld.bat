:: EXE install script for the Github Scraper
pushd %~dp0
cd ../github_scraper
pyinstaller -y --onefile -n githubscraper __main__.py
popd