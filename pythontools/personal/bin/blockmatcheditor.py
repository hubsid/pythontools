import click
import re
import os


@click.command()
@click.option('--file', required=True)
@click.option('--begin', 'begin_regx', required=True)
@click.option('--match', 'match_regx', required=True)
@click.option('--replace', 'repl_str', required=True)
def main(file, begin_regx, match_regx, repl_str):
    pattern_obj = re.compile(match_regx)

    filename = file
    file = open(filename, 'r')
    tmpfile = open('tmpfile', 'w')

    begin = False
    match = False
    for line in file:
        if not begin:
            print(f'-{line}')
            if re.compile(begin_regx).search(line):
                begin = True
            tmpfile.write(line)
        elif not match:
            print(f'.{line}')
            match_obj = pattern_obj.search(line)
            if match_obj:
                match = True
                tmpfile.write(pattern_obj.sub(repl_str, line))
            else:
                tmpfile.write(line)
        else:
            print(f'+{line}')
            tmpfile.write(line)

    file.close()
    tmpfile.close()

    os.remove(filename)
    os.rename('tmpfile', filename)


if __name__ == '__main__':
    main()
