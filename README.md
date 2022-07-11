# brodcast-fuzzer

python3 pngfuzzer.py 3

3 is number of running

png file format:

89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
00 00 00 01 00 00 00 01 08 02 00 00 00 90 77 53
DE 00 00 00 0C 49 44 41 54 08 D7 63 F8 CF C0 00
00 03 01 01 00 18 DD 8D B0 00 00 00 00 49 45 4E
44 AE 42 60 82
1. first 8 bytes is PNG signature (89 50 4E 47 0D 0A 1A 0A)
2. next couple bytes is header size (00 00 00 0D, number of bytes can be different?)
3. next 49484452 identifies a header chunk (49 48 44 52)
4. next 4 bytes is image pixel wide (00 00 00 01)
5. next 4 bytes is image pixel high (00 00 00 01)
6. next 1 byte is how many bits per pixel (08)
7. next 1 byte indicates color type (02)
8. next 1 byte indicates compression method (00, seems 0 is the only accepted value?)
9. next 1 byte indicates filter method (00, seems 0 is the only accepted value?)
10. next 1 byte indicates not interlaced (00)
11. next 907753DE is CRC of chunk's type and content (907753DE)
12. next couple bytes is IDAT content size (00 00 00 0C, number of bytes can be different?)
13. next 49444154 identifies a data chunk (49 44 41 54)
14. next 1 byte indicates DEFLATE compression method using a 256-byte window (08)
15. next 1 byte indicates ZLIB FCHECK value, no dictionary used, maximum compression algorithm (D7)
16. next couple bytes is a compressed DEFLATE block using the static Huffman code that decodes to 0x00 0xFF 0x00 0x00 (63 F8 CF C0 00)
17. next 4 bytes is the ZLIB check value: the Adler32 checksum of the uncompressed data (03 01 01 00)
18. next 4 bytes is CRC of chunk's type and content (18 DD 8D B0)
19. the rest of bytes indicates the end of image (00 00 00 00 49 45 4E 44 AE 42 60 82)
