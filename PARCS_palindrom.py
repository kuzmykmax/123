from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        (n, m) = self.read_input()
        step = (m - n) / len(self.workers)

        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(n + i * step, n + (i + 1) * step))

        pals = self.reduce_files(mapped)
        self.write_output(pals)


    @staticmethod
    @expose
    def mymap(a, b):
        pal = []
        for i in range(a, b):
            is_pal = True
            curr_num = str(i)
            str_len = int(len(curr_num))
            for j in range(0, int(str_len / 2)):
                if curr_num[j] != curr_num[str_len - j - 1]:
                    is_pal = False
            if is_pal:
                pal.append(str(i))
        return pal

    @staticmethod
    @expose
    def reduce_files(mapped):
        output = []

        for val in mapped:
            output = output + val.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        k = int(f.readline())
        f.close()
        return n, k

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(', '.join(output))
        f.write('\n')
        f.close()