# Thoughts
Thoughts is a multi-user blogging website where peope can share their thoughts and mind. Registered users can _"Like"_ & _"Comment"_ on the posts. The live site can be visited here: [Thoughts](https://thoughts-blog.appspot.com)


# Table of Contents
1. [Setup and Deployment](#setup)
2. [Directory Structure](#directory-structure)
3. [Technologies Used](#technologies)

### <a name="setup"></a>2. Setup and Deployment
Follow the steps below to run the app :

1. Download and Install the Python SDK for Google App Engine. Follow instuctions at https://cloud.google.com/appengine/downloads
2. Clone the git repository: `git clone https://github.com/alisaleemh/thoughts.git`
3. Run on the local development server:
	* Run `dev_appserver.py <PATH_TO_YOUR_CLONED_REPO>`
	* On your browser navigate to http://localhost:8080/blog
	* To access the Datastore viewer in the locl development console, navigate to http://localhost:8000
	* For more information, please refer to https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server
4. Check the live app here: [Thoughts](https://thoughts-blog.appspot.com)

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
	 |__ README.md
```

1. **static:** This directory contains all CSS, JavaScript libraries as well as static images.
2. **views:** This directory contains all the HTML templates.
3. **models:** This directory contains schema definitions for the Google Datastore models.
4. **handlers:** This directory contains all the handlers handling the requests made by the application.
5. **app.yaml:** The standard Google App Engine configuration file.
6. **index.yaml:** This configuration file specifies custom indexes.
7. **blog.py:** Runs the web application.
8. **helpers.py:** Contains various helper functions such as encryption and hashing.
9. **decorators.py:** Contains various decorators essential for validation and application security.

### <a name="technologies"></a> 4. Technologies

* This application uses Google `webapp2` framework. `webapp2` is a light-weight Python web framework compatible with Google App Engine. You can find more information here: https://webapp2.readthedocs.io/en/latest/guide/handlers.html#handlers-101
* The application utilizes `jinja2` as its templating language. Read more here: http://jinja.pocoo.org/docs/2.9/
* THe front-end utilized the popular `boostrap` framework. Read more: http://getbootstrap.com/
* The application utlizes the Google Cloud Datastore as its database. Google Cloud Datastore is a NoSQL database built for automatic scaling. Read more here: https://cloud.google.com/appengine/docs/standard/python/datastore/
* The application is hosted on Google Cloud Platform. Read more here: https://cloud.google.com/
