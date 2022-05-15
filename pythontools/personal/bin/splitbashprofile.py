#!/usr/local/bin/python3
def main():
    file = open('/Users/sidharth/.bash_profile', 'r')

    content_ubvm = ''
    content_pc = ''

    write_to_ubvm = False
    write_to_pc = False

    section_start = False
    for line in file:
        if line.startswith('##>'):
            section_start = True
            if line.find('UBVM') > 0:
                write_to_ubvm = True
            if line.find('PC') > 0:
                write_to_pc = True
        elif line.startswith('##<'):
            section_start = False
            write_to_ubvm = False
            write_to_pc = False

        if section_start:
            if write_to_ubvm:
                content_ubvm += line
            if write_to_pc:
                content_pc += line

    file_ubvm = open('/Users/sidharth/.bash_profile.ubvm', 'w')
    file_pc = open('/Users/sidharth/.bash_profile.pc', 'w')

    file_ubvm.write(content_ubvm)
    file_pc.write(content_pc)

    print('done')


if __name__ == '__main__':
    main()
