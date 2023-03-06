# tbsp

## The Initial Idea
Here are the initial efforts made towards the final project in Cybersecurity
Network Analytics. I began by researching ways to improve performance of the
current implementation of domain name similarity. Instead of using third-party
dependencies to compute strings similarity, I use the edit distance algorithm.
This algorithm takes as input two strings (e.g. two domains) and returns the
minimum number of operations needed to transform the first word to the second. I
then applied a scoring function in order to properly scale the edit distance
with respect to the longest of the two input strings. To explain this idea
further, if one string is 100 characters long, however the edit distance between
it and another string is, say, 50, then the score should be 0.5. This score
essentially says how similar one word is to another. On the other hand, if the
length of the longest word is 20 and it took 20 operations to transform to the
other word, then the score will be 0; the two words are not similar at all.

## Next Steps
My plans for the future include implementing a fully-functional sliding window
mechanism with highly-tuned parameters in order to accelerate runtime while
maintaining some degree of accuracy. The current implementation in HinDom
calculates the string similarity of every pair of with time complexity: 
$$\Omega(n)$$ The edit distance scoring function goes to 0 as the edit 
distance goes to infinity. Therefore, my current implementation of sliding 
windows computes the top k maximum scores per window. I am experimenting with 
window sizes and values of k to find the optimal values to achieve my goal
towards the beginning of this section. Another gaol of mine is to include some
level of feature extraction given a list of domain names. Not only could I
compute edit distance, but also include other string metrics that I have yet to
search for.
