---
layout: page
title: Blog 
---


{% for post in site.posts %}
  {% if post.title contains "(OUT-DATED)" %}
  {% else %}
  * [ {{ post.title }} ]({{ post.url }})
  {% endif %}
{% endfor %}
