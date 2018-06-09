## WHY?
You may ask me why do I use some scripts to generate mongoose schema from .yaml .



This is a test for another project called *ProjectBoost*.
It's purpose to create all boilerplate code from data structre.
So these yaml files will probably be used **for generating GraphQL schemas**

Now dir struct is:

	├──Schem.js 		# auto-generated file with all schemas
	├──BaseNode.coffee 	# base server functions for all nodes
	├──test
	|    └── baseNode.coffee	# tests for base functions
	├──foo			# foder of 'foo' object
	|    ├── fooNode.coffee 	# server functions
	|    ├── foo.js			# mongo schema
	|    ├── foo.yaml		# general structure
	|    └── test
	|        └── foo.coffee		    # testing rules (move to test.coffee??)
	└── bar
	     └── ...

Direction of further devel:

	Name
	├── client.coffee #api for web
	├── server.coffee #functions of server
	├── Schema.js
	├── GraphQL.js
	├── desc.md
	└── test
		└── name.coffee 	#test path

