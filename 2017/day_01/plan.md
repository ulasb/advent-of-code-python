Plan
1) Read the input file given as a command line argument. If none is given, use input.txt
2) The input file contains a single line of digits. The digits are to be processed in a circular manner. 

There are two parts to this problem. 

Part 1:
1) Go through and keep a running sum of the digits that are the same as the next digit in the list.
2) Once you have exhausted all digits (and checked the last one since the list is circular), print the sum.
3) Test the algorithm against the cases below to validate:
1122 should produce a sum of 3
1111 should produce a sum of 4
1234 should produce a sum of 0
91212129 should produce a sum of 9

Part 2:
1) Go through and keep a running sum of the digits that are the same as the digit halfway around the list.
2) Once you have exhausted all digits (and checked the last one since the list is circular), print the sum.
3) Test the algorithm against the cases below to validate:
1212 should produce a sum of 6
1221 should produce a sum of 0
123425 should produce a sum of 4
123123 should produce a sum of 12
12131415 should produce a sum of 4


