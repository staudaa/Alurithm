import csv
from Logic_BFS_DFS import graf_labirin

def load_soal():
    soal_map = {'Easy': [], 'Medium': [], 'Hard': []}
    with open('D:\COLLEGE LIFE\Semester 2\ALGORITMA DAN PEMROGRAMAN II\ALURITHM_P1\Alurithm\\soal.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            soal_map[row['Tingkat']].append(row)
    return soal_map

def tingkat_node(node):
    if node in ['IN']:
        return 'Easy'
    elif node in ['B1', 'S1', 'L1']:
        return 'Medium'
    elif node in ['S2', 'L2', 'L3']:
        return 'Hard'
    return None

def main():
    soal_map = load_soal()
    posisi = 'IN'
    riwayat = [posisi]
    nyawa = 3
    skor = 100

    while posisi != 'OUT':
        tingkat = tingkat_node(posisi)
        if not soal_map[tingkat]:
            print(f"Tidak ada soal tersedia untuk tingkat {tingkat}.")
            break
        
        soal = soal_map[tingkat].pop(0)
        print(f"\nLokasi: {posisi} | Tingkat: {tingkat}")
        print(f"{soal['Soal']}")

        if soal['Tipe'] == 'PG':
            print(f"A. {soal['Opsi_A']}")
            print(f"B. {soal['Opsi_B']}")
            print(f"C. {soal['Opsi_C']}")
            print(f"D. {soal['Opsi_D']}")
            jawaban = input("Jawaban Anda (A/B/C/D): ").strip().upper()
            benar = jawaban == soal['Jawaban'].upper()
        elif soal['Tipe'] == 'Esai':
            jawaban = input("Jawaban Anda: ").strip()
            benar = jawaban.lower() == soal['Jawaban'].lower()
        else:
            print("Tipe soal tidak dikenali.")
            break

        hasil = 'benar' if benar else 'salah'
        print("Jawaban Benar!" if benar else "Jawaban Salah.")
        if hasil == 'salah':
            skor -= 10
            if skor <= 0:
                print("\nGame over!!!")
                break

        if posisi == 'L1' and hasil == 'salah':
            nyawa -= 1
            print(f"Nyawa kamu tersisa: {nyawa}")
            if nyawa == 0:
                print("Nyawa Kamu Habis! Game over!!!")
                break
            continue
        elif posisi == 'L1' and hasil == 'benar':
            nyawa = 3
        if hasil in graf_labirin[posisi]:
            posisi = graf_labirin[posisi][hasil]
            riwayat.append(posisi)
        else:
            print("Tidak ada jalur lanjutan.")
            break
        
    if posisi == 'OUT':
        print("\nSelamat! Kamu telah mencapai tujuan akhir!")
        print (f"Skor Anda: {skor}")
        
    print("\nRute yang ditempuh:")
    print(" → ".join(riwayat))

if __name__ == '__main__':
    main()
