source=./mystyles.scss
target=../app/feeds/static/feeds/css/style.css

watch:
	clear
	sass --sourcemap=none --watch $(source):$(target)

build:
	clear
	sass --sourcemap=none $(source):$(target)

sourcemap:
	clear
	sass --sourcemap=inline --watch $(source):$(target)
