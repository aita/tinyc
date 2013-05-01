# coding:utf-8

from collections import namedtuple
import struct

Code = namedtuple('Code', 'opcode i_operand s_operand')


POP = 0
PUSHI = 1
ADD = 2
SUB = 3
MUL = 4
GT = 5
LT = 6
BEQ0 = 7
LOADA = 8
LOADL = 9
STOREA = 10
STOREL = 11
JUMP = 12
CALL = 13
RET = 14
POPR = 15
FRAME = 16
PRINTLN = 17
ENTRY = 18
LABEL = 19

OPCODE_DICT = {
    POP: "POP",
    PUSHI: "PUSHI",
    ADD: "ADD",
    SUB: "SUB",
    MUL: "MUL",
    GT: "GT",
    LT: "LT",
    BEQ0: "BEQ0",
    LOADA : "LOADA",
    LOADL: "LOADL",
    STOREA: "STOREA",
    STOREL: "STOREL",
    JUMP: "JUMP",
    CALL: "CALL",
    RET: "RET",
    POPR : "POPR",
    FRAME : "FRAME",
    PRINTLN : "PRINTLN",
    ENTRY: "ENTRY",
    LABEL: "LABEL",
}
OPCODE_NAME = {v:k for k,v in OPCODE_DICT.items()}


class VirtualMachine(object):

    def __init__(self, max_stack=200):
        self.reset(max_stack)

    def reset(self, max_stack):
        self.max_stack = max_stack
        self.codes = []         # VMコード
        self.labels = {}
        # よくわからないエラー対策のため+1する
        self.stack = [None for x in range(max_stack+1)] # スタック
        self.sp = max_stack                     # スタックポインタ
        self.fp = max_stack                     # フレームポインタ
        self.pc = 0                             # プログラムカウンタ

    # def unpack(self, fp, fmt):
    #     readsize = struct.calcsize(fmt)
    #     buf = fp.read(readsize)
    #     val = struct.unpack(fmt, buf)
    #     return val

    def read_code(self, fp):
        n_code = 0
        for line in fp:
            vals = line.split()
            opcode = OPCODE_NAME[vals[0]]
            if opcode in (PUSHI, LOADA, LOADL, STOREA,
                          STOREL, FRAME, POPR,):
                ival = int(vals[1])
                self.codes.append(Code(opcode, ival, None))
            elif opcode in (BEQ0, LABEL, JUMP, CALL, ENTRY):
                sval = vals[1]
                if opcode in (LABEL, ENTRY):
                    self.labels[sval] = n_code
                else:
                    self.codes.append(Code(opcode, None, sval))
            elif opcode == PRINTLN:
                sval = ' '.join(vals[1:])[1:-1]
                self.codes.append(Code(opcode, None, sval))
            else:
                # raise ValueError("Unknown opcode: %s" % opcode)
                self.codes.append(Code(opcode, None, None))
                
            if not opcode in (LABEL, ENTRY):
                n_code += 1

        def _replace(n):
            opcode, ival, sval = n
            if opcode in (BEQ0, JUMP, CALL):
                return Code(opcode, self.labels[sval], sval)
            return n
        self.codes = map(_replace, self.codes)

    def execute_code(self, start_pc):
        self.sp = self.fp = self.max_stack
        self.pc = start_pc

        while True:
            opcode = self.codes[self.pc]
            code = opcode.opcode
            if code == POP:
                self.pop()
            elif code == PUSHI:
                self.push(opcode.i_operand)
            elif code == ADD:
                y = self.pop()
                x = self.pop()
                self.push(x+y)
            elif code == SUB:
                y = self.pop()
                x = self.pop()
                self.push(x-y)
            elif code == MUL:
                y = self.pop()
                x = self.pop()
                self.push(x*y)
            elif code == LT:
                y = self.pop()
                x = self.pop()
                self.push(x>y)
            elif code == GT:
                y = self.pop()
                x = self.pop()
                self.push(x<y)
            elif code == BEQ0:
                x = self.pop()
                if x == 0:
                    self.pc = opcode.i_operand
                    continue
            elif code == LOADA:
                 self.push(self.stack[self.fp+opcode.i_operand+3])
            elif code == LOADL:
                 self.push(self.stack[self.fp-opcode.i_operand])
            elif code == STOREA:
                self.stack[self.fp+opcode.i_operand+3] = self.top()
            elif code == STOREL:
                self.stack[self.fp-opcode.i_operand] = self.top()
            elif code == JUMP:
                self.pc = opcode.i_operand
                continue
            elif code == CALL:
                self.push(self.pc+1)
                self.pc = opcode.i_operand;
                continue
            elif code == RET:
                x = self.pop()
                self.sp = self.fp
                self.fp = self.pop()
                if self.sp >= self.max_stack:
                    print 'stop...'
                    return
                self.pc = self.pop()
                continue
            elif code == POPR:
                self.sp = self.sp - opcode.i_operand
                self.push(x)
            elif code == FRAME:
                self.push(self.fp)
                self.fp = self.sp
                self.sp -= opcode.i_operand
            elif PRINTLN:
                 print opcode.s_operand % self.top()
            else:
                raise ValueError("Unknown opcode: %s" % opcode)
            self.pc += 1

    def top(self):
        return self.stack[self.sp+1]

    def pop(self):
        self.sp += 1
        return self.stack[self.sp]

    def push(self, x):
        self.stack[self.sp] = x
        self.sp -= 1


if __name__ == "__main__":
    import sys
    vm = VirtualMachine()
    vm.read_code(open(sys.argv[1]))
    # print 'codes', vm.codes
    vm.execute_code(vm.labels["main"])
