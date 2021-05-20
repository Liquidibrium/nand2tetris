from typing import Tuple


class StackPush:
    # *SP=D , *SP++
    __PUSH: Tuple[str, ...] = ("@SP", "A=M", "M=D", "@SP", "M=M+1")

    @staticmethod
    def to_asm_code(segment: str, address: str, file_name: str) -> Tuple[str, ...]:
        return StackPush._filter_segment(segment, address, file_name) + StackPush.__PUSH

    @staticmethod
    def _filter_segment(segment: str, address: str, file_name: str) -> Tuple[str, ...]:
        if segment == "constant":
            return StackPush._constant(address)
        elif segment == "static":
            return StackPush._static(address, file_name)
        elif segment == "temp":
            return StackPush._segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPush._segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPush._segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == "0":
                return StackPush._pointer("THIS")
            return StackPush._pointer("THAT")
        else:  # THIS/THAT
            return StackPush._segment_pointer(segment.upper(), address)

    @staticmethod
    def _static(address: str, file_name: str) -> Tuple[str, ...]:  # file.address
        return (
            f"//push static {address}",
            f"@{file_name}.{address}",
            "D=M",
        )

    @staticmethod
    def _pointer(segment: str) -> Tuple[str, ...]:
        return "//pointer", f"@{segment}", "D=M"

    @staticmethod
    def _constant(address: str) -> Tuple[str, ...]:
        return f"//push const {address}", f"@{address}", "D=A"

    @staticmethod
    def _segment_pointer(
        segment: str, address: str, memory_location: str = "M"
    ) -> Tuple[str, ...]:
        return (
            f"//push {segment} {address}",
            f"@{address}",
            "D=A",
            f"@{segment}",
            f"A={memory_location}+D",  # calculate ptr = (segment + address)
            "D=M",  # save value,  D = *ptr
        )


class StackPop:
    # *SP-- = *D
    # use R13 to save D, *R13 = D
    # *SP-- , D=*SP , **R13 = D
    _POP: Tuple[str, ...] = (
        "@R13",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@R13",
        "A=M",
        "M=D",
    )

    @staticmethod
    def to_asm_code(segment: str, address: str, file_name: str) -> Tuple[str, ...]:
        return StackPop._filter_segment(segment, address, file_name) + StackPop._POP

    @staticmethod
    def _filter_segment(segment: str, address: str, file_name: str) -> Tuple[str, ...]:
        if segment == "static":
            return StackPop._static(address, file_name)
        elif segment == "temp":
            return StackPop._segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPop._segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPop._segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == "0":
                return StackPop._pointer("THIS")
            return StackPop._pointer("THAT")
        else:  # THIS/THAT
            return StackPop._segment_pointer(segment.upper(), address)

    @staticmethod
    def _static(address: str, file_name: str) -> Tuple[str, ...]:
        return f"//pop static {address}", f"@{file_name}.{address}", "D=A"

    @staticmethod
    def _pointer(segment: str) -> Tuple[str, ...]:
        return "//pointer", f"@{segment}", "D=A"

    @staticmethod
    def _segment_pointer(
        segment: str, address: str, memory_location: str = "M"
    ) -> Tuple[str, ...]:
        return (
            f"//pop {segment} {address}",
            f"@{segment}",
            f"D={memory_location}",
            f"@{address}",
            "D=D+A",
        )
