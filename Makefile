check-code:
	@black --line-length 79 --check --diff ./wallpaperdownloader
	@pylint --rcfile=./.pylint.rc ./wallpaperdownloader

install-dev:
	@pip install -r requirements-dev.txt
	@pip install -r requirements.txt

build-package:
	python setup.py sdist bdist_wheel
	cp ./dist/wallpaperdownloader-*.tar.gz ./dist/wallpaperdownloader.tar.gz

test:
	pytest -v