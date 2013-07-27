all:enforcetab unitcheck shelltest aimltest pythoncheck logcheck
ifeq ('$(shell uname)', 'Darwin')
  logcheck_command=find ./log -name '*.log*' -type f -print0 | xargs -0 grep -inH -e 'error' | wc -l | grep '^[ ]*0'
  logcheck_detail=find ./log -name '*.log*' -type f -print0 | xargs -0 grep -inH -e 'error' | tail -n 20
else
  logcheck_command=find ./log -name '*.log*' -type f -print0 | xargs -0 -e grep -inH -e 'error' | wc -l | grep '^[ ]*0'
  logcheck_detail=find ./log -name '*.log*' -type f -print0 | xargs -0 -e grep -inH -e 'error' | tail -n 20
endif

pythoncheck:
	@for f in `find . -iname "*.py"`; do\
		pylint -E $$f;\
	done

unitcheck:
	python ./weixin_unittest.py

enforcetab:
	find . -name "*.py" -type f -print0 | xargs -0 grep -inH -e "^ " | wc -l | grep '^[ ]*0'

shelltest:
	./tool/test.sh 5000

aimltest:
	./tool/aiml_chat_test.sh 5000

logcheck:
	$(logcheck_command) || ($(logcheck_detail) && false)
