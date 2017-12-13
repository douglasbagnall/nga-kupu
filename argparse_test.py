import argparse

def function(args):
    with open(args.input) as file, open(args.good_output, 'w') as file2, open(args.bad_output, 'w') as file3:
        text = file.read()
        numberslist = text.split()
        numberslist = [int(number) for number in numberslist]
        file.close()

        file2.write(str(sum(numberslist[:3])))
        file2.close()

        file3.write(str(sum(numberslist[-2:])))
        file3.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help="takes a file containing numbers")
    parser.add_argument('--good_output', '-g', help="writes the sum of the first 3 numbers to a new file")
    parser.add_argument('--bad_output', '-b', help="writes the sum of the last 2 numbers to a new file")
    args = parser.parse_args()
    function(args)

main()
