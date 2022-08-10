---
layout: post
title: five five-letter words with twenty-five unique letters?
lang: en
lang-ref: five five-letter words with twenty-five unique letters?
tag: computation
---

The content creator [Matt Parker](https://standupmaths.com/) made a YouTube video titled [Can you find: five five-letter words with twenty-five unique letters?](https://www.youtube.com/watch?v=_-AfhLQfb6w&ab_channel=Stand-upMaths).
The essence of the question at hand is how many combinations of five five-letter words exist such that all twenty-five letters are unique.

Matt Parker had engineered a [Python script](https://github.com/standupmaths/fiveletterworda) that could solve this problem in a swift amount of time of 31.95 days.
Let us see if we can do slightly better without making the algorithm too complicated, and hopefully get close to the impressive 1.3 sec of [Shelby Doolittle](https://github.com/shelbyd/fast_fives).

First, let us consider the representation of the words.
A word cannot be in the solution if it contains the same letter multiple times.
The words can thus without problem be represented as a binary where each letter is mapped into individual powers of two, i.e:

| Letter | Number | i in <2^i> |
|--------|--------|------------|
| a      | 1      | 0          |
| b      | 2      | 1          |
| c      | 4      | 2          |
| d      | 8      | 3          |
| e      | 16     | 4          |
| f      | 32     | 5          |
| ...    | ...    | ...        |

The word "fed" is now represented as:

| 0 | 0 | .. | 1 | 1 | 1 | 0 | 0 | 0 |
|   |   |    | f | e | d |   |   |   |

Or as an integer value 8+16+32=56.
Here it should be noted that the ordering of the letters is lost.
Losing the information of the ordering does not matter during computation, because all letters need to be unique, but it requires us to keep the original words to later do the conversion from integer -> word.
It should be obvious that the ordering is lost if we consider the word "deaf".
In the binary representation "deaf" is represented as:

| 0 | 0 | .. | 1 | 1 | 1 | 0 | 0 | 1 |
|   |   |    | f | e | d |   |   | a |

Or as an integer value 1+8+16+32=56.

The prize that is won from representing the words as binaries is that bitwise operations can be performed.
Bitwise operations are often considered to be very computationally efficient.
Now it can be checked if two words have the same letter by applying [bitwise AND](https://en.wikipedia.org/wiki/Bitwise_operation#AND).
If the two words have no letters in common, then the bitwise AND will yield zero.

Now, let's start constructing the code.

The first is how letters are translated to binary values:

{% highlight python %}
alphabet = list("abcdefghijklmnopqrstuvwxyz")
values = [2 ** i for i in range(0, 26)]
letter_to_value = {}
for letter, value in zip(alphabet, values):
    letter_to_value[letter] = value
{% endhighlight %}

In the above code, a dictionary is created that takes a letter and then returns the integer corresponding to the binary for that letter.

Now the words will be loaded in from "words_alpha.txt":

{% highlight python %}
words5 = []
with open("data/words_alpha.txt", "r") as file:
    for line in file.readlines():
        if len(line.strip()) == 5:
            words5.append(line.strip())
words5_purged = []
for word in words5:
    for letter in alphabet:
        if word.count(letter) >= 2:
            break
    else:
        words5_purged.append(word)
{% endhighlight %}

In the above code, all available word is read from the file, and all words that are not five letters long is removed.
Further, all words containing the same letter more than once are also purged.
Removing these words with multiple of the same letter is important to do, before converting to binary. As an example, "a" got the value of 1, and "b" got the value of 2. If a word had two "a"s, then the conversion to binary would give 1+1 -> 2, which would be interpreted as being a "b".

Now the binary form of the words can be constructed:

{% highlight python %}
words5_value = []
value_to_word = {}
for word in words5_purged:
    value = 0
    for letter in word:
        value += letter_to_value[letter]
    if value not in words5_value:
        words5_value.append(value)
    if value not in value_to_word:
        value_to_word[value] = [word]
    else:
        value_to_word[value].append(word)
{% endhighlight %}

"words5_value" is a list of all the words in integer or binary form. Note that this will be shorter than the number of words, because anagrams have the same binary form, as explained earlier.
"value_to_word" is the conversion from the binary back to a word.
This will also keep track of anagrams so that for any found solution of five words, all the solutions coming from the anagrams can be found easily.
As an example 'feral' would have the value 133169, value_to_word[133169] -> [feral, flare], because feral and flare are anangrams.

Now the code that finds all the solutions can be constructed:

{% highlight python %}
num_words = len(words5_value)
solutions = []
for idx1 in range(0, num_words - 4):
    word1 = words5_value[idx1]
    for idx2 in range(idx1 + 1, num_words - 3):
        word2 = words5_value[idx2]
        if (word1 & word2) != 0:
            continue
        cumulative_word2 = word1 ^ word2
        for idx3 in range(idx2 + 1, num_words - 2):
            word3 = words5_value[idx3]
            if (cumulative_word2 & word3) != 0:
                continue
            cumulative_word3 = cumulative_word2 ^ word3
            for idx4 in range(idx3 + 1, num_words - 1):
                word4 = words5_value[idx4]
                if (cumulative_word3 & word4) != 0:
                    continue
                cumulative_word4 = cumulative_word3 ^ word4
                for idx5 in range(idx4 + 1, num_words):
                    word5 = words5_value[idx5]
                    if (cumulative_word4 & word5) != 0:
                        continue
                    solutions.append([word1, word2, word3, word4, word5])
{% endhighlight %}

This is a little bigger chunk of code, but only two things are mostly going on.
The first thing:

{% highlight python %}
if (word1 & word2) != 0:
    continue
{% endhighlight %}

This part is to just go to the next word as the second word when word1 and word2 have one or more letters in common.
This is to avoid going further down in the nesting when the solution is already void.
The second thing:

{% highlight python %}
cumulative_word3 = cumulative_word2 ^ word3
{% endhighlight %}

In the above code-line "^" means bitwise [XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR).
This is used to make a cumulative word that can be used to check other words down the nesting, instead of checking one word at a time.
The alternative many-check code to the above would be:

{% highlight python %}
if (word1 & word4) != 0:
    continue
if (word2 & word4) != 0:
    continue
if (word3 & word4) != 0:
    continue
{% endhighlight %}

The cumulative technique will result in fewer operations overall.
As an example of how the cumulative word works, let's consider the two words "fed" and "cab":

| 0 | 0 | .. | 1 | 1 | 1 | 0 | 0 | 0 |
|   |   |    | f | e | d |   |   |   |

| 0 | 0 | .. | 0 | 0 | 0 | 1 | 1 | 1 |
|   |   |    |   |   |   | c | b | a |

The XOR is now:

| fed: | 0 | 0 | .. | 1 | 1 | 1 | 0 | 0 | 0 |
| cab: | 0 | 0 | .. | 0 | 0 | 0 | 1 | 1 | 1 |
| XOR: | 0 | 0 | .. | 1 | 1 | 1 | 1 | 1 | 1 |

It should be more clear now, that doing bitwise AND on the cumulative word, is the same as doing bitwise AND on all the words one at a time.

The full code can be found here, [five_fiveletter_words_python.py]({{ site.baseurl }}/assets/python_scripts/five_fiveletter_words_python.py)

The run time of the constructed algorithm is 21415 sec which is about ~6 hours.
Which is about 7680 times faster than 32 days, but still 16600 times slower than 1.3 sec.
