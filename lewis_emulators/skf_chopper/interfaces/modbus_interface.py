from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis.utils.byte_conversions import int_to_raw_bytes, BYTE, float_to_raw_bytes
from lewis.utils.replies import conditional_reply
import struct


def log_replies(f):
    def _wrapper(self, *args, **kwargs):
        result = f(self, *args, **kwargs)
        self.log.info(f"Reply in {f.__name__}: {result}")
        return result
    return _wrapper


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder="big")


@has_log
class SKFChopperModbusInterface(StreamInterface):
    """
    This implements the modbus stream interface for an skf chopper.
    """
    commands = {
        Cmd("any_command", r"^([\s\S]*)$", return_mapping=lambda x: x),
    }

    def __init__(self):
        super().__init__()
        self.read_commands = {
            353: self.get_freq,
            345: self.get_freq,
            462: self.catch_get,
            477: self.get_speed,
            240: self.catch_get,
            347: self.catch_get,
            362: self.catch_get,
            360: self.catch_get,
            0: self.catch_get
        }

        self.write_commands = {
            345: self.set_freq,
        }

    in_terminator = ""
    out_terminator = b""
    readtimeout = 10
    protocol = "stream"

    def handle_error(self, request, error):
        error_message = "An error occurred at request " + repr(request) + ": " + repr(error)
        print(error_message)
        self.log.error(error_message)
        return str(error).encode("utf-8")

    @log_replies
    @conditional_reply("connected")
    def any_command(self, command):
        self.log.info(command)
        transaction_id = command[0:2] if self.device.send_ok_transid else int(0).to_bytes(2, byteorder="big")
        protocol_id = command[2:4]
        length = int.from_bytes(command[4:6], "big")
        unit = command[6]
        function_code = int(command[7])
        data = command[8:]

        print(f"trans id {transaction_id} protocol id {protocol_id} length {length} unit {unit} function code {function_code} data {data}")

        if len(command[6:]) != length:
             raise ValueError(f"Invalid message length, expected {length} but got {len(data)}")
    
        if function_code == 3:
            return self.handle_read(transaction_id, protocol_id, unit, function_code, data)
        elif function_code == 16:
            return self.handle_write(command)
        else:
            raise ValueError(f"Unknown modbus function code: {function_code}")

    def handle_read(self, transaction_id, protocol_id, unit, function_code, data):
        mem_address = bytes_to_int(data[0:2])
        words_to_read = bytes_to_int(data[2:4])
        self.log.info(f"Attempting to read {words_to_read} words from mem address: {mem_address}")
        reply_data = self.read_commands[mem_address]()

        self.log.info(f"reply_data = {reply_data}")
        
        if type(reply_data) is float:
            data_length = 4
            littleendian_bytes = bytearray(float_to_raw_bytes(reply_data, low_byte_first=True))
            print(f"first {littleendian_bytes[:2]} second {littleendian_bytes[2:]}")
            # split up in 2-byte words, then swap endianness respectively to big endian. 
            first_word = littleendian_bytes[:2][::-1]
            second_word = littleendian_bytes[2:][::-1]
            print(f"swapped first {first_word} second {second_word}")
            reply_data_bytes = first_word + second_word


        function_code_bytes = function_code.to_bytes(1, byteorder="big")
        unit_bytes = unit.to_bytes(1, byteorder="big")

        data_length_bytes = data_length.to_bytes(1, byteorder="big")

        length = int(3+data_length).to_bytes(2, byteorder="big")


        reply = transaction_id \
            + protocol_id \
            + length \
            + unit_bytes \
            + function_code_bytes \
            + data_length_bytes \
            + reply_data_bytes

        print(f"replying with {reply}")
        print(f"REPLY: transaction id {transaction_id} protocol id {protocol_id} length {length} unit {unit_bytes} func code {function_code_bytes} data length {data_length_bytes} reply_data {reply_data_bytes}")
        print(reply_data_bytes)

        return reply

    def handle_write(self, command):
        mem_address = bytes_to_int(data[0:2])
        value = bytes_to_int(data[2:4])
        self.write_commands[mem_address](value)

        # On write, device echos command back to IOC
        return command

    def get_speed(self):
        return int(self.device.speed)

    def get_freq(self):
        return float(self.device.freq)

    def set_freq(self, value):
        self.device.freq = value

    def catch_get(self):
        return int(0)

    def catch_write(self, val):
        pass