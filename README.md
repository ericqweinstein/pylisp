PyLisp
======

A little LISP written in Python, based on work by [Anton Davydov](https://github.com/davydovanton/rlisp) and [Mary Rose Cook](https://github.com/maryrosecook/littlelisp
).

## Requirements
* [Python 3+](https://www.python.org/)

## Installation
`$ git clone git@github.com:ericqweinstein/pylisp.git`

## Usage
`$ cd pylisp && python main.py`

## Examples
I originally created this as a [Repl.it tutorial](https://repl.it/talk/learn/PyLisp-LISP-in-Just-Over-100-Lines-of-Python/6712). You can [try it out there](https://repl.it/@ericqweinstein/PyLisp) or run locally (see instructions above).

```lisp
(define pi 3.14159)
(define square (lambda (x) (* x x)))
(define circle-area (lambda (r) (* pi (square r))))
(circle-area 100)
```

## Contributing
1. Branch (`$ git checkout -b fancy-new-feature`)
2. Commit (`$ git commit -m "Fanciness!"`)
3. Push (`$ git push origin fancy-new-feature`)
4. Ye Olde Pulle Requeste
