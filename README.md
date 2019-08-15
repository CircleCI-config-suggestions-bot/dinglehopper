dinglehopper
============

dinglehopper is an OCR evaluation tool and reads ALTO, PAGE and text files.

![Travis CI badge](https://api.travis-ci.org/qurator-spk/dinglehopper.svg?branch=master)

Goals
-----
* Useful
  * As an UI tool
  * For an automated evaluation
  * As a library
* Unicode support

Usage
-----
~~~
dinglehopper some-document.gt.page.xml some-document.ocr.alto.xml
~~~
This generates `report.html` and `report.json`.


As a OCR-D processor:
~~~
ocrd-dinglehopper -m mets.xml -I OCR-D-GT-PAGE,OCR-D-OCR-TESS -O OCR-D-OCR-TESS-EVAL
~~~
This generates HTML and JSON reports in the `OCR-D-OCR-TESS-EVAL` filegroup.


![dinglehopper displaying metrics and character differences](.screenshots/dinglehopper.png?raw=true)