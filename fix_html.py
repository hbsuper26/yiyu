import subprocess

git_content = subprocess.check_output(['git', 'show', '3fb60e9:templates/index.html']).decode('utf-8')

start_idx = git_content.find('<section id="management"')
end_idx = git_content.find('<!-- Success Stories')
sections = git_content[start_idx:end_idx]

with open('templates/index.html', 'r', encoding='utf-8') as f:
    current_content = f.read()

curr_start = current_content.find('<section id="management"')
curr_end = current_content.find('<!-- Success Stories')

if curr_start != -1 and curr_end != -1:
    new_content = current_content[:curr_start] + sections + current_content[curr_end:]
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Fixed HTML!')
else:
    print('Could not find sections in current index.html')
