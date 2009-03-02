#ifndef MOVEBITS_H
#define MOVEBITS_H

typedef unsigned long long Bitboard;

// basic moves bit-tables
const Bitboard left_moves[] = {
    0x0000000000000000LL, 0x0000000000000001LL, 0x0000000000000003LL, 0x0000000000000007LL,
    0x000000000000000FLL, 0x000000000000001FLL, 0x000000000000003FLL, 0x000000000000007FLL,
    0x0000000000000000LL, 0x0000000000000100LL, 0x0000000000000300LL, 0x0000000000000700LL,
    0x0000000000000F00LL, 0x0000000000001F00LL, 0x0000000000003F00LL, 0x0000000000007F00LL,
    0x0000000000000000LL, 0x0000000000010000LL, 0x0000000000030000LL, 0x0000000000070000LL,
    0x00000000000F0000LL, 0x00000000001F0000LL, 0x00000000003F0000LL, 0x00000000007F0000LL,
    0x0000000000000000LL, 0x0000000001000000LL, 0x0000000003000000LL, 0x0000000007000000LL,
    0x000000000F000000LL, 0x000000001F000000LL, 0x000000003F000000LL, 0x000000007F000000LL,
    0x0000000000000000LL, 0x0000000100000000LL, 0x0000000300000000LL, 0x0000000700000000LL,
    0x0000000F00000000LL, 0x0000001F00000000LL, 0x0000003F00000000LL, 0x0000007F00000000LL,
    0x0000000000000000LL, 0x0000010000000000LL, 0x0000030000000000LL, 0x0000070000000000LL,
    0x00000F0000000000LL, 0x00001F0000000000LL, 0x00003F0000000000LL, 0x00007F0000000000LL,
    0x0000000000000000LL, 0x0001000000000000LL, 0x0003000000000000LL, 0x0007000000000000LL,
    0x000F000000000000LL, 0x001F000000000000LL, 0x003F000000000000LL, 0x007F000000000000LL,
    0x0000000000000000LL, 0x0100000000000000LL, 0x0300000000000000LL, 0x0700000000000000LL,
    0x0F00000000000000LL, 0x1F00000000000000LL, 0x3F00000000000000LL, 0x7F00000000000000LL};

const Bitboard right_moves[] = {
    0x00000000000000FELL, 0x00000000000000FCLL, 0x00000000000000F8LL, 0x00000000000000F0LL,
    0x00000000000000E0LL, 0x00000000000000C0LL, 0x0000000000000080LL, 0x0000000000000000LL,
    0x000000000000FE00LL, 0x000000000000FC00LL, 0x000000000000F800LL, 0x000000000000F000LL,
    0x000000000000E000LL, 0x000000000000C000LL, 0x0000000000008000LL, 0x0000000000000000LL,
    0x0000000000FE0000LL, 0x0000000000FC0000LL, 0x0000000000F80000LL, 0x0000000000F00000LL,
    0x0000000000E00000LL, 0x0000000000C00000LL, 0x0000000000800000LL, 0x0000000000000000LL,
    0x00000000FE000000LL, 0x00000000FC000000LL, 0x00000000F8000000LL, 0x00000000F0000000LL,
    0x00000000E0000000LL, 0x00000000C0000000LL, 0x0000000080000000LL, 0x0000000000000000LL,
    0x000000FE00000000LL, 0x000000FC00000000LL, 0x000000F800000000LL, 0x000000F000000000LL,
    0x000000E000000000LL, 0x000000C000000000LL, 0x0000008000000000LL, 0x0000000000000000LL,
    0x0000FE0000000000LL, 0x0000FC0000000000LL, 0x0000F80000000000LL, 0x0000F00000000000LL,
    0x0000E00000000000LL, 0x0000C00000000000LL, 0x0000800000000000LL, 0x0000000000000000LL,
    0x00FE000000000000LL, 0x00FC000000000000LL, 0x00F8000000000000LL, 0x00F0000000000000LL,
    0x00E0000000000000LL, 0x00C0000000000000LL, 0x0080000000000000LL, 0x0000000000000000LL,
    0xFE00000000000000LL, 0xFC00000000000000LL, 0xF800000000000000LL, 0xF000000000000000LL,
    0xE000000000000000LL, 0xC000000000000000LL, 0x8000000000000000LL, 0x0000000000000000LL};

const Bitboard up_moves[] = {
    0x0101010101010100LL, 0x0202020202020200LL, 0x0404040404040400LL, 0x0808080808080800LL,
    0x1010101010101000LL, 0x2020202020202000LL, 0x4040404040404000LL, 0x8080808080808000LL,
    0x0101010101010000LL, 0x0202020202020000LL, 0x0404040404040000LL, 0x0808080808080000LL,
    0x1010101010100000LL, 0x2020202020200000LL, 0x4040404040400000LL, 0x8080808080800000LL,
    0x0101010101000000LL, 0x0202020202000000LL, 0x0404040404000000LL, 0x0808080808000000LL,
    0x1010101010000000LL, 0x2020202020000000LL, 0x4040404040000000LL, 0x8080808080000000LL,
    0x0101010100000000LL, 0x0202020200000000LL, 0x0404040400000000LL, 0x0808080800000000LL,
    0x1010101000000000LL, 0x2020202000000000LL, 0x4040404000000000LL, 0x8080808000000000LL,
    0x0101010000000000LL, 0x0202020000000000LL, 0x0404040000000000LL, 0x0808080000000000LL,
    0x1010100000000000LL, 0x2020200000000000LL, 0x4040400000000000LL, 0x8080800000000000LL,
    0x0101000000000000LL, 0x0202000000000000LL, 0x0404000000000000LL, 0x0808000000000000LL,
    0x1010000000000000LL, 0x2020000000000000LL, 0x4040000000000000LL, 0x8080000000000000LL,
    0x0100000000000000LL, 0x0200000000000000LL, 0x0400000000000000LL, 0x0800000000000000LL,
    0x1000000000000000LL, 0x2000000000000000LL, 0x4000000000000000LL, 0x8000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL};

const Bitboard down_moves[] = {
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000001LL, 0x0000000000000002LL, 0x0000000000000004LL, 0x0000000000000008LL,
    0x0000000000000010LL, 0x0000000000000020LL, 0x0000000000000040LL, 0x0000000000000080LL,
    0x0000000000000101LL, 0x0000000000000202LL, 0x0000000000000404LL, 0x0000000000000808LL,
    0x0000000000001010LL, 0x0000000000002020LL, 0x0000000000004040LL, 0x0000000000008080LL,
    0x0000000000010101LL, 0x0000000000020202LL, 0x0000000000040404LL, 0x0000000000080808LL,
    0x0000000000101010LL, 0x0000000000202020LL, 0x0000000000404040LL, 0x0000000000808080LL,
    0x0000000001010101LL, 0x0000000002020202LL, 0x0000000004040404LL, 0x0000000008080808LL,
    0x0000000010101010LL, 0x0000000020202020LL, 0x0000000040404040LL, 0x0000000080808080LL,
    0x0000000101010101LL, 0x0000000202020202LL, 0x0000000404040404LL, 0x0000000808080808LL,
    0x0000001010101010LL, 0x0000002020202020LL, 0x0000004040404040LL, 0x0000008080808080LL,
    0x0000010101010101LL, 0x0000020202020202LL, 0x0000040404040404LL, 0x0000080808080808LL,
    0x0000101010101010LL, 0x0000202020202020LL, 0x0000404040404040LL, 0x0000808080808080LL,
    0x0001010101010101LL, 0x0002020202020202LL, 0x0004040404040404LL, 0x0008080808080808LL,
    0x0010101010101010LL, 0x0020202020202020LL, 0x0040404040404040LL, 0x0080808080808080LL};

const Bitboard ne_moves[] = {
    0x8040201008040200LL, 0x0080402010080400LL, 0x0000804020100800LL, 0x0000008040201000LL,
    0x0000000080402000LL, 0x0000000000804000LL, 0x0000000000008000LL, 0x0000000000000000LL,
    0x4020100804020000LL, 0x8040201008040000LL, 0x0080402010080000LL, 0x0000804020100000LL,
    0x0000008040200000LL, 0x0000000080400000LL, 0x0000000000800000LL, 0x0000000000000000LL,
    0x2010080402000000LL, 0x4020100804000000LL, 0x8040201008000000LL, 0x0080402010000000LL,
    0x0000804020000000LL, 0x0000008040000000LL, 0x0000000080000000LL, 0x0000000000000000LL,
    0x1008040200000000LL, 0x2010080400000000LL, 0x4020100800000000LL, 0x8040201000000000LL,
    0x0080402000000000LL, 0x0000804000000000LL, 0x0000008000000000LL, 0x0000000000000000LL,
    0x0804020000000000LL, 0x1008040000000000LL, 0x2010080000000000LL, 0x4020100000000000LL,
    0x8040200000000000LL, 0x0080400000000000LL, 0x0000800000000000LL, 0x0000000000000000LL,
    0x0402000000000000LL, 0x0804000000000000LL, 0x1008000000000000LL, 0x2010000000000000LL,
    0x4020000000000000LL, 0x8040000000000000LL, 0x0080000000000000LL, 0x0000000000000000LL,
    0x0200000000000000LL, 0x0400000000000000LL, 0x0800000000000000LL, 0x1000000000000000LL,
    0x2000000000000000LL, 0x4000000000000000LL, 0x8000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL};

const Bitboard nw_moves[] = {
    0x0000000000000000LL, 0x0000000000000100LL, 0x0000000000010200LL, 0x0000000001020400LL,
    0x0000000102040800LL, 0x0000010204081000LL, 0x0001020408102000LL, 0x0102040810204000LL,
    0x0000000000000000LL, 0x0000000000010000LL, 0x0000000001020000LL, 0x0000000102040000LL,
    0x0000010204080000LL, 0x0001020408100000LL, 0x0102040810200000LL, 0x0204081020400000LL,
    0x0000000000000000LL, 0x0000000001000000LL, 0x0000000102000000LL, 0x0000010204000000LL,
    0x0001020408000000LL, 0x0102040810000000LL, 0x0204081020000000LL, 0x0408102040000000LL,
    0x0000000000000000LL, 0x0000000100000000LL, 0x0000010200000000LL, 0x0001020400000000LL,
    0x0102040800000000LL, 0x0204081000000000LL, 0x0408102000000000LL, 0x0810204000000000LL,
    0x0000000000000000LL, 0x0000010000000000LL, 0x0001020000000000LL, 0x0102040000000000LL,
    0x0204080000000000LL, 0x0408100000000000LL, 0x0810200000000000LL, 0x1020400000000000LL,
	0x0000000000000000LL, 0x0001000000000000LL, 0x0102000000000000LL, 0x0204000000000000LL,
    0x0408000000000000LL, 0x0810000000000000LL, 0x1020000000000000LL, 0x2040000000000000LL,
    0x0000000000000000LL, 0x0100000000000000LL, 0x0200000000000000LL, 0x0400000000000000LL,
    0x0800000000000000LL, 0x1000000000000000LL, 0x2000000000000000LL, 0x4000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL};

const Bitboard sw_moves[] = {
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000001LL, 0x0000000000000002LL, 0x0000000000000004LL,
    0x0000000000000008LL, 0x0000000000000010LL, 0x0000000000000020LL, 0x0000000000000040LL,
    0x0000000000000000LL, 0x0000000000000100LL, 0x0000000000000201LL, 0x0000000000000402LL,
    0x0000000000000804LL, 0x0000000000001008LL, 0x0000000000002010LL, 0x0000000000004020LL,
    0x0000000000000000LL, 0x0000000000010000LL, 0x0000000000020100LL, 0x0000000000040201LL,
    0x0000000000080402LL, 0x0000000000100804LL, 0x0000000000201008LL, 0x0000000000402010LL,
	0x0000000000000000LL, 0x0000000001000000LL, 0x0000000002010000LL, 0x0000000004020100LL,
    0x0000000008040201LL, 0x0000000010080402LL, 0x0000000020100804LL, 0x0000000040201008LL,
    0x0000000000000000LL, 0x0000000100000000LL, 0x0000000201000000LL, 0x0000000402010000LL,
    0x0000000804020100LL, 0x0000001008040201LL, 0x0000002010080402LL, 0x0000004020100804LL,
    0x0000000000000000LL, 0x0000010000000000LL, 0x0000020100000000LL, 0x0000040201000000LL,
    0x0000080402010000LL, 0x0000100804020100LL, 0x0000201008040201LL, 0x0000402010080402LL,
    0x0000000000000000LL, 0x0001000000000000LL, 0x0002010000000000LL, 0x0004020100000000LL,
    0x0008040201000000LL, 0x0010080402010000LL, 0x0020100804020100LL, 0x0040201008040201LL};

const Bitboard se_moves[] = {
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL, 0x0000000000000000LL,
    0x0000000000000002LL, 0x0000000000000004LL, 0x0000000000000008LL, 0x0000000000000010LL,
    0x0000000000000020LL, 0x0000000000000040LL, 0x0000000000000080LL, 0x0000000000000000LL,
    0x0000000000000204LL, 0x0000000000000408LL, 0x0000000000000810LL, 0x0000000000001020LL,
    0x0000000000002040LL, 0x0000000000004080LL, 0x0000000000008000LL, 0x0000000000000000LL,
    0x0000000000020408LL, 0x0000000000040810LL, 0x0000000000081020LL, 0x0000000000102040LL,
    0x0000000000204080LL, 0x0000000000408000LL, 0x0000000000800000LL, 0x0000000000000000LL,
    0x0000000002040810LL, 0x0000000004081020LL, 0x0000000008102040LL, 0x0000000010204080LL,
    0x0000000020408000LL, 0x0000000040800000LL, 0x0000000080000000LL, 0x0000000000000000LL,
    0x0000000204081020LL, 0x0000000408102040LL, 0x0000000810204080LL, 0x0000001020408000LL,
    0x0000002040800000LL, 0x0000004080000000LL, 0x0000008000000000LL, 0x0000000000000000LL,
    0x0000020408102040LL, 0x0000040810204080LL, 0x0000081020408000LL, 0x0000102040800000LL,
    0x0000204080000000LL, 0x0000408000000000LL, 0x0000800000000000LL, 0x0000000000000000LL,
    0x0002040810204080LL, 0x0004081020408000LL, 0x0008102040800000LL, 0x0010204080000000LL,
    0x0020408000000000LL, 0x0040800000000000LL, 0x0080000000000000LL, 0x0000000000000000LL};

const Bitboard knight_moves[] = {
    0x0000000000020400LL, 0x0000000000050800LL, 0x00000000000A1100LL, 0x0000000000142200LL,
    0x0000000000284400LL, 0x0000000000508800LL, 0x0000000000A01000LL, 0x0000000000402000LL,
    0x0000000002040004LL, 0x0000000005080008LL, 0x000000000A110011LL, 0x0000000014220022LL,
    0x0000000028440044LL, 0x0000000050880088LL, 0x00000000A0100010LL, 0x0000000040200020LL,
    0x0000000204000402LL, 0x0000000508000805LL, 0x0000000A1100110ALL, 0x0000001422002214LL,
    0x0000002844004428LL, 0x0000005088008850LL, 0x000000A0100010A0LL, 0x0000004020002040LL,
    0x0000020400040200LL, 0x0000050800080500LL, 0x00000A1100110A00LL, 0x0000142200221400LL,
    0x0000284400442800LL, 0x0000508800885000LL, 0x0000A0100010A000LL, 0x0000402000204000LL,
    0x0002040004020000LL, 0x0005080008050000LL, 0x000A1100110A0000LL, 0x0014220022140000LL,
    0x0028440044280000LL, 0x0050880088500000LL, 0x00A0100010A00000LL, 0x0040200020400000LL,
    0x0204000402000000LL, 0x0508000805000000LL, 0x0A1100110A000000LL, 0x1422002214000000LL,
    0x2844004428000000LL, 0x5088008850000000LL, 0xA0100010A0000000LL, 0x4020002040000000LL,
    0x0400040200000000LL, 0x0800080500000000LL, 0x1100110A00000000LL, 0x2200221400000000LL,
    0x4400442800000000LL, 0x8800885000000000LL, 0x100010A000000000LL, 0x2000204000000000LL,
    0x0004020000000000LL, 0x0008050000000000LL, 0x00110A0000000000LL, 0x0022140000000000LL,
    0x0044280000000000LL, 0x0088500000000000LL, 0x0010A00000000000LL, 0x0020400000000000LL};

#endif // MOVEBITS_H
