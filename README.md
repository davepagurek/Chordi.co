# BeatBot
Procedural music, taught with data from real artists

## Dependencies
Check requirements.txt

## Neural Network structure
The following program uses a Feed Forward Neural network that is trained with
midi data to generate a song. There two  hidden layers present and
25 nodes on the first hidden layer and 10 on the second.

## File function
The following files have the corresponding functions.
| File Name | Description |
| --------------------- |
| tomidi.py | Converts an intermediate text file with midi chord data to a midi
file to be played. |
| --------------------- |
| learn.py | Creates an intermediate file from the all the trained data. |
## Chord enumeration
```
-1   (start)
0    M1
1    m1
2    o2
3    m2
4    m3
5    M3
6    m4
7    M4
8    m5
9    M5
10   M5^7
11   m6
12   M6
13   o7
14   (end)
```

## Basic music theory
```
Major:
1 2 3 4 5 6 7
M m m M M m o

Natural minor:
1 2 3 4 5 6 7
m o M m m M M
```
