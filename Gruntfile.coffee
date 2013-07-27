module.exports = (grunt) ->
	# Project configuration
	grunt.initConfig(
		pkg : grunt.file.readJSON('package.json')
		uglify:
			options:
				banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
			app:
				files:
					'app/static/js/lib/date-zh-CN.min.js': ['app/static/js/lib/datejs/date-zh-CN.js']
					'app/static/js/lib/accounting.min.js': ['app/static/js/lib/accounting/accounting.js']
					'app/static/js/app.min.js': ['app/static/js/app.js']
		cssmin:
			compress:
				files:
					'app/static/css/app.min.css': ['app/static/css/app.css']
	)

	# Load the plugins that provide tasks
	grunt.loadNpmTasks('grunt-contrib-uglify')
	grunt.loadNpmTasks('grunt-contrib-cssmin')

	# Default task
	grunt.registerTask 'default', ['uglify', 'cssmin']