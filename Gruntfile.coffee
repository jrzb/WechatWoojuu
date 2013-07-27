#---------------------------
# File : Gruntfile.coffee
# Author : liki
# Description : Config file for Gruntjs
# Created : 5/17/13
#---------------------------

'use strict'

module.exports = (grunt) ->
	# Project configuration
	grunt.initConfig(
		pkg : grunt.file.readJSON('package.json')
		uglify:
			options:
				banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
			app:
				files:
					'ui/app/js/app.min.js': ['ui/app/js/app.js']
		cssmin:
			compress:
				files:
					'ui/app/css/app.min.css': ['ui/app/css/app.css'],
					'ui/app/lib/flat-ui/css/flat-ui.min.css': ['ui/app/lib/flat-ui/css/flat-ui.css']
	)

	# Load the plugins that provide tasks
	grunt.loadNpmTasks('grunt-contrib-uglify')
	grunt.loadNpmTasks('grunt-contrib-cssmin')

	# Default task
	grunt.registerTask 'default', ['uglify', 'cssmin']