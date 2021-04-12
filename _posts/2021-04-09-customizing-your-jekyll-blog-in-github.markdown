---
layout: post
title:  "Customizing your Jekyll blog in Github: support for tags (without external plugins), Latex math formulas, comments section"
date:   2021-04-09 13:06:03 +0200
categories: jekyll update
tags: jekyll blog
---
Setting up a blog in Github with [Jekyll][jekyll-docs] is a reasonably painless experience (thanks in part to the comprenhensive [Github documentation][github-jekyll-docs]). However, there are a few features that do not come 'out of the box':

* No support for post tagging, or tag index pages (each one showing the posts tagged with an individual tag), without external plugins.

* No way to render math formulas out of the box

* As is usual in static blog generators, support for a comments section requires a third party solution.

In this post, we'll try to fix these issues...

## Tag support (without external plugin dependency)

This solution is based on an original [post][christian-specht-post] at  [Christian Specht's site][christian-specht-site]. I've added a small Python3 script that automates the task of regenerating tag index pages, and a small Liquid snippet to add to your post layout that will display links to the tag
indexes that are used in the current post page.


* Add tags to your posts markdown, in the frontmatter _**tags**_ property (only single-word tags are supported)

{% highlight plaintext %}
---
layout: post
title:  "Customizing your Jekyll blog in Github: support for tags (without external plugins), Latex math formulas, comments section"
date:   2021-04-09 13:06:03 +0200
categories: jekyll update
tags: jekyll blog
---
{% endhighlight %}

For example, this post has been tagged with `jekyll` and `blog`.

* Create a new `tabpage.html` layout in `./_layouts':
{% highlight html %}
{% raw %}
---
layout: default
---

<h1>{{ page.tag }}</h1>

<ul>
{% for post in site.tags[page.tag] %}
  <li>
    {{ post.date | date: "%B %d, %Y" }}: <a href="{{ post.url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>
{% endraw %}
{% endhighlight %}

This layout will be used for tags index pages: each one will show links to all the posts that
contain the tag.

* Add the following in your `./layouts/post.html` layout:
{% highlight html %}
{% raw %}
{% if page.tags %}
  <small>tags 
  {% for tag in page.tags %}
    {% for site_tag in site.tags %}
      {% if tag == site_tag[0] %}
        <em><a href="/tags/{{ tag }}/index.html">{{ tag }}</a></em>
      {% endif %}
    {% endfor %}
  {% endfor %}
  </small>
{% endif %}
{% endraw %}
{% endhighlight %}

This will show the tags you've used for your post, wherever you placed it in the layout
(In this post, they are located between the Title-author and the main content)

* create  a `refresh_tags.py` script in your site root (Python3): 
{% highlight python %}
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

{% endhighlight %}

* call the refresh_tags.py script (from your site root) prior everytime you add a tag to 
a post:

{% highlight shell %}
>> python refresh_tags.py
{% endhighlight %}

## Adding Latex Math formulas with MathJax

Add the following to the `<head>` section of `_layouts/default.html`:

{% highlight html %}
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({
	  tex2jax: {
	      inlineMath: [['$','$'], ['\\(','\\)']],
	      processEscapes: true
	  }
      });
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

{% endhighlight %}

You can add then Latex formulas in your markdown: e.g.`$V^2 + D_i$` will render as $V^2 + D_i$

## Comments section in your posts with utterances:

[utterances][utterance-site] allows you to add comments in your post that are stored as GitHub issues. People wanting to comment on your posts
will need a GitHub account (which is almost a feature, rather than a drawback :blush: ). Setup couldn't be easier: just add the following script call
to your `./_posts/post.html` layout, where you want the comment section to be (change your username/reponame to your Github user name and the repo name of your site):

{% highlight javascript %}
<script src="https://utteranc.es/client.js"
        repo="username/reponame"
        issue-term="pathname"
        label="💬comment"
        theme="github-dark"
        crossorigin="anonymous"
        async>
</script>
{% endhighlight %}

See [their site][utterance-site] for more information on configuration options.

## Syntax Highlighting

Jekyll supports syntax highlighting. If you write the following in your markdown

{% highlight plaintext %}
{% raw %}
{% highlight python %}
import matplotlib.pyplot as plt
figure(1)
plt([1,2,3],[4,5,6],'ro-')
plt.show()
{% endhighlight %}
{% endraw %}
{% endhighlight %}

it will be rendered as follows

{% highlight python %}
import matplotlib.pyplot as plt
figure(1)
plt([1,2,3],[4,5,6],'ro-')
plt.show()
{% endhighlight %}

To find out the list of supported languages in command line, grep the language you're searching for from rougify, e.g.:

{% highlight plaintext %}
rougify list | grep verilog
verilog: The System Verilog hardware description language
{% endhighlight %}



[github-jekyll-docs]: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll
[jekyll-docs]: https://jekyllrb.com/docs/
[christian-specht-post]: https://christianspecht.de/2014/10/25/separate-pages-per-tag-category-with-jekyll-without-plugins/
[christian-specht-site]: https://christianspecht.de
[utterance-site]: https://utteranc.es/
