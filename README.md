# clog
CLI working time tracker.<br>
Visualize your effort.<br>
Expose your laziness.<br>
Statistics never lie.

## Dependencies
- Python >= 3.10
- [rich](https://github.com/textualize/rich)

## Installation
Clone this repo and run `pip install .`.

```sh
$ git clone https://github.com/ryota0527/clog.git .
$ cd clog
$ pip install .
```

## Usage
Register some categories of your work, e.g.
```sh
$ clog add reading
$ clog add research
$ clog add meeting
```

Make sure to start tracking when you start working:
```sh
$ clog start (category)
```

When you finished, stop tracking:
```sh
$ clog stop
```

To check the statistics of your working time, run:
```sh
$ clog show
```
