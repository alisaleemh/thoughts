# Thoughts
Thoughts is a multi-user blogging website where peope can share their thoughts and mind. Registered users can _"Like"_ & _"Comment"_ on the posts. The live site can be visited here: thoughts-blog.appspot.com

# Table of Contents
1. [How to deploy the app?](#deploy-app)
2. [Directory Structure](#directory-structure)
3. [Resources Used](#resources)
4. [Future Improvements](#future-improvements)

### <a name="deploy-app"></a>2. How to deploy the app ?
Follow the steps below to run the app :

1. Download Google App Engine Console
2. Clone the repository from https://github.com/ghoshabhi/Multi-User-Blog.git
3. To run locally :
	* Unzip the contents from the cloned directory and find the file _"app.yaml"_.
	* Open the app engine console and choose the option _"Add an existing application"_ from the Menu bar.
	* Navigate to the location where the repo was cloned.
	* Click the *_"Run"_* button and navigate to the port mentioned for the app in the app engine console. If this is the first time you're running the app you will have the site open at : localhost:8080
4. If you want to visit the live hosted app, visit this URL : your-own-blog.appspot.com

### <a name="directory-structure"></a>3. Directory Structure

```
|__
   |__ handlers
      |__ blogfront.py
      |__ bloghandler.py
      |__ ...
   |__ models
      |__ comment.py
      |__ like.py
      |__ post.py
      |__ user.py
      |__ ...
   |__ static
      |__ css  
						   |__ bootstrap.css
						   |__ boostrap.min.css
						   |__ ...
      |__ fonts
			         |__ font-awesome
							 |__ ...
      |__ img
						   |__ ...
      |__ js
							 |__jquery
							 |__...
   |__ templates
      |__ base.html
      |__ comment.html
      |__ editcomment.html
      |__ ...
   |__ app.yaml
   |__ blog.py
   |__ docorators.py
   |__ helpers.py
   |__ index.yaml
	 |__ README.mdS
```

1. **static :** This folder contains all the CSS/JS/Image resources
2. **views :** This folder contains all the template files.
3. **models:** Contains schema definitaions for all the models
4. **handlers:** Contains handlers to handle each individual route
5. **utility:** Has helper functions and jinja filters
6. **app.yaml :** Has all the app configurations
7. **favicon.ico :** The website icon seen in the tab
8. **find_utf8.py :** Utility script written to remove the UTF8 characters from a file
9. **index.yaml :** Contains index definitions
10. **main.py :** Houses the routing configurations and runs the webapp

### <a name="resources"></a> 4. Resources

* Python is used as the scripting language for the server
* `jinja2`, a templating library for Python & natively implemented in Google App Engine
   `webapp2`, GAE's main library
* `ndb` : The Google Datastore NDB Client Library allows App Engine Python apps to connect to Cloud Datastore.
* `hmac`, `hlib` to enable encryption
* `re` to enable Regular Expression check for email and password inputs
* Front-end frameworks : HTML,CSS, jQuery, clippy.js, TinyMCE editor, toastr.js
* App Engine : Google App Engine (GAE), Google's platform as a service solution

### <a name="future-improvements"></a> 5. Future Improvements

* Use `ndb.BlobKeyProperty` for Photo uploads
* Implement `tags` for each post
* Show posts according to dates
* Filter by `tags`, `dates` and `author`

_Any suggestions to the site are welcomed. Please email me at abhighosh18@gmail.com to share your suggestions_
