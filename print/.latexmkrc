# XeLaTeX and index generation are handled by latexmk; no Python is needed here.
$pdf_mode = 5;
$ENV{'TEXINPUTS'} = './_support//:' . ($ENV{'TEXINPUTS'} // '');
$makeindex = 'makeindex -s _support/python.ist %O -o %D %S';
