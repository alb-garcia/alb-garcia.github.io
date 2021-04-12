#!/usr/bin/env python

# creates index pages for the posts tags in ./tags
# to work, it requires a tagpage.html layout in ./_layouts

import os
import glob

posts = glob.glob('./_posts/*.markdown')
site_tags = set()

for post in posts:
    print(f'-- {post} tags:')
    inside = False
    front_matter = []
    with open(post, 'r') as f:
        for line in f:
            if '---' in line and not inside:
                inside = True # next line is front matter
            elif '---' in line and inside:
                break #front matter finished
            elif inside:
                front_matter.append(line)


    tags = []
    for line in front_matter:
        if 'tags:' in line:
            tags = line.strip().split()[1:]
            print('  ' + ' '.join(tags))
            break
    site_tags = site_tags | set(tags)

for tag in site_tags:
    os.makedirs(f'./tags/{tag}', exist_ok = True)
    with open(f'./tags/{tag}/index.html', 'w') as f:
        s  =  '---\n'
        s +=  'layout: tagpage\n'
        s += f'tag: {tag}\n'
        s +=  '---\n'
        f.write(s)

print('-- tags refreshed.')


        
    
