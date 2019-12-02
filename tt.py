import githubscraper


#el = githubscraper.get_repo_files("ss5nathan","ss5nathan.github.io")
el = githubscraper.get_all_files_for_user("ss5nathan")
print(el)

for e in el:
    print(e)
print("done")