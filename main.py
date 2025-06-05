import csv
import os
from Logic_BFS_DFS import graf_labirin
from auth import login, register

def load_soal():
    soal_map = {'Easy': [], 'Medium': [], 'Hard': []}
    with open('D:\COLLEGE LIFE\Semester 2\ALGORITMA DAN PEMROGRAMAN II\ALURITHM_P1\Alurithm\db\soal.csv', newline='', encoding='utf-8') as csvfile:
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

def main_game():
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
    
    input("\nTekan Enter untuk kembali ke menu...")

def autentikasi(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Selamat datang, {username}!")
        print("\nMenu:")
        print("1. Lihat Leaderboard")
        print("2. Mulai Permainan")
        print("3. Logout")
        pilihan = input("Masukkan pilihan (1/2/3): ").strip()
        if pilihan == '1':
            print("Tampilkan leaderboard")
        elif pilihan == '2':
            print("1. Mulai")
            print("2. Kembali")
            menu = input("Masukkan pilihan menu (1/2) : ")
            if menu == "1" : 
                main_game()
            elif menu == "2" :
                continue
        elif pilihan == '3':
            print("Anda telah logout.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Selamat datang di Alurithm! \nPermainan labirin berbasis soal Algoritma dan Pemrograman Dasar")
        print("\nPilih opsi:")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3): ").strip()
        if pilihan == '1':
            register()
        elif pilihan == '2':
            username = login()
            if username:
                # Call the autentikasi function with the logged-in username
                autentikasi(username[0])  # username is a list, so we take the first element
        elif pilihan == '3':
            print("Terima kasih sudah mencoba. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == '__main__':
    main()
