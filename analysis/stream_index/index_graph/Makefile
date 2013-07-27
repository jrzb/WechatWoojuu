all:enforcetab pythoncheck shelltest
ifeq ('$(shell uname)', 'Darwin')
  logcheck_command=find ./log -name '*.log*' -type f -print0 | xargs -0 grep -inH -e 'error' | wc -l | grep '^[ ]*0'
  logcheck_detail=find ./log -name '*.log*' -type f -print0 | xargs -0 grep -inH -e 'error' | tail -n 20
else
  logcheck_command=find ./log -name '*.log*' -type f -print0 | xargs -0 -e grep -inH -e 'error' | wc -l | grep '^[ ]*0'
  logcheck_detail=find ./log -name '*.log*' -type f -print0 | xargs -0 -e grep -inH -e 'error' | tail -n 20
endif

pythonindex_check_command=find . -name "*.py" -type f -print0 | xargs -0 grep -inH -e "^ " | wc -l | grep '^[ ]*0'
pythonindex_check_detail=find . -name "*.py" -type f -print0 | xargs -0 grep -inH -e "^ "

pythoncheck:
	@for f in `find . -iname "*.py"`; do\
		pylint -E $$f;\
	done

enforcetab:
	$(pythonindex_check_command) || ($(pythonindex_check_detail) && false)

shelltest:
	./test.sh 8091

logcheck:
	$(logcheck_command) || ($(logcheck_detail) && false)

unitcheck:
	python -c "import eventtrigger; eventtrigger.get_message('queue1', 'localhost')"
