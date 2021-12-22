
# Convert hex string `x` to binary string `b`
# h = int(x,16)
# b = f'{h:0{len(x)*4}b}'

SAMPLE_INPUT = [
    '8A004A801A8002F478',
    '620080001611562C8802118E34',
    'C0015000016115A2E0802F182340',
    'A0016C880162017C3686B18A3D4780',
]

version_sum: int = 0

def HexStringToBinaryString(hex: str) -> str:
    return f'{int(hex,16):0{len(hex)*4}b}'

class Packet:
    def __init__(self, hex: None|str= None, bin: None|str=None) -> None:
        self.version: int = -1
        self.packet_type: int = -1
        self.literal_value: None|int = None
        self.subpackets: list[Packet] = []
        self.bin: str = ''
        if hex is not None:
            self.bin = HexStringToBinaryString(hex)
        elif bin is not None:
            self.bin = bin
        else:
            raise RuntimeError("Need packet input")

    # Consume the string that defines this packet, return leftover string bits?
    def ConsumeBits(self, bit_count: int) -> int:
        digits: int = int(self.bin[:bit_count], 2)
        self.bin = self.bin[bit_count:]
        return digits

    def ConsumeLiteral(self) -> int:
        value: int = 0
        while True:
            value <<= 4
            bits = self.ConsumeBits(5)
            value |= bits & 0xf
            if bits & 0x10:
                continue
            break
        return value
    
    def Parse(self):
        self.version = self.ConsumeBits(3)
        global version_sum
        version_sum += self.version
        self.packet_type = self.ConsumeBits(3)
        if self.packet_type == 4:  # Literal Value
            self.literal_value = self.ConsumeLiteral()
        else:  # Operator
            length_type_id = self.ConsumeBits(1)
            if length_type_id:  # 11-bit subpacket count
                subpacket_count = self.ConsumeBits(11)
                for _ in range(subpacket_count):
                    subpacket = Packet(bin=self.bin)
                    subpacket.Parse()
                    self.bin = subpacket.bin
                    self.subpackets.append(subpacket)
            else:  # 15-bit subpackets length
                subpacket_length = self.ConsumeBits(15)
                subpacket_bin = self.bin[:subpacket_length]
                self.bin = self.bin[subpacket_length:]
                while len(subpacket_bin):
                    subpacket = Packet(bin=subpacket_bin)
                    subpacket.Parse()
                    subpacket_bin = subpacket.bin
                    self.subpackets.append(subpacket)


for input in SAMPLE_INPUT:
    version_sum = 0
    packet = Packet(hex=input)
    packet.Parse()
    print(version_sum)

version_sum = 0
packet = Packet(hex='C20D7900A012FB9DA43BA00B080310CE3643A0004362BC1B856E0144D234F43590698FF31D249F87B8BF1AD402389D29BA6ED6DCDEE59E6515880258E0040A7136712672454401A84CE65023D004E6A35E914BF744E4026BF006AA0008742985717440188AD0CE334D7700A4012D4D3AE002532F2349469100708010E8AD1020A10021B0623144A20042E18C5D88E6009CF42D972B004A633A6398CE9848039893F0650048D231EFE71E09CB4B4D4A00643E200816507A48D244A2659880C3F602E2080ADA700340099D0023AC400C30038C00C50025C00C6015AD004B95002C400A10038C00A30039C0086002B256294E0124FC47A0FC88ACE953802F2936C965D3005AC01792A2A4AC69C8C8CA49625B92B1D980553EE5287B3C9338D13C74402770803D06216C2A100760944D8200008545C8FB1EC80185945D9868913097CAB90010D382CA00E4739EDF7A2935FEB68802525D1794299199E100647253CE53A8017C9CF6B8573AB24008148804BB8100AA760088803F04E244480004323BC5C88F29C96318A2EA00829319856AD328C5394F599E7612789BC1DB000B90A480371993EA0090A4E35D45F24E35D45E8402E9D87FFE0D9C97ED2AF6C0D281F2CAF22F60014CC9F7B71098DFD025A3059200C8F801F094AB74D72FD870DE616A2E9802F800FACACA68B270A7F01F2B8A6FD6035004E054B1310064F28F1C00F9CFC775E87CF52ADC600AE003E32965D98A52969AF48F9E0C0179C8FE25D40149CC46C4F2FB97BF5A62ECE6008D0066A200D4538D911C401A87304E0B4E321005033A77800AB4EC1227609508A5F188691E3047830053401600043E2044E8AE0008443F84F1CE6B3F133005300101924B924899D1C0804B3B61D9AB479387651209AA7F3BC4A77DA6C519B9F2D75100017E1AB803F257895CBE3E2F3FDE014ABC')
packet.Parse()
print(version_sum)
