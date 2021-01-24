def rawDatas2PM10(H_D3, L_D3):
    PM10 = (H_D3 * 256) + L_D3
    print("PM10 : " + str(PM10) + " ug/m3")
    #100


def rawDatas2PM2_5(H_D2, L_D2):
    PM2_5 = (H_D2 * 256) + L_D2
    print("PM2.5 : " + str(PM2_5) + " ug/m3")
    #60


def rawDatas2PM1(H_D1, L_D1):
    PM1 = (H_D1 * 256) + L_D1
    print("PM1 : " + str(PM1) + " ug/m3")


# strDatas = "424D0004E1000174424D0004E1010175424D0004E1000174424D0004E1010175"

jsonDatas = {}
# intDatas = int(strDatas,16)

# hexDatas = hex(intDatas)
# print(hexDatas)

bytearrayDatas = bytearray.fromhex(strDatas)
# print(bytearrayDatas)

# print(bytearrayDatas[0])

jsonDatas = {
    "headers": {"Head1": bytearrayDatas[0], "Head2": bytearrayDatas[1]},
    "datas": {
        "H_Lenght": bytearrayDatas[2],
        "L_Lenght": bytearrayDatas[3],
        "H_D1": bytearrayDatas[4],
        "L_D1": bytearrayDatas[5],
        "H_D2": bytearrayDatas[6],
        "L_D2": bytearrayDatas[7],
        "H_D3": bytearrayDatas[8],
        "L_D3": bytearrayDatas[9],
        "H_D4": bytearrayDatas[10],
        "L_D4": bytearrayDatas[11],
        "H_D5": bytearrayDatas[12],
        "L_D5": bytearrayDatas[13],
        "H_D6": bytearrayDatas[14],
        "L_D6": bytearrayDatas[15],
        "H_D7": bytearrayDatas[16],
        "L_D7": bytearrayDatas[17],
        "H_D8": bytearrayDatas[18],
        "L_D8": bytearrayDatas[19],
        "H_D9": bytearrayDatas[20],
        "L_D9": bytearrayDatas[21],
        "H_D10": bytearrayDatas[22],
        "L_D10": bytearrayDatas[23],
        "H_D11": bytearrayDatas[24],
        "L_D11": bytearrayDatas[25],
        "H_D12": bytearrayDatas[26],
        "L_D12": bytearrayDatas[27],
        "H_D13": bytearrayDatas[28],
        "L_D13": bytearrayDatas[29],
        "H_CS": bytearrayDatas[30],
        "L_CS": bytearrayDatas[31],
    },
}

print(jsonDatas)

print("")

rawDatas2PM10(jsonDatas["datas"]["H_D3"], jsonDatas["datas"]["H_D3"])
rawDatas2PM2_5(jsonDatas["datas"]["H_D2"], jsonDatas["datas"]["H_D2"])
rawDatas2PM1(jsonDatas["datas"]["H_D1"], jsonDatas["datas"]["H_D1"])